import json
import logging
import pymysql
import requests
import os

#setup logging module

#Loading environment variables
RDS_USER=os.environ["RDS_USER"]
RDS_PASSWORD=os.environ["RDS_PASSWORD"]
RDS_HOST=os.environ["RDS_HOST"]
RDS_DB=os.environ["RDS_DB"]
API_KEY = os.environ["API_KEY"]
API_HOST="https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
currency = "USD"


try:
    conn = pymysql.connect(host=RDS_HOST,user=RDS_USER, passwd=RDS_PASSWORD, database=RDS_DB, connect_timeout=5)
    logging.info("Database connection successful")
except pymysql.Error as error:
    logging.error("Error connecting to database:", error)
    


def lambda_handler(event, context):
    # Extraer datos de CoinMarketCap
    api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {
        'symbol': 'BTC,ETH',
        'convert': 'USD'
    }
    headers = {
        'X-CMC_PRO_API_KEY': os.environ['API_KEY']
    }
    response = requests.get(api_url, params=params, headers=headers)
    data = response.json()

    # Procesar datos y almacenar en la base de datos
    btc = data['data']['BTC']['quote']['USD']['price']
    eth = data['data']['ETH']['quote']['USD']['price']
    
    insert_table(btc,eth)

    # Devolver respuesta en formato JSON
    response_body = {
        'statusCode': 200,
        'body': json.loads(json.dumps({
            'BTC_price': btc,
            'ETH_price': eth
        }))
    }
    return response_body


def insert_table(btc_price, eth_price):
    try:
    # Crear un objeto cursor usando el método cursor()
        with conn.cursor() as cursor:
            # Sentencia SQL para la inserción
            sql_query = "INSERT INTO price_table (BTC, ETH) VALUES (%s, %s)"
            values = (btc_price, eth_price)
            cursor.execute(sql_query, values)
            conn.commit()
            logging.info("Database successfully inserted")
            return
    finally:
        return