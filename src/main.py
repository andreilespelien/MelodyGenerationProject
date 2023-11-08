from keras.preprocessing.text import Tokenizer
import nltk
from nltk.tokenize import word_tokenize
import numpy as np
import re
from keras.utils import to_categorical



#model build
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding
from tensorflow import keras

model = keras.models.load_model('mymodel.h5')
# model = Sequential()
# model.add(Embedding(vocabulary_size, seq_len, input_length = seq_len))
# model.add(LSTM(50, return_sequences=True))
# model.add(LSTM(50))
# model.add(Dense(50, activation='relu'))
# model.add(Dense(vocabulary_size, activation='softmax'))
print(model.summary())

#compiling the network
# model.compile(loss='categorical_crossentropy', optimizer ='adam', metrics=['accuracy'])
# model.fit(train_inputs, train_targets, epochs=500,verbose=1)
# model.save("mymodel.h5")
