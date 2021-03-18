import numpy as np 
import librosa
from os import listdir
from os.path import isfile, join

def snr(ori_sig, dec_sig):
    min_len = min(len(ori_sig), len(dec_sig))
    ori_sig, dec_sig = ori_sig[:min_len], dec_sig[:min_len]
    nom = np.sum(np.power(ori_sig, 2))
    denom = np.sum(np.power(np.subtract(ori_sig, dec_sig), 2))
    eps = 1e-20
    snr = 10 * np.log10(nom / (denom + eps) + eps)
    return min_len, snr, ori_sig, dec_sig


def mse(ori_sig, dec_sig):
	# print(snr(ori_sig, dec_sig)[1])
	_, _, ori_sig, dec_sig = snr(ori_sig, dec_sig)
	# print(np.mean(np.power(np.subtract(ori_sig, dec_sig), 2)))
	return np.mean(np.power(np.subtract(ori_sig, dec_sig), 2))

onlyfiles = [f for f in listdir('./d/') if isfile(join('./d/', f)) and f.endswith('wav')]
print(onlyfiles)
mse_arr = []
for i in onlyfiles:
	mse_arr.append(mse(librosa.load('./d/' + i)[0], librosa.load('./9/' + i)[0]))
print(mse_arr)
print(np.mean(mse_arr))

