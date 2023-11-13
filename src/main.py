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

#predicting words
from keras.preprocessing.sequence import pad_sequences

input_text = input().strip().lower()
encoded_text = tokenizer.texts_to_sequences([input_text])[0]
pad_encoded = pad_sequences([encoded_text], maxlen=seq_len, truncating='pre')
print(encoded_text, pad_encoded)

for i in (model.predict(pad_encoded)[0]).argsort()[-3:][::-1]:
    pred_word=tokenizer.index_word[i]
    print("Next word suggestion:", pred_word)