# import all the libraries needed
import numpy as np
import pandas as pd
import pickle
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler


# Class used for new data predictions
class Evaluation_model():
    def __init__(self,path):
        # read the model and scaler
        # Load the model and preprocessing components from the pickle file

        with open(path, 'rb') as file:
            self.loaded_model_dict = pickle.load(file)
            self.data = None

    def get_preprocessed_data(self,data, scaler, dummies_columns):
        # Drop the 'Nº' column
        data = data.drop(['Nº'], axis=1)

        # Apply log transformation to 'Nº WC's'
        data["Nº WC's"] = np.log(data["Nº WC's"] + 0.001)

        # Identify categorical columns
        cols = []

        for col in data.columns:
            if data[col].dtype == 'O':
                if data[col].unique().shape[0]==2:
                    data[col] = data[col].map({data[col].unique()[0]: 0, data[col].unique()[1]: 1})
                else:
                    cols.append(col)

        # Apply get_dummies to categorical columns
        data_encoded = pd.get_dummies(data, columns=cols, drop_first=True)

        # Ensure the data has the same columns as the training data
        for col in dummies_columns:
            if col not in data_encoded.columns:
                data_encoded[col] = 0

        # Align the order of columns
        data_encoded = data_encoded[dummies_columns]
        data_encoded = data_encoded.drop(['Cluster','Finalidade', 'Preço (MZN)'], axis=1, errors='ignore')

        # Scale numeric features
        numeric_features = ["Nº WC's"]
        data_encoded[numeric_features] = scaler.transform(data_encoded[numeric_features])

        return data_encoded

    def get_prediction(self,data):

        # Extract components
        loaded_scaler = self.loaded_model_dict['scaler']
        loaded_kmeans = self.loaded_model_dict['kmeans']
        loaded_cluster_means_dict = self.loaded_model_dict['cluster_means_dict']
        loaded_finalidade_segments = self.loaded_model_dict['finalidade_segments']
        loaded_dummies_columns = self.loaded_model_dict['dummies_columns']

        # Preprocess the input sample
        input_sample_preprocessed = self.get_preprocessed_data(data, loaded_scaler, loaded_dummies_columns)

        input_finalidade=0
        # Predict the cluster for the input sample
        if data['Finalidade'].values[0]=='V':
            input_finalidade = 1

        input_cluster = loaded_kmeans.predict(input_sample_preprocessed)

        # Predict the price using the mean price for the assigned cluster
        predicted_price = "{:.2f}".format(np.exp(loaded_cluster_means_dict[input_finalidade][input_cluster[0]]) - 0.001)

        return predicted_price, input_cluster[0]

# input_sample = pd.DataFrame([{
#     'Nº': 1, 'Design': 'Flat', 'Finalidade': 'A', 'Bairro': 'Alto-Maé', 'Tipologia': 'T2', 'Moveis': 'S',
#     'Guarda-Fatos': 'C', 'Ar-Condicionado': 'C', 'Garagem': 'S', 'Cozinha Americana': 'C',
#     'Nº WC\'s': 1, 'Suite': 'S', 'Vista': 'S', 'Piscina': 'S', 'Obras': 'S'
# }])

# path = '/content/drive/MyDrive/Documentos/Trabalho de Licenciatura/Evaluation Model Files/house_evaluation_model.pkl'

# eval_model = Evaluation_model(path)
# predicted_price = eval_model.get_prediction(input_sample)

# print(f"Predicted Price: {predicted_price} MZN")

