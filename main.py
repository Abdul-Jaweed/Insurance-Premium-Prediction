from insurance.logger import logging
from insurance.exception import InsuranceException
import os 
import sys
from insurance.utils import get_collection_as_dataframe
from insurance.entity.config_entity import DataIngestionConfig
from insurance.entity import config_entity
from insurance.components.data_ingestion import DataIngestion
from insurance.components.data_validation import DataValidation
from insurance.components.data_transformation import DataTransformation
from insurance.components.model_trainer import ModelTrainer
from insurance.components.model_evaluation import ModelEvaluation
from insurance.components.model_pusher import ModelPusher




# def test_logger_and_exception():
#     try:
#         logging.info("Starting the test_logger_and_exception")
#         result = 3 / 0
#         print(result)
#         logging.info("Ending point of the test_logger_and_exception")
#     except Exception as e:
#         logging.debug(str(e))
#         raise InsuranceException(e, sys)
    
if __name__ == "__main__":
    try:
        # start_training_pipeline()
        # test_logger_and_exception()
        # get_collection_as_dataframe(database_name = "INSURANCE", collection_name = "INSURANCE_PROJECT")
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        
        # data ingestion
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config = training_pipeline_config)
        print(data_ingestion_config.to_dict())
        
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        
        #Data Validation
        
        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config = data_validation_config,
                                         data_ingestion_artifact = data_ingestion_artifact)
        
        data_validation_artifact = data_validation.initiate_data_validation()
        
        
        
        # Data Transformation
        
        data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config, data_ingestion_artifact=data_ingestion_artifact)
        
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        
        
        # Model Trainer
        
        model_trainer_config = config_entity.ModelTrainingConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        
        
        # Model Evaluation
        
        model_eval_config = config_entity.ModelTrainingConfig(training_pipeline_config=training_pipeline_config)
        model_eval = ModelEvaluation(model_eval_config=model_eval_config,
        data_ingestion_artifact=data_ingestion_artifact,
        data_transformation_artifact=data_transformation_artifact,
        model_trainer_artifact=model_trainer_artifact)
        #model_eval_artifact = model_eval.intitate_model_evaluation()
        model_eval_artifact = model_eval.initiate_model_evaluation()
        
        
        # Model Pusher
        
        model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config=training_pipeline_config)
        model_pusher = ModelPusher(model_pusher_config=model_pusher_config, 
                                   data_transformation_artifact=data_transformation_artifact, 
                                   model_trainer_artifact=model_trainer_artifact)
        
        Model_pusher_artifact = model_pusher.initiate_model_pusher()
                                     
                                     
    except Exception as e:
        print(e)

