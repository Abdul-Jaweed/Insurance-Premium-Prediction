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
from insurance.utils import load_object
from insurance.config import TARGET_COLUMN





class ModelEvaluation:
    
    def __init__(self,
                 model_eval_config: config_entity.ModelEvaluationConfig,
                 data_ingestion_artifact: artifact_entity.DataIngestionArtifact,
                 data_transformation_artifact: artifact_entity.DataTransformationArtifact,
                 model_trainer_artifact: artifact_entity.ModelTrainerArtifact):
        
        
        try:
            
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()

        except Exception as e:
            raise InsuranceException(e, sys)
    
  
    def intitate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        
        try:
            
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            
            if latest_dir_path == None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=None)
                
                logging.info(f"MOdel evaluation artifact : {model_eval_artifact}")
                
                return model_eval_artifact
            
            
            
            
            # find location previous model 
            
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()
            
            
            
            # previous model
            
            transformer = load_object(file_path = transformer_path)
            model = load_object(file_path = model_path)
            target_encoder = load_object(file_path = target_encoder_path)
            
       
       
            # new model
            
            current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model = load_object(file_path=self.model_trainer_artifact.model_path)
            curent_target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)
        
            # load data from test
            
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df = test_df[TARGET_COLUMN]
            y_true = target_df
            
            
            
            # transform categorical and predict
            
            input_features_name = list(transformer.feature_names_in_)
            for i in input_features_name:
                if test_df[i].dtypes=='object':
                    test_df[i] = target_encoder.fit_transform(test_df[i])
            
            input_arr = transformer.transform(test_df[input_features_name])
            y_pred = model.predict(input_arr)
            
            
            
            # comparision between new model and old model
            
            previous_model_score = r2_score(y_true=y_true, y_pred=y_pred)
            
            
            
            # Accuracy current model 
            
            input_feature_name = list(current_transformer.feature_names_in_)
            input_arr = current_transformer.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)
            y_true = targer_df
            
            
            current_model_score = r2_score(y_true=y_true, y_pred=y_pred)
            
            
            # Final comparison between both model
            
            if current_model_score <= previous_model_score:
                logging.info(f"Current trained model is not better than previous model")
                raise Exception("Current model is not better than previous trained model")
            
            
            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted =  True, improved_accuracy=current_model_score - previous_model_score)
            
            return model_eval_artifact
        
        except Exception as e:
            raise InsuranceException(e, sys)
        




# TO STORE MODEL
#     Cloud (AWS -> s3 bucket)
#     Database -> model pusher
#     local system -> saved_models


