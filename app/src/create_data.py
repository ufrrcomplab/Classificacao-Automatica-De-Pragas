'''
  Este Codigo tem como objetivo de criar de uma unica base de dados servendo como dado de validação:

* Primeiro é coletado as imagens por pastas
* A cada imagens em uma pasta é extraida as caracteristica da forma(Hu moments),
  da textura(Haralick) e da cor(color histogram )
* É armazenado em uma array os dados separado por dados e attributo
* Logo todas as imagens colocadas em uma array é criada a codificação h5py para criar a Base de Dado.
* Basta separar por pasta toda as imagens que deseja testar e rodar o algoritmo é já está feita.

'''


import os
import cv2
import h5py
import random
import mahotas
import numpy as np
from skimage import img_as_float32
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from sklearn.model_selection import StratifiedShuffleSplit


# DEFININDO AS VARIAVEIS GLOBAIS
path = "VALIDACAO"
attributes = ["Image"]



class ImageProcessing(BaseEstimator, TransformerMixin):

    def __init__(self, path, attributes):
        '''
            * Path : Caminho até as pastas das imagens
            * Attributes : São os nomes das pastas contendo as Diferentes imagens
        '''
        self.path = path
        self.attributes = attributes
        self.dataset_X = []
        self.dataset_y = []
        self.bins = 8

    def fit(seft, *_):
        return self

    def get_files(self, attribute):
        files = sorted([os.path.join(self.path, attribute, file)
                        for file in os.listdir(self.path + "/"+attribute)
                        if file.endswith('.jpg')])
        random.shuffle(files)
        return files

    # feature-descriptor-1: Hu Moments
    def fd_hu_moments(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        feature = cv2.HuMoments(cv2.moments(image)).flatten()
        return feature

    # feature-descriptor-2: Haralick Texture
    def fd_haralick(self, image):
        # convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # compute the haralick texture feature vector
        haralick = mahotas.features.haralick(image).mean(axis=0)
        # return the result
        return haralick

    # feature-descriptor-3: Color Histogram
    def fd_histogram(self, image, mask=None):
        # convert the image to HSV color-space
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # compute the color histogram
        hist = cv2.calcHist([image], [0, 1, 2], None, [
                            self.bins, self.bins, self.bins], [0, 256, 0, 256, 0, 256])
        # normalize the histogram
        cv2.normalize(hist, hist)
        # return the histogram
        return hist.flatten()

    def load_image(self, item):
        '''
            * Carregar a imagem
            * Redimencionar a imagem tendo como valor maxímo do pixel 255.
        '''

        image = cv2.imread(item)
        gray = cv2.resize(image, (255, 255), interpolation=cv2.INTER_LINEAR)

        return gray

    def make_sets(self, *_):
        for attribute in self.attributes:

            data = self.get_files(attribute)

            for item in data:
                image = self.load_image(item)
                ####################################
                # Global Feature extraction
                ####################################
                fv_hu_moments = self.fd_hu_moments(image)
                fv_haralick = self.fd_haralick(image)
                fv_histogram = self.fd_histogram(image)

                ###################################
                # Concatenate global features
                ###################################
                global_feature = np.hstack(
                    [fv_histogram, fv_haralick, fv_hu_moments])

                self.dataset_X.append(global_feature)
                self.dataset_y.append(attributes.index(attribute))

        self.dataset_X = np.array(self.dataset_X)
        self.dataset_y = np.array(self.dataset_y)

    def save_h5(self, h5_filename, data, label, data_dtype='float64', label_dtype='int64'):

        if os.path.isfile(h5_filename):
            raise ValueError("O arquivo '{}' já existe e não pode "
                             "ser apagado.".format(h5_filename))

        h5_fout = h5py.File(h5_filename)
        h5_fout.create_dataset(
            'data', data=data, compression='gzip', compression_opts=4, dtype=data_dtype)
        h5_fout.create_dataset(
            'label', data=label, compression='gzip', compression_opts=1, dtype=label_dtype)
        h5_fout.close()

    def transform(self, Name=""):
        self.make_sets()
        # MUDANDO O ENDEREÇO PATH DO SISTEMA PARA SALVAR OS ARQUIVOS
        try:
            os.chdir(os.getcwd()+"/"+self.path)
            print("Directory changed to ", os.getcwd())
        except OSError:
            print("Can't change the current working Directory")

        self.save_h5(Name, self.dataset_X, self.dataset_y)
        print("Sucesso. Acessar os arquivos na pasta.")


def create_validation():
    # SETANDO OS PARAMETROS NO ALGORITMO
    MakeDataSet = ImageProcessing(path, attributes)
    
    _ = MakeDataSet.transform("Validacao")
    # EXECUTANDO O ALGORITMO

if __name__ == "__main__":
    create_validation()