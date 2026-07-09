import pandas as pd
from sqlalchemy import create_engine
import oracledb

# DB Connection
oracledb_conn = create_engine(
    "oracle+oracledb://SYSTEM:admin@localhost:1521/XE"
)

print(pd.read_sql("""SELECT * FROM STORES""",oracledb_conn))