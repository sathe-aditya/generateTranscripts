import numpy
import os
import tflearn
import pickle
from tflearn.data_utils import *

path = 'Eps 1.1 - 1.12.txt'
pickleFilePath = 'char_idx_speech_HIMYM.p'
maxlen = 100
LR = 1e-3
char_idx = None

# if os.path.isfile(pickleFilePath):
	# char_idx = pickle.load(open(pickleFilePath,'r'))

X, Y, char_idx = textfile_to_semi_redundant_sequences(path, seq_maxlen=maxlen, redun_step=3, pre_defined_char_idx=char_idx)

pickle.dump(char_idx, open(pickleFilePath, 'w'))

model = tflearn.input_data([None, maxlen, len(char_idx)])
model = tflearn.lstm(model, 128, return_seq=True)
model = tflearn.dropout(model, 0.5)
# model = tflearn.lstm(model, 128, return_seq=True)
# model = tflearn.dropout(model, 0.5)
model = tflearn.lstm(model, 128)
model = tflearn.dropout(model, 0.5)
model = tflearn.fully_connected(model, len(char_idx), activation='softmax')
model = tflearn.regression(model, optimizer='adam', loss='categorical_crossentropy', learning_rate=LR)
model = tflearn.SequenceGenerator(model, dictionary=char_idx, seq_maxlen=maxlen, clip_gradients=3.0)

model.load('modelStoryHIMYM.model')
iteration = 1

# while True:
	# print "Iteration: {}".format(iteration)
	# model.fit(X, Y, n_epoch=3, validation_set=0.1, run_id='StoryHIMYM', batch_size=128)
	# model.save('modelStoryHIMYM.model')
	# iteration += 1
for i in range(1):
	seed = random_sequence_from_textfile(path, maxlen)
	print "Testing"
	print "Seed: {}" .format(seed)
	print "Testing with a temperature of 1.0"
	print model.generate(500, temperature=1.0, seq_seed=seed)
	print "\nTesting with a temperature of 0.5"
	print model.generate(500, temperature=0.5, seq_seed=seed)
	print ""
	print ""