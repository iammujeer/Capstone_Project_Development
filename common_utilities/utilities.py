import pandas as pd
from sqlalchemy import create_engine 
#import cx_Oracle
import logging

#Logging Config

logging.basicConfig(
    filename="application_logs/etljob.log",
    filemode='a',
    format="%(asctime)s-%(levelname)s%(message)s",
    level=logging.INFO
)   

def read_file_and_write_to_database(file_path,file_type):
    if file_type =='csv':
        df = pd.read_csv(file_path)
    elif file_type =='json':
        df = pd.read_json(file_path)
    elif file_type =='xml':
        df = pd.read_xml(file_path,xpath=".//item")
    else:
        raise ValueError(f"unsupported file type passed {file_type}")
    return df