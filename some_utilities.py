import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import IPython
import librosa
import soundfile as sf
import numpy as np
from resampy import resample
import itertools
import numpy as np
import scipy
import collections
import subprocess
from matplotlib import rcParams
import os
from os import listdir
from os.path import isfile, join


# frame a 12 second audio clip
second = 12
def process_frame_down_to_k_sec(filename):
	sig, sr = librosa.load(filename, sr=None)
	sig = sig[sr * 1:sr * (1 + second)]
	the_window = np.concatenate((np.concatenate((np.hanning(sr)[:(sr // 2)], [1.0] * sr * (second - 1))), np.hanning(sr)[(sr // 2):]))
	sig *= the_window
	librosa.output.write_wav('/'.join(filename.split('/')[:-2]) + '/' + system_name_framed + i.split('/')[-1], sig, sr)



# system_name = 'd_relu_60_5_5_5/'
# system_name_framed = system_name[:-1] + '_framed/'
# system_name = ['ref/', 'lp_3p5/', 'lp_7/', 'mp3_112/', 'model_a_168/', 'model_c_96/', 'model_c_112/', 'model_d_96/', 'model_d_112/']
system_name = ['ref/', 'lp_3p5/', 'mp3_64/', 'model_a_64/', 'model_a_79/', 'model_b_79/']
system_name_framed = ''
for i in system_name:
	mypath = '/Users/Kai/Documents/cs_phd/minje/audio_coding/audio_coding/AUDIO_MUSHRA/SPL-V3-L/'
	system_name_framed = i[:-1] + '_framed/'
	print(i, system_name_framed)
	

	# List all wave files under a directory

	if os.path.exists(mypath + system_name_framed):
		pass
	else:
		os.mkdir(mypath + system_name_framed)

	mypath += i
	onlyfiles = [mypath + f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith('.wav')]
	for i in onlyfiles:
		# print i
		process_frame_down_to_k_sec(i)


