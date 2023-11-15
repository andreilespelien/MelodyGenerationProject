from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding
from tensorflow import keras

from MIDIParsing import MIDIParser
import numpy as np

parser = MIDIParser("maestro-v2.0.0") # "dataTemp" or "maestro-v2.0.0"
print("Read")

seqlen = 3
sequences, vocab = parser.returnData(seqlen)
vocab += 1 # 971 for dataTemp and 530250 for maestro

sequencesnp = np.empty([len(sequences), seqlen], dtype='int32')
for i in range(len(sequences)):
    sequencesnp[i] = sequences[i]
print("Parsed")

tts_ratio = 0.75
train_inputs = sequencesnp[:,:-1]
train_targets = sequencesnp[:,-1]
train_targets = to_categorical(train_targets, num_classes = vocab) # 971 or 530250
# print(sequencesnp[0])
# print(train_inputs[0])
# print(train_targets[0])

# # model = keras.models.load_model('mymodel.h5')
model = Sequential()
model.add(Embedding(vocab, 2, input_length = 2)) # 971 or 530250
model.add(LSTM(50, return_sequences=True))
model.add(LSTM(50))
model.add(Dense(50, activation='relu'))
model.add(Dense(vocab, activation='softmax')) # 971 or 530250
# # print(model.summary())

# #compiling the network
model.compile(loss='categorical_crossentropy', optimizer ='adam', metrics=['accuracy'])
model.fit(train_inputs, train_targets, epochs=500, verbose=1)
model.save("mymodel.h5")

# #predicting words
# # from keras.preprocessing.sequence import pad_sequences

# # input_text = input().strip().lower()
# # encoded_text = tokenizer.texts_to_sequences([input_text])[0]
# # pad_encoded = pad_sequences([encoded_text], maxlen=seq_len, truncating='pre')
# # print(encoded_text, pad_encoded)

# # for i in (model.predict(pad_encoded)[0]).argsort()[-3:][::-1]:
# #     pred_word=tokenizer.index_word[i]
# #     print("Next word suggestion:", pred_word)