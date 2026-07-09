import pandas as pd
from sqlalchemy import create_engine 
#import cx_Oracle
import logging

from common_utilities.utilities import read_file_and_write_to_database

#Logging Config

logging.basicConfig(
    filename="application_logs/etljob.log",
    filemode='a',
    format="%(asctime)s-%(levelname)s%(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)
#DB Conn
oracledb_conn = create_engine(
    "oracle+oracledb://system:admin@localhost:1521/xe"
)

mysql_conn =  create_engine(
    "mysql+pymysql://root:admin@localhost:3306/Feb2026Retaildwh"
)

class DataExtaction:
    def extract_sales_data_load_stage(self,file_path,file_type):
        logger.info("Data extraction has started for sales data")
        df = read_file_and_write_to_database(file_path,file_type)
        df.to_sql("stage_sales",mysql_conn,index=False)
        logger.info("Data extraction completed for sales data")

    def extract_product_data_load_stage(self,file_path,file_type):
        logger.info("Data extraction has started for product data")
        df = read_file_and_write_to_database(file_path,file_type)
        df.to_sql("stage_product",mysql_conn,index=False)
        logger.info("Data extraction completed for product data")

    def extract_inventory_data_load_stage(self,file_path,file_type):
        logger.info("Data extraction has started for inventory data")
        df = read_file_and_write_to_database(file_path,file_type)
        df.to_sql("stage_inventory",mysql_conn,index=False)
        logger.info("Data extraction completed for inventory data")

    def extract_supplier_data_load_stage(self,file_path,file_type):
        logger.info("Data extraction has started for supplier data")
        df = read_file_and_write_to_database(file_path,file_type)
        df.to_sql("stage_supplier",mysql_conn,index=False)
        logger.info("Data extraction completed for supplier data")

    def extract_stores_data_load_stage(self):
        logger.info("Data extraction has started for stores data")
        df = pd.read_sql("""SELECT * FROM STORES""",oracledb_conn)
        df.to_sql("stage_stores",mysql_conn,index=False)
        logger.info("Data extraction completed for stores data")

if __name__ == "__main__":
    de = DataExtaction()
    
    de.extract_sales_data_load_stage("source_systems/sales_data.csv","csv")
    de.extract_product_data_load_stage("source_systems/product_data_from_linux.csv","csv")
    de.extract_inventory_data_load_stage("source_systems/inventory_data.xml","xml")
    de.extract_supplier_data_load_stage("source_systems/supplier_data.json","json")    
    de.extract_stores_data_load_stage()