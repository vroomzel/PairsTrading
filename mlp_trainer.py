import class_ForecastingTrader
import numpy as np
np.random.seed(1) # NumPy
import random
random.seed(3) # Python
import tensorflow as tf
tf.set_random_seed(2) # Tensorflow
session_conf = tf.ConfigProto(intra_op_parallelism_threads=1,
                              inter_op_parallelism_threads=1)
from keras import backend as K
sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)
K.set_session(sess)

import pandas as pd
import pickle
import time
import sys

forecasting_trader = class_ForecastingTrader.ForecastingTrader()

################################# READ PRICES AND PAIRS #################################
# read prices
df_prices = pd.read_pickle('../data/etfs/pickle/commodity_ETFs_intraday_interpolated_screened_no_outliers')
# split data in training and test
df_prices_train, df_prices_test = data_processor.split_data(df_prices,
                                                            ('01-01-2009',
                                                             '31-12-2017'),
                                                            ('01-01-2018',
                                                             '31-12-2018'),
                                                            remove_nan=True)
# load pairs
with open('data/etfs/pickle/pairs_unsupervised_learning_intraday.pickle', 'rb') as handle:
    pairs = pickle.load(handle)
n_years_train = round(len(df_prices_train) / (240 * 78))

################################# TRAIN MODELS #################################

n_in_set = [3, 5, 7, 10]
hidden_nodes_set = [[3], [5], [7], [10], [3, 3], [5, 5], [7,7], [10, 10]]
hidden_nodes_names = [str(nodes[0])+'*2_' if len(nodes) > 1 else str(nodes[0])+'_' for nodes in hidden_nodes_set]

for input_dim in n_in_set:
    for i, hidden_nodes in enumerate(hidden_nodes_set):
        model_config = {"n_in": input_dim,
                        "n_out": 1,
                        "epochs": 2,#250,
                        "hidden_nodes": hidden_nodes,
                        "loss_fct": "mse",
                        "optimizer": "adam",
                        "train_val_split": '2017-01-01'}
        models = forecasting_trader.train_models(pairs, model_config)
        # save models for this confguration
        with open('models_n_in-'+str(input_dim)+'_hidden_nodes-'+hidden_nodes_names[i]+'.pkl', 'wb') as f:
            pickle.dump(models, f)