import logging
from azure.storage.blob import BlobServiceClient
import pymongo
import json
import os
import azure.functions as func

# Configurações do Blob Storage
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = 'conradcontainer'
blob_name = 'part-r-00000-f5c243b9-a015-4a3b-a4a8-eca00f80f04c.json'

# Configurações do Cosmos DB
CONNECTION_STRING = os.getenv("AZURE_COSMOS_CONNECTION_STRING")
DB_NAME = "api-mongodb-sample-database"
UNSHARDED_COLLECTION_NAME = "classification-colors-ml-collection"

# Função para ler o JSON de uma string
def read_json_string(json_string):
    """Read JSON string and return its contents as a list of dictionaries"""
    try:
        data = [json.loads(line.strip()) for line in json_string.splitlines()]
        return data
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        raise e

# Função para baixar o blob do Azure Blob Storage e processar os dados na memória
def download_blob_storage(blob_service_client, container_name, blob_name):
    """Download the JSON file from Blob Storage and return its content as an array"""
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_data = blob_client.download_blob().readall().decode('utf-8')
        logging.info("Blob baixado com sucesso!")
        return read_json_string(blob_data)
    except Exception as e:
        logging.error(f"Erro ao baixar o blob: {e}")
        return []

# Função para criar o banco de dados e a coleção
def create_database_unsharded_collection(client):
    """Create sample database with shared throughput if it doesn't exist and an unsharded collection"""
    db = client[DB_NAME]

    # Verifique coleções existentes
    logging.info(f"Coleções disponíveis no DB: {db.list_collection_names()}")

    # Create database if it doesn't exist
    if DB_NAME not in client.list_database_names():
        db.command({'customAction': "CreateDatabase", 'offerThroughput': 400})
        logging.info(f"Created db {DB_NAME} with shared throughput")

    # Create collection if it doesn't exist
    if UNSHARDED_COLLECTION_NAME not in db.list_collection_names():
        db.command({'customAction': "CreateCollection", 'collection': UNSHARDED_COLLECTION_NAME})
        logging.info(f"Created collection {UNSHARDED_COLLECTION_NAME}")

    return db[UNSHARDED_COLLECTION_NAME]

# Função para salvar documentos na coleção
def save_documents(collection, documents):
    """Save a list of documents to the collection"""
    for document in documents:
        # Verifique se o documento já existe na coleção
        if collection.find_one({"lab": document["lab"], "color": document["color"], "value1": document["value1"], "value2": document["value2"]}):
            logging.info(f"Documento já existe: {document}")
        else:
            collection.insert_one(document)
            logging.info(f"Documento inserido: {document}")
    logging.info(f"Processamento de {len(documents)} documentos concluído.")

# Função principal
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        logging.info("Conexão ao Blob Storage estabelecida com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao conectar ao Blob Storage: {e}")
        return func.HttpResponse("Erro ao conectar ao Blob Storage", status_code=500)

    if not CONNECTION_STRING:
        logging.error("A string de conexão do Cosmos DB não foi encontrada nas variáveis de ambiente.")
        return func.HttpResponse("Erro: A string de conexão do Cosmos DB não foi encontrada.", status_code=500)

    logging.info("Cosmos DB Connection String encontrada.")

    try:
        client = pymongo.MongoClient(CONNECTION_STRING)
        logging.info("Tentando se conectar ao Cosmos DB...")
        client.server_info()  # Isso irá lançar uma exceção se a conexão falhar
        logging.info("Conexão ao Cosmos DB estabelecida com sucesso.")

        # Download do blob e leitura dos documentos
        documents = download_blob_storage(blob_service_client, container_name, blob_name)
        logging.info(f"Documentos lidos: {documents}")

        # Criar a coleção no Cosmos DB
        collection = create_database_unsharded_collection(client)

        # Salvar os documentos na coleção
        save_documents(collection, documents)
    except pymongo.errors.OperationFailure as e:
        logging.error(f"Falha na operação do MongoDB: {e}")
        return func.HttpResponse(f"Erro ao conectar ao Cosmos DB: {e}", status_code=500)
    except pymongo.errors.ServerSelectionTimeoutError as e:
        logging.error(f"Erro ao conectar ao servidor do MongoDB: {e}")
        return func.HttpResponse("Erro ao conectar ao servidor do Cosmos DB", status_code=500)
    except Exception as e:
        logging.error(f"Erro desconhecido ao conectar ao Cosmos DB: {e}")
        return func.HttpResponse(f"Erro desconhecido: {e}", status_code=500)

    return func.HttpResponse("Dados inseridos com sucesso no Cosmos DB", status_code=200)

# Registro do Trigger HTTP
app = func.FunctionApp()

@app.function_name(name="MyFunction")
@app.route(route="MyFunction", methods=["GET", "POST"], auth_level=func.AuthLevel.ANONYMOUS)
def MyFunction(req: func.HttpRequest) -> func.HttpResponse:
    return main(req)