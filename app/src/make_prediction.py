import os
import h5py
import json
import joblib
import xgboost
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


class load_reshape(BaseEstimator, TransformerMixin):

    def __init__(self, Validation=""):
        self.ValidationFileName = Validation
        self.X_val = []
        self.y_val = []

    def fit(self, *_):
        return self

    def transform(self, *_):
        T = h5py.File(self.ValidationFileName)
        self.X_val = T['data'][:]
        self.y_val = T['label'][:]
        return self.X_val, self.y_val


class Analyzation(BaseEstimator, TransformerMixin):
    def __init__(self, attributes, Prediction=True, Estimator_Score=True, MatrizConfusion=True,
                 accuracy=True, Class_Report=True):
        self.attributes = attributes
        self.Pred = Prediction
        self.Sc = Estimator_Score
        self.Ma = MatrizConfusion
        self.Ac = accuracy
        self.CP = Class_Report

    def fit(self, *_):
        return self

    def transform(self, path, task, Prediction, Estimator_Score, MatrizConfusion, accuracy, Class_Report):

        # MUDANDO O ENDEREÇO PATH DO SISTEMA PARA SALVAR AS INFORMAÇÃO DO TEST
        try:
            os.chdir(path+"/VALIDACAO/Resultado")
            print("Directory changed to ", os.getcwd())
        except OSError:
            print("Can't change the current working Directory")
        


        data = {
            'prediction': '{}'.format(y_Validation_pred),
            'Validation_Score': Estimator_Score,
            'Validation_Acuracy': (accuracy.mean()*100),
            'Validation_Classification Report': Class_Report
        }

        with open("%s1.json" %task, 'w') as jsonfile:
            json.dump(data, jsonfile)

        if(self.Ma):
            #print('\033[1m Matriz de confusao:\n\n')
            sns.set()
            fig = plt.figure()
            fig, ax = plt.subplots(1, 2, figsize=(24, 12))
            # plt.figure(figsize=16)
            #fig, ax = plt.subplots(1,2)
            sns.heatmap(pd.DataFrame(MatrizConfusion, columns=self.attributes, index=self.attributes),
                        annot=True,
                        fmt='g',
                        cmap=sns.cubehelix_palette(8, start=.7, rot=-.75),
                        ax=ax[0])
            plt.xlabel('predicted value')
            plt.ylabel('true value')
            #print('\033[1m Matriz de Analise de Erros:\n\n')
            row_sums = MatrizConfusion.sum(axis=1)
            norm_conf_mx = MatrizConfusion / row_sums
            np.fill_diagonal(norm_conf_mx, 0)
            sns.heatmap(pd.DataFrame(norm_conf_mx, columns=self.attributes, index=self.attributes),
                        cmap=plt.cm.gray, ax=ax[1])
            plt.xlabel('predicted value')
            plt.ylabel('true value')
            plt.savefig('%s.pdf' %task)


if __name__ == "__main__":
    # PATH DE BASE
    path = os.getcwd()

    # MUDANDO O ENDEREÇO PATH DO SISTEMA PARA SALVAR O MODELO PREDITIVO
    try:
        os.chdir(path + "/VALIDACAO")
        print("Directory changed to ", os.getcwd())
    except OSError:
        print("Can't change the current working Directory")

    # Definindo os labels da pasta das imagens
    attributes = ["BLISSUS", "CIGARRINHA", "Image"]

    # Carregar na memoria os DataSet
    Dados = load_reshape("Validacao")

    # Iniciar o carregamento dos dados de Treinamento e de Test
    X_val, y_val = Dados.transform()

    # MUDANDO O ENDEREÇO PATH DO SISTEMA PARA SALVAR O MODELO PREDITIVO
    try:
        os.chdir(path)
        print("Directory changed to ", os.getcwd())
    except OSError:
        print("Can't change the current working Directory")


    # CARREGAR O MODELO PREDITIVO
    XG = joblib.load("XGBoostModel.pkl")

    y_Validation_pred = XG.predict(X_val)
    Validation_score = XG.score(X_val, y_Validation_pred)
    Validation_matriz_conf = confusion_matrix(y_val, y_Validation_pred, labels=[
                                            i for i in range(len(attributes))])
    Validation_accuracy = accuracy_score(y_Validation_pred, y_val)
    Validation_Classification_Report = classification_report(
        y_val, y_Validation_pred)

    # Setando os parametros de resultados ser Analizado
    Validation_analise = Analyzation(attributes)

    # Imprimir na tela os resultados no intuito de AnaliseS
    Validation_analise.transform(path=path, task="XG_Validation", Prediction=y_Validation_pred, Estimator_Score=Validation_score,
                                MatrizConfusion=Validation_matriz_conf, accuracy=Validation_accuracy,
                                Class_Report=Validation_Classification_Report)

    print('Validation completa \n')
