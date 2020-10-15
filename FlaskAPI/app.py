import flask
from flask import Flask, jsonify, request
import json
import pickle
import numpy as np
import pandas as pd
from data_prep import *

app = Flask(__name__)

def load_model_logwage():
    file_name = "models/model_logwage.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

def load_model_positions():
    file_name = "models/model_positions.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

@app.route('/predict', methods=['GET'])
def predict():
    # parse input features from request
    request_json = request.get_json()
    X_df = prepare_data_for_prediction(request_json['input'])

    # load model
    model = load_model_logwage()
    columns = model.get_booster().feature_names
    X_df = X_df[columns]
    wage_prediction = np.expm1(model.predict(X_df))[0]

    # Just giving a more round value to the user
    wage_prediction = int(round(wage_prediction,2 - len(str(int(wage_prediction)))))

    if X_df.loc[0,'GK'] == 1:
        positions_prediction = 'GK'
    else:
        X_df = get_features_predictions_positions(X_df)
        model = load_model_positions()
        probas = model.predict_proba(X_df)
        predicted_probas = []
        for i in range(14):
            predicted_probas = predicted_probas + [int(round(probas[i][0,1],2)*100)]

        positions = ['RW', 'ST', 'CF', 'LW', 'CAM', 'CB', 'CM', 'CDM', 'LM', 'RB', 'RM', 'LB', 'LWB', 'RWB']
        pos_preds_series = pd.Series(data=predicted_probas,index=positions).sort_values(ascending=False)
        indexes = pos_preds_series[pos_preds_series>25].index
        positions_prediction = ''

        for i in range(len(indexes)):
            positions_prediction = positions_prediction + indexes[i] +', '

        positions_prediction = positions_prediction[:-2]
    response = json.dumps({'Predicted wage (EUR)': str(wage_prediction), 'Best positions': positions_prediction})
    return response, 200

if __name__ == '__main__':
    application.run(debug=True)
