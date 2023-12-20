# AUTOMAÇÂO GOOGLE TRENDS 

> Status: em andamento 🚀

## Tecnologias usadas

* Python
* FASTAPI
* Docker
* Postgres
* AWS
* Selenium

## Como executar o projeto
1. Ir até a pasta do projeto e criar a virualenv

> virtualenv venv

2. Ative a virtualenv

> source venv/bin/activate

3. Instale as dependencias

> pip install -r requirements.txt

4. Na raiz do projeto, onde estiver o arquivo main.py execute: 

> python main.py

### Se sua distribuição adotar o PEP 668 

1. Ir até a pasta do projeto e criar a virualenv
> python3 -m venv .venv

2. Ative a virtualenv
> source .venv/bin/activate

3. Instale as dependencias

> python3 -m pip install -r requirements.txt

4. Na raiz do projeto, onde estiver o arquivo main.py execute: 

> python3 -m main

* Teste local

> http://127.0.0.1:8000/docs

## Como fazer migrações no banco de dados

1. Execute o comando para criar o arquivo de migração no versions

> alembic revision -m "<nome-da-migraçao>"

2. Depois de criada a migração execute

> alembic upgrade head --sql

> alembic upgrade head

### Obs: consulte a documentação do alembic para entender como fazer a migração no banco de dados, pois se trata de algo um tanto complexo. 

### Arquitetura do projeto

- `alembic/`: Dentro dessa pasta fica tudo relacionado ao Alembic
  - `versions/`: Aqui fica os arquivos de migrações
  - `env.py`: Arquivo que podemos fazer algumas configurações no Alembic
- `database/`: Contém arquivos de conexão com o banco de dados
- `models`: Pasta que abriga os models do banco de dados
- `alembic.ini`: arquivo responsável por iniciar o alembic, contém informações do banco de dados
- `bot_trends.py`: automação do Google Trends
- `main.py`: arquivo responsável por iniciar o projeto


### Sobre o Projeto

> O bot abre a navegador já indo direto para o Google Trends.

> Ao abrir o swagger, há um endpoint de Post com alguns parametros, que são: 

- `param`: aqui é onde vai o parametro de pesquisa. O que você quiser pesquisar. 

- `country`: aqui já se trata de um filtro de região.

- `period`: aqui é simplesmente o filtro de data. Está Últimos 7 dias por default. No entanto,  Período Personalizado, o usuário consegue escolher qual data exata quer. 

- `initial_date` e `end_date`: serve apenas caso o usuário escolha o Período Personalizado.

> O bot vai baixar os arquivos CSV proceduralmente. Começando de cima para baixo. Ai ele vai para uma pasta chamada file, dentro do projeto (por hora, já que os arquivos vão para s3). E depois disso os dados que estão dentro do arquivo serão tratados e jogados dentro do banco de dados. 


