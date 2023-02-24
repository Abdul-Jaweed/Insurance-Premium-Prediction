from insurance.entity import config_entity, artifact_entity
from insurance.exception import InsuranceException
from typing import Optional
import os
import sys
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from insurance import utils
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from insurance.predictor import ModelResolver
from insurance.logger import logging
from insurance.utils import load_object, save_object
from insurance.config import TARGET_COLUMN
from insurance.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,ModelPusherArtifact
from insurance.entity.config_entity import ModelPusherConfig
from insurance.predictor import ModelResolver

from insurance.predictor import ModelResolver
from insurance.entity.config_entity import ModelPusherConfig
from insurance.exception import InsuranceException
import os,sys
from insurance.utils import load_object,save_object
from insurance.logger import logging
from insurance.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,ModelPusherArtifact




class ModelPusher:
    
    def __init__(self,model_pusher_config:ModelPusherConfig,
    data_transformation_artifact:DataTransformationArtifact,
    model_trainer_artifact:ModelTrainerArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.model_pusher_config=model_pusher_config
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)
        except Exception as e:
            raise InsuranceException(e, sys)
        
        
        
    def initiate_model_pusher(self)->ModelPusherArtifact:
            
            try:
                
                # model and target encoder data
                
                logging.info(f"Loading transformer model and target encoder")
                transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
                model = load_object(file_path=self.model_trainer_artifact.model_path)
                target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)
                
                
                # model pushing and saving into model_pusher dir
                
                # model pusher
                
                logging.info(f"Saving model into model pusher directory")
                save_object(file_path=self.model_pusher_config.pusher_transformer_path, obj=transformer)
                save_object(file_path=self.model_pusher_config.pusher_model_path, obj=model)
                save_object(file_path=self.model_pusher_config.pusher_target_encoder_path, obj=target_encoder)
                
   
                # saved model dir
                
                logging.info(f"Saving model in saved model dir")
                transformer_path=self.model_resolver.get_latest_save_transfomer_path()
                model_path=self.model_resolver.get_latest_save_model_path()
                target_encoder_path=self.model_resolver.get_latest_save_target_encoder_path()


                save_object(file_path=transformer_path, obj=transformer)
                save_object(file_path=model_path, obj=model)
                save_object(file_path=target_encoder_path, obj=target_encoder)


                model_pusher_artifact = ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir,
                saved_model_dir=self.model_pusher_config.saved_model_dir)
                logging.info(f"Model pusher artifact: {model_pusher_artifact}")
                
                return model_pusher_artifact
                
           
            except Exception as e:
                raise InsuranceException(e, sys)

