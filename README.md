
# Global Solution - 2 Semestre 2024

## Energia para um Futuro Sustentável



## Arquitetura da Solução

![image](https://github.com/user-attachments/assets/fcfe46b2-1b83-4f8e-973b-e00ebc3b8952)


## Etapas 
Para a disciplina de Cloud Computing será necessário a execução das seguintes etapas:

### 1. Definição e exploração do Dataset:

Usar algum dataset de clima. Por exemplo: https://www.kaggle.com/datasets?search=climate+disaster+csv

**Entrega:** URL do arquivo escolhido e explicação da massa de dados

**Valor (2.0)**

### 2. Criação dos recursos na Azure por meio de IaC (terraform):

Criar os serviços Azure Storage Account e Azure Cosmo DB

Nome do Storage Account: stglobalsolutionrmxxxxxx (substiruir o xxxxxx pelo RM do aluno)

Nome da Instância Cosmo DB: cosmoglobalsolutuionrmxxxxxx (substiruir o xxxxxx pelo RM do aluno)

Criar ou utilizar uma conta no Databricks Community Edition

**Entrega:** Script IaC e telas (print screen) dos recursos criados.

**(Valor 4.0)**


### 3. Desenvolvimento de um Script em Python:

Desenvolver um script em Python para ler os dados do Azure Storage Account, processar esses dados de acordo com algum algoritmo de Data Science, gravar os resultados no Cosmo DB.

O algoritmo de Data Science pode ser utilizado de outra disciplina (ML por exemplo).

Usar como exemplo o código "function_app.py". Nesse código tem as funções para conexão com o Storage Account, com o Cosmo DB, leitura de um arquivo CSV, grvação de registros em JSON no Cosmo DB.

**Entrega:** Script Python e tela da execução do Script.

**(Valor 4.0)**

**As imagens deverão estar todas em um único documento PDF. Os códigos devem estar em arquivos TXT e em arquivos separados por script**
