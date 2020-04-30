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


mypath = '/Users/Kai/Documents/cs_phd/minje/audio_coding/audio_coding/AUDIO_MUSHRA/SPL-V3-L/'
system_name = 'd_relu_60_5_5_5/'
system_name_framed = system_name[:-1] + '_framed/'
print(system_name_framed)
# frame a 12 second audio clip
second = 12
def process_frame_down_to_k_sec(filename):
	sig, sr = librosa.load(filename, sr=None)
	sig = sig[sr * 1:sr * (1 + second)]
	the_window = np.concatenate((np.concatenate((np.hanning(sr)[:(sr // 2)], [1.0] * sr * (second - 1))), np.hanning(sr)[(sr // 2):]))
	sig *= the_window
	librosa.output.write_wav('/'.join(filename.split('/')[:-2]) + '/' + system_name_framed + i.split('/')[-1], sig, sr)

# List all wave files under a directory

if os.path.exists(mypath + system_name_framed):
	pass
else:
	os.mkdir(mypath + system_name_framed)



mypath += system_name
onlyfiles = [mypath + f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith('.wav')]
for i in onlyfiles:
	print i
	process_frame_down_to_k_sec(i)


