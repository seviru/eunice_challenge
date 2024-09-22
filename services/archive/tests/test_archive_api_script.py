import sys
import os
import random
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from logger import logger


endpoints = [
    "http://localhost:8080/api/articles",
    f"http://localhost:8080/api/articles/{random.randint(1, 20)}",
]

for endpoint in endpoints:
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        logger.info(
            "Request to endpoint was successful",
            extra={
                "endpoint": endpoint,
                "response": response.json()
            }
        )
    except requests.HTTPError as err:
        logger.error(
            "Request to endpoint returned error",
            extra={
                "endpoint": endpoint,
                "error": str(err)
            }
        )
    except Exception as err:
        logger.error(
            f"An error occurred while making the request to {endpoint}: {err}",
            extra={
                "endpoint": endpoint,
                "error": str(err)
            }
        )
