
# Azure Cosmos DB with MongoDB API - Python Integration

This project provides a quick start guide for integrating a Python application with Azure Cosmos DB using the MongoDB API. It also demonstrates the creation and deployment of an Azure Function that interacts with Cosmos DB.

## Summary
- Introduction
- Prerequisites
- Project Setup
- Local Execution
- Azure Deployment
- Environment Variable Management
- Additional Resources
- Contribution
- License

---

## Introduction

This repository is a basic example to help you get started with developing Python applications that use Azure Cosmos DB with the MongoDB API. It includes an Azure Function that can be published to Azure and run in a consumption environment.

---

## Prerequisites

Before you begin, ensure you have the following installed and configured on your system:

- **Azure CLI**: [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- **Active Azure account**: [Create an Azure account](https://azure.microsoft.com/en-us/free/)
- **Python 3.11+**: [Install Python](https://www.python.org/downloads/)
- **Azure Functions Core Tools**: [Install Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- **Git**: [Install Git](https://git-scm.com/)

---

## Project Setup

### 1. Clone the repository:
```bash
git clone https://github.com/conradperes/azure-cosmos-db-mongodb-python-getting-started-main.git
cd azure-cosmos-db-mongodb-python-getting-started-main
```

### 2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### 3. Install Python dependencies:
```bash
sh setup-venv.sh
```

### 4. Run the setup script:
This script will install the Resource Group, Storage Account, Blob storage, upload the `summary-2014.json` to blob storage, create the Cosmos DB account, database, and collection.
```bash
sh setup.sh
```

### 5. Set the environment variables:
Configure the necessary environment variables. Add these to your `.env` file or export them in your terminal session:
```bash
export FUNCTION_APP_NAME="my-function-app-172394009"
export RESOURCE_GROUP="myResourceGroup3"
export STORAGE_ACCOUNT_NAME="mystorageaccountunique2"
export REGION="brazilsouth"
export NAME_COSMOSDB_ACCOUNT="conradcosmosdb"
export AZURE_STORAGE_CONNECTION_STRING=$(az storage account show-connection-string --name $STORAGE_ACCOUNT_NAME --resource-group $RESOURCE_GROUP --query connectionString --output tsv)
export AZURE_COSMOS_CONNECTION_STRING=$(az cosmosdb keys list --name $NAME_COSMOSDB_ACCOUNT --resource-group $RESOURCE_GROUP --type connection-strings --query "connectionStrings[0].connectionString" -o tsv)
export API_MANAGEMENT_NAME="apimanagementconrad"
export API_NAME="myfunctionap"
export FUNCTION_URL=https://$FUNCTION_APP_NAME.azurewebsites.net/api/myfunction
export API_PATH=/myfunction
```

---

## Local Execution

### 1. Start the Azure Function locally:
```bash
func start
```

### 2. Test the function:
You can now access the locally generated endpoint and test the function.

---

## Azure Deployment

### 1. Deploy the Azure Function:
Run the setup script to automatically create the Function App and deploy the function to Azure.
```bash
sh setup-functions.sh
```

### 2. Publish changes:
If you modify the code and need to redeploy the function, use the following command:
```bash
func azure functionapp publish $FUNCTION_APP_NAME
```

---

## Environment Variable Management

This project uses environment variables to configure connections to Azure Cosmos DB and the Storage Account. These variables can be set both locally (in `.env` or directly in the shell) and in the Azure environment.

---

## Additional Resources

- [Azure Cosmos DB Documentation](https://docs.microsoft.com/en-us/azure/cosmos-db/introduction)
- [Azure Functions Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/functions-overview)
- [MongoDB API Example in Cosmos DB](https://docs.microsoft.com/en-us/azure/cosmos-db/mongodb-introduction)

---

## Contribution

Contributions are welcome! Feel free to open issues and pull requests.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
