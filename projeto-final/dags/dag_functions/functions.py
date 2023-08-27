from datetime import datetime
import json
import os
import pandas as pd

import requests
import boto3
from botocore import exceptions
from botocore.exceptions import ClientError
from os import getenv
from dotenv import load_dotenv
from abc import ABC


load_dotenv('/opt/airflow/outputs/credentials .env')

class AWS_Airflow(ABC):
    AWS_ACCESS_KEY_ID = getenv('AWS_ID')
    AWS_SECRET_ACCESS_KEY = getenv('AWS_KEY')
    SECRET_NAME = "secret-projeto-final-bootcamp"
    REGION_NAME = "us-east-1"

    def __init__(self) -> None:
        self.s3_client = boto3.client('s3', aws_access_key_id=self.AWS_ACCESS_KEY_ID, aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY)
        self.s3_resource = boto3.resource('s3', aws_access_key_id=self.AWS_ACCESS_KEY_ID, aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY)

    @staticmethod
    def get_secret() -> str:
        session = boto3.session.Session(aws_access_key_id=AWS_Airflow.AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_Airflow.AWS_SECRET_ACCESS_KEY)
        client = session.client(service_name='secretsmanager', region_name=AWS_Airflow.REGION_NAME)
        try:
            get_secret_value_response = client.get_secret_value(SecretId=AWS_Airflow.SECRET_NAME)
            return get_secret_value_response['SecretString']
        except ClientError as e:
            raise e

    @staticmethod
    def get_token(secret) -> str:
        url = "https://api.cnptia.embrapa.br/token"
        payload = f"grant_type=password&username={json.loads(secret)['username']}&password={json.loads(secret)['password']}%40"
        headers = {
            "Authorization": f"Basic {json.loads(secret)['token']}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.text)["access_token"]
    
    @staticmethod
    def get_embrapa_data(token):
        dfs = {}
        endpoints = {
            "produtos-biologicos": "bioinsumos/v1/produtos-biologicos"
            ,"inoculantes": "bioinsumos/v1/inoculantes"
            ,"obtentores": "agritec/v1/obtentores"
            ,"culturas": "agritec/v1/culturas"
        }
        for key, value in endpoints.items():
            url = f"https://api.cnptia.embrapa.br/{value}"
            payload={}
            headers = {
            'Authorization': f'Bearer {token}'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            dfs[key] = json.loads(response.text)
        return dfs
    
    @staticmethod
    def write_data_s3(dfs):
        for chave,valor in dfs.items():
            df = pd.DataFrame(valor['data'])
            temp_file_path = '/tmp/temp_dataframe.csv'
            df.to_csv(temp_file_path, index=False)
            data_proc = datetime.now().strftime("%Y%m%d_%H%M%S")
            s3_client = boto3.client(
                's3'
                , aws_access_key_id = getenv('AWS_ID')
                , aws_secret_access_key = getenv('AWS_KEY')
            )
            bucket_name = 'data-lake-projeto-final'
            s3_file_path = f'embrapa/{chave}/dados_{data_proc}.csv'
            try:
                # Carrega o arquivo temporário para o S3
                s3_client.upload_file(temp_file_path, bucket_name, s3_file_path)
                print(f"DataFrame salvo como '{s3_file_path}' no S3 com sucesso.")
            except Exception as e:
                print(f"Erro ao carregar o arquivo para o S3: {e}")
            finally:
                # Remove o arquivo temporário local
                os.remove(temp_file_path)
        