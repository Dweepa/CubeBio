import tensorflow as tf
import pickle
import sys
import matplotlib.pyplot as plt1
import numpy as np
from IPython.display import Audio, display
import time
from sklearn.model_selection import train_test_split
import random
from network import *
from data import *
import os

# TODO:
'''
- loss = cosine, problem with euclidean
- net = Vanilla/Denset
- layers: number of layers
- neurons: number of neurons per layer
- embedding length: 8, 16, 32
- epoch: 50, 75, 100, 200
- (densenet param: subject to results)
- samples per perturbagen: 50, 100, 200

sys arguments: layer neuron emb_len dropout samples_per_pert 
'''

layer = int(sys.argv[1])
neuron = int(sys.argv[2])
emb_len = int(sys.argv[3])
dropout = int(sys.argv[4])
samples_per_pert = int(sys.argv[5])

print(layer, neuron, emb_len, dropout, samples_per_pert)
model_name = "MOD_triplet_" + str(layer) + "_" + str(neuron) + "_" + str(emb_len) + "_" + str(samples_per_pert)
embedding_name = "EMB_triplet_" + str(layer) + "_" + str(neuron) + "_" + str(emb_len) + "_" + str(samples_per_pert)
if (os.path.exists('../../Models/' + model_name) == 0):
    os.mkdir('../../Models/' + model_name)

# X = pickle.load(open('../../Data/X_train_triplet_full', 'rb'))
# test = pickle.load(open('../../Data/X_test_triplet_full', 'rb'))
full = pickle.load(open('../../Data/full', 'rb'))
dbfile = open('../../Data/test_perts', 'rb')
test_pert = pickle.load(dbfile)
dbfile = open('../../Data/train_perts', 'rb')
train_pert = pickle.load(dbfile)
dbfile.close()

# List of all perturbagens
all_pert = np.concatenate((train_pert, test_pert))
# print("total perts: ",len(all_pert))

# Testing on unseen perturbagens
epoch = 200
s = siamese("cos", "net", layer, neuron, emb_len, dropout)
print("= Created Model")
X, test = get_data(full, all_pert, samples_per_pert)
# X, test = get_data(full, all_pert[0:30], 2)
print("== Got Data")
full_dataset_embeddings, embeddings, trained, pred, p_loss, n_loss, train_acc_l, test_acc_l = \
    run_network(model_name, embedding_name, s, epoch, X, test, full)

print("===== Results")
print("Testing on unseen perturbagens: Cosine distance")
p = np.sum(trained[0][2] <= 0.5)
n = np.sum(trained[0][3] > 0.5)
print("Training Accuracy", (p + n) / len(X[0]) / 2)

p = np.sum(pred[0][2] <= 0.5)
n = np.sum(pred[0][3] > 0.5)
print("Testing Accuracy", (p + n) / len(test[0]) / 2)
