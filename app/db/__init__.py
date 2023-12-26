import mysql.connector
import yaml
import time
import sys
from pydantic import BaseModel
from app.logger import get_logger

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
    with open('config/server.yaml', 'r', encoding="UTF-8") as file:
        cfg = yaml.safe_load(file)
        cnx = mysql.connector.connect(**cfg['mysql'])

except IOError:
    logger.error("can not open config file")
    sys.exit(1)

database_connection =  cnx

def close():
    database_connection.close()
    logger.info("database connection closed")
