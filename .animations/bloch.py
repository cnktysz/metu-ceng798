from qiskit.visualization import plot_bloch_vector
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import os 

def delete_all_logs(log_dir):
	log_list = os.listdir(log_dir)
	for item in log_list:
		if item.endswith('.png'):
			os.remove(log_dir+item)


def rotate_y(i):
	fig = plot_bloch_vector([np.sin((i/180)*np.pi),0,np.cos((i/180)*np.pi)], title="New Bloch Sphere")
	fig.savefig('png/out_%4.d.png'%i)
	plt.close()

delete_all_logs('png/')
for i in tqdm(range(0,360,10)):
	rotate_y(i)