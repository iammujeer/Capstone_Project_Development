import pandas as pd
from sqlalchemy import create_engine 
#import cx_Oracle
import logging

from common_utilities.utilities import read_file_and_write_to_database
from project_config.etlconfig import *
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
    f"oracle+oracledb://{oracle_user}:{oracle_pwd}@{oracle_localhost}:{oracle_port}/{oracle_service}"
)

mysql_conn =  create_engine(
    f"mysql+pymysql://{mysql_user}:{mysql_pwd}@{mysql_localhost}:{mysql_port}/{mysql_database}"
)

class DataTransformation:
    def transform_filtered_sales_data(self):
        logger.info("Filter transformation has started for sales data")
        try:
            query = """select * from stage_sales where sale_date >= '2024-09-10'"""
            df = pd.read_sql(query,mysql_conn)
            df.to_sql("filtered_sales",mysql_conn,index=False)
            logger.info("Filter transformation completed for filtered sales data")

        except Exception as e:
            logger.error(f"Error encountered while data extraction of sales data,{e},exc_info=True")

    def transform_router_sales_data_high_region(self):
        logger.info("Router transformation has started for high sales data")
        try:
            query = """SELECT * FROM FILTERED_SALES WHERE REGION = 'HIGH'"""
            df = pd.read_sql(query,mysql_conn)
            df.to_sql("high_sales",mysql_conn,index=False)
            logger.info("Router transformation completed for high sales data")

        except Exception as e:
            logger.error(f"Error encountered while data extraction of high sales data,{e},exc_info=True")
        
    def transform_router_sales_data_low_region(self):
        logger.info("Router transformation has started for low sales data")
        try:
            query = """SELECT * FROM FILTERED_SALES WHERE REGION = 'low'"""
            df = pd.read_sql(query,mysql_conn)
            df.to_sql("low_sales",mysql_conn,index=False)
            logger.info("Router transformation completed for low sales data")

        except Exception as e:
            logger.error(f"Error encountered while data extraction of low sales data,{e},exc_info=True")

    def transform_aggregator_sales_data(self):
        logger.info("Aggregator transformation has started for sales data")
        try:
            query = """SELECT product_id,year(sale_date) as year, month(sale_date) as month,
                       sum(quantity*price) total_sales
                       FROM filtered_sales
                       group by product_id,year(sale_date), month(sale_date) 
                       order by product_id"""
            df = pd.read_sql(query,mysql_conn)
            df.to_sql("monthly_sales_summary_source",mysql_conn,index=False)
            logger.info("Aggregator transformation completed for sales data")

        except Exception as e:
            logger.error(f"Error encountered while data extraction of aggregator sales data,{e},exc_info=True")

    def transform_joiner_sales_product_stores(self):
        logger.info("Joiner transformation has started for sales data")
        try:
            query = """SELECT filtered_sales.sales_id,filtered_sales.quantity,(filtered_sales.quantity*filtered_sales.price)  SALES_AMOUNT,
                       filtered_sales.sale_date,stage_product.product_id, stage_product.product_name,stage_stores.store_id,stage_stores.store_name
                       FROM filtered_sales
                       JOIN stage_product
                       ON filtered_sales.product_id = stage_product.product_id
                       JOIN stage_stores
                       ON stage_stores.store_id = filtered_sales.store_id"""
            df = pd.read_sql(query,mysql_conn)
            df.to_sql("monthly_sales_summary_source",mysql_conn,index=False)
            logger.info("Joiner transformation completed for sales data")

        except Exception as e:
            logger.error(f"Error encountered while data extraction of joiner sales data,{e},exc_info=True")


    def transform_aggregrator_inventory_level(self):
        logger.info("Aggregrator transformation has started for inventory data")
        try:
            query = """select store_id, sum(quantity_on_hand) as total_inventory from stage_inventory group by store_id"""
            df = pd.read_sql(query,mysql_conn)
            df.to_sql("aggregrated_inventory_level",mysql_conn,index=False)
            logger.info("Aggregrator transformation completed for inventory data")

        except Exception as e:
            logger.error(f"Error encountered while data extraction of aggregrator inventory data,{e},exc_info=True")


if __name__ == "__main__":
    de = DataTransformation()    
    de.transform_filtered_sales_data()
    de.transform_router_sales_data_high_region()
    de.transform_router_sales_data_low_region()
    de.transform_joiner_sales_product_stores()
    de.transform_aggregrator_inventory_level()
    de.transform_aggregator_sales_data()