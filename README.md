## Telegram bot para investidores
    O objetivo desse bot é informar ao investidor quando uma ação cai ou sobe determinada porcentagem

[Telegram](https://telegram.org) é um aplicativo de mensagens com foco na velocidade e segurança. É super rápido, simples e gratuito.

## Gerar token bot telegram

Com o telegram instalado em seu smart phone, você pode gerar um tolken de telegram bot atraves do [Bot Father](https://telegram.me/BotFather)

## Gerar token HG Brasil
O [HG Brasil](https://hgbrasil.com/status/finance) fornece uma api (HG Finance API) para a consulta de cotação de ações, iremos utiliza-lá para obter a cotação atual dos ativos
Você deve gerar uma API Token na [HG Brasil](https://hgbrasil.com/status/finance).

## Requisitos
       Python >= 3.7
       PostgreSQL >= 12.1

# Instalação
### Dependencias em sistemas baseado em Debian
       sudo apt-get install postgresql
       sudo apt-get install python-psycopg2
       sudo apt-get install libpq-dev
### Requirements
    pip install -r requirements.txt

#### Configuração de banco de dados

###### Criar banco

    Necessario criar um banco de dados postgress

###### arquivo conf/database.py
    Inserir os dados de conexão com o postgreSQL no constutor:
    def __init__(self, host='your_host', db='your_database', user='your_user', password='your_password')

###### Criar tabelas

    python3 setup_database.py

#Inserir tokens
    * renomear o arquivo .example_env para .env
    * Os tokens gerados anteriormente (Token telegram bot e HG Brasil) devem ser inseridos no arquivo .env em suas respectivas variaveis

# Usuários
    O Bot só ira responder a usuários com o ID cadastrado na tabela users

    Para descobrir qual o ID do seu usuario, envie ao bot a seguinte mensagem:
    /start

    Essa é a unica rota que irá responder um usuário não cadastrado

    Pegue o ID que irá retornar, e insira na tabela Users. Execute no seu SGBD:
    insert into users(user_id,username) values (SEU_ID,SEU_NOME)
    SEU_ID = INT
    SEU_NOME = STRING

# Inicializar
    python3 core.py

# Cadastrando alertas
    Para cadastrar um novo alerta, envie a seguinte mensagem ao bot:
    TICKET:PORCENTAGEM_QUEDA:PORCENTAGEM_ALTA
    Exemplo:
    ITSA4:5:8

    Dessa forma, irá avisar o usuário quando a ação da Itausa (ITSA4) cair 5 Porcento ou subir 8 Porcento


# Médotos disponíveis
    /start
        Retorno: Olá, eu sou seu bot de investimentos, seu ID é 999999999

    /inserir
        Exemplo: /inserir ITSA4:4:2
        Retorno:   ITSA4  inserido com sucesso

    /excluir
        Exemplo: /excluir ITSA4
        Retorno:   ITSA4 excluido com sucesso



### Documentações
[Telegram Bot](https://core.telegram.org/bots/api)

[HG Brasil](https://console.hgbrasil.com/documentation/finance)
