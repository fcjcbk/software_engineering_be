import mysql.connector
import yaml
import time
import sys
from pydantic import BaseModel
from logger import get_logger

logger =  get_logger(__name__)

def connect_to_mysql(config, attempts=3, delay=2):
    attempt = 1
    # Implement a reconnection routine
    while attempt < attempts + 1:
        try:
            return mysql.connector.connect(**config)
        except (mysql.connector.Error, IOError) as err:
            if attempts == attempt:
                # Attempts to reconnect failed; returning None
                logger.info("Failed to connect, exiting without a connection: %s", err)
                return None
            logger.info(
                "Connection failed: %s. Retrying (%d/%d)...",
                err,
                attempt,
                attempts-1,
            )
            # progressive reconnect delay
            time.sleep(delay ** attempt)
            attempt += 1
    return None

try:
    with open('../config/server.yaml', 'r', encoding="UTF-8") as file:
        cfg = yaml.safe_load(file)
        cnx = mysql.connector.connect(**cfg['mysql'])

except IOError:
    logger.error("can not open config file")
    sys.exit(1)

database_connection =  cnx

# cnx = mysql.connector.connect(**config['mysql'])

# cnx.close()

# class emp(BaseModel):
#     empno: int
#     ename: str

# cnx = connect_to_mysql(cfg['mysql'])
# lt: list[emp] = []
# if cnx is not None:
#     query: str = "SELECT empno, ename FROM emp"
#     cursor = cnx.cursor()
#     cursor.execute(query)
#     for a in cursor:
#         # print("{}, {}".format(empno, ename))
#         lt.append(emp(int(empno=a[0]), ename=a[1]))
#         # print("{}".format(emp(a)))
#     print(lt)
#     cnx.close()
