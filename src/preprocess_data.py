import joblib
import pandas as pd

label_encoder = joblib.load("models/label_encoder.joblib")
def preprocess_input_data(input_df):
    input_df['Country'] = label_encoder.transform(input_df['Country'])
    return input_df

