import logging
from azure.storage.blob import BlobServiceClient
import pymongo
import json
import os
import azure.functions as func

# Configurações do Blob Storage
connection_string = "<Inserir a String de conexão com o Azure Storage Account>"
# Exemplo:
#connection_string = "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=stfiapgs;AccountKey=rQ/Cdadasdfsdqffsdfs8kvxcvxcFkvCTzNeq8lsfsdfhsdfidsfksdIGKQJhrgQR8sX9KG4L2Xjv9m7ldfsdfs+AStTm0ldg==;BlobEndpoint=https://stfiapgs.blob.core.windows.net/;FileEndpoint=https://stfiapgs.file.core.windows.net/;QueueEndpoint=https://stfiapgs.queue.core.windows.net/;TableEndpoint=https://stfiapgs.table.core.windows.net/"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = '<nome do contrainer>'
blob_name = '<nome do arquivo CSV ou JSON>'

# Configurações do Cosmos DB
CONNECTION_STRING = "<Inserir a String de conexão com o Azure Cosmo DB>"
# Exemplo
#CONNECTION_STRING = "mongodb://cosmodbserver-2tscr:3243l3k2hklwfed8p34y2sdfO4bAA==@cosmodbserver-2tscr.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@cosmodbserver-2tscr@"

DB_NAME = "<nome_do_cosmo_db>"
UNSHARDED_COLLECTION_NAME = "<nome da collection>"

# Função para ler o CSV e converter em DataFrame
def read_csv_from_azure(blob_stream):

    # Ler o CSV usando pandas
    df = pd.read_csv(io.BytesIO(blob_stream))
    
    return df

# Função para baixar o blob do Azure Blob Storage e processar os dados na memória
def download_blob_storage(blob_service_client, container_name, blob_name):
    """Download the JSON file from Blob Storage and return its content as an array"""
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_data = blob_client.download_blob().readall().decode('utf-8')
        logging.info("Blob baixado com sucesso!")
        print("Blob baixado com sucesso!")

        # Baixar o blob como um stream
        blob_stream = blob_client.download_blob().readall()
        
        return read_csv_from_azure(blob_stream)
    
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
def save_documents(collection, records):
    """Save a list of documents to the collection"""
    
    # Gravar cada registro no Cosmos DB
    for record in records:
        collection.insert_one(record)

    logging.info(f"Dados gravados com sucesso no container '{container_name}' do Cosmos DB.")
    print(f"Dados gravados com sucesso no container '{container_name}' do Cosmos DB.")

# Função principal
def main():
    logging.info('Execução da função MAIN')

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
        df = download_blob_storage(blob_service_client, container_name, blob_name)

        ##
        ## Trabalhar o algoritmo de Data Science nesse trecho
        ##

        # Converter o DataFrame para uma lista de dicionários
        records = json.loads(df.to_json(orient='records'))
        
        # Criar a coleção no Cosmos DB
        collection = create_database_unsharded_collection(client)

        # Salvar os documentos na coleção
        save_documents(collection, records)

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

if __name__ == "__main__":
    main()