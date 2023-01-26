import numpy as np
import pandas as pd
import yaml
import dill
import os
import sys
from insurance.exception import InsuranceException
from insurance.config import mongo_client
from insurance.logger import logging


def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    try:
        logging.info(f"Reading data from database:{database_name} and collection_name:{collection_name}")
        df = pd.DataFrame(mongo_client[database_name][collection_name].find())
        logging.info(f"Find columns:{df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping columns: _id")
            df = df.drop("_id", axis=1)
        logging.info(f"Rows and Columns  in df:{df.shape}")
        return df
        
    except Exception as e:
        raise InsuranceException(e, sys)