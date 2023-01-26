import pymongo
import numpy as np
import pandas as pd
import json
import os
import sys
from dataclasses import dataclass

@dataclass
class EnvironmentVariable:
    mongo_db_url = os.getenv("MONGO_DB_URL")
    
    
env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = "expenses"
print(env_var.mongo_db_url)