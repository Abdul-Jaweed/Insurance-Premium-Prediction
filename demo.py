# batch prediction
# training pipeline

from insurance.pipeline.batch_prediction import start_batch_prediction
from insurance.pipeline.training_pipeline import start_training_pipeline

file_path=r"F:\Insurance Premium Prediction\Insurance-Premium-Prediction\insurance.csv"
# print(__name__)
if __name__=="__main__":
    try:
        output = start_training_pipeline()
        output_file = start_batch_prediction(input_file_path=file_path)
        #print(output_file)
    except Exception as e:
        print(e)