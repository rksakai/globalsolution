resource "azurerm_resource_group" "example" {
  name     = "rg-teste"
  location = "East US"
}

# Definir a conta do Azure Cosmos DB com a API do MongoDB
resource "azurerm_cosmosdb_account" "example" {
  name                = "cosmosdb-teste"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  offer_type          = "Standard"
  kind                = "MongoDB"
  #enable_automatic_failover = true

  consistency_policy {
    consistency_level = "Session"
  }

  # Definir o throughput (RU/s)
  geo_location {
    location          = azurerm_resource_group.example.location
    failover_priority = 0
  }

  capabilities {
    name = "EnableMongo"
  }
}

# Definir o recurso de banco de dados do Cosmos DB com a API do MongoDB
resource "azurerm_cosmosdb_mongo_database" "db_teste" {
  name                = "db_gs"
  resource_group_name = azurerm_resource_group.example.name
  account_name        = azurerm_cosmosdb_account.example.name
  throughput          = 400
}
