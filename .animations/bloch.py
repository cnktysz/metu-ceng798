from qiskit.visualization import plot_bloch_vector
from qiskit.visualization import plot_bloch_multivector
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import os 

def delete_all_logs(log_dir):
	log_list = os.listdir(log_dir)
	for item in log_list:
		if item.endswith('.png'):
			os.remove(log_dir+item)

def plot_2_qubits():
	fig = plot_bloch_multivector([0,1,0,0])
	fig.savefig('png/out.png')
	plt.close()	


def vector():
	fig = plot_bloch_vector([0,-1,0])
	fig.plot([1,0],[0,0])
	fig.savefig('png/out.png')
	plt.close()	

def rotate_y(i,v):
	fig = plot_bloch_vector([np.sin((i/180)*np.pi)*np.cos((v/180)*np.pi),np.sin((i/180)*np.pi)*np.sin((v/180)*np.pi),np.cos((i/180)*np.pi)])
	fig.savefig('png/to_gif/out_%4.d.png'%i)
	plt.close()

'''
delete_all_logs('png/to_gif/')
for i in tqdm(range(0,91,1)):
	if i < 45:
		v=i
	else: 
		v=90-i
	rotate_y(i,v)
'''
vector()
