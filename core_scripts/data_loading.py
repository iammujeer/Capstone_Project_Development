import methodtools
import pandas as pd
from sqlalchemy import create_engine, text
import logging

# Logging configuration
from common_utilities.utilities import read_file_and_write_to_database
from project_config.etlconfig import *

logging.basicConfig(
    filename="application_logs/etljob.log",
    filemode='w',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO )
logger = logging.getLogger(__name__)

#DB Conn
oracledb_conn = create_engine(
    f"oracle+oracledb://{oracle_user}:{oracle_pwd}@{oracle_localhost}:{oracle_port}/{oracle_service}"
)

mysql_conn =  create_engine(
    f"mysql+pymysql://{mysql_user}:{mysql_pwd}@{mysql_localhost}:{mysql_port}/{mysql_database}"
)

class DataLoading:

    def load_load_fact_sales_table(self):
        logger.info("Data Loading in fact_sales started...")

        query = text("""insert into fact_sales(sales_id,product_id,store_id,quantity,total_sales,sale_date) 
                    select sales_id,product_id,store_id,quantity,sales_amount,sale_date from sales_with_details""")
        with mysql_conn.connect() as conn:
            logger.info(query)
            conn.execute(query)
            conn.commit()
        logger.info("Data Loading in fact_sales completed...")

    def load_load_fact_inventory_table(self):
        logger.info("Data Loading in fact_inventory started...")

        query = text("""insert into fact_inventory(product_id,store_id,quantity_on_hand,last_updated) 
            select product_id,store_id,quantity_on_hand,last_updated from stage_inventory""")
        with mysql_conn.connect() as conn:
            logger.info(query)
            conn.execute(query)
            conn.commit()
        logger.info("Data Loading in fact_inventory completed...")

    def load_monthly_sales_summary_table(self):
        logger.info("Data Loading in monthly_sales_summary started...")

        query = text("""insert into monthly_sales_summary(product_id,year,month,total_sales ) 
                        select product_id,year,month,total_sales from monthly_sales_summary_source""")
        with mysql_conn.connect() as conn:
            logger.info(query)
            conn.execute(query)
            conn.commit()
        logger.info("Data Loading in monthly_sales_summary completed...")


    def load_inventory_level_bys_stores_table(self):
        logger.info("Data Loading in inventory_level_bys_stores started...")

        query = text("""insert into inventory_levels_by_store(store_id,total_inventory) 
                        select store_id,total_inventory from aggregrated_inventory_level""")
        with mysql_conn.connect() as conn:
            logger.info(query)
            conn.execute(query)
            conn.commit()
        logger.info("Data Loading in inventory_level_bys_stores completed...")


if __name__ == "__main__":
    dl = DataLoading()
    dl.load_load_fact_sales_table()
    dl.load_load_fact_inventory_table()
    dl.load_monthly_sales_summary_table()
    dl.load_inventory_level_bys_stores_table()