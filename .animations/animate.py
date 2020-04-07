import imageio, os

def delete_all_logs(log_dir):
	log_list = os.listdir(log_dir)
	for item in log_list:
		if item.endswith('.png'):
			os.remove(log_dir+item)


images = []
filenames = sorted(os.listdir("png/to_gif/"))

for i in range(len(filenames)):
	filenames[i] = 'png/to_gif/'+ filenames[i]


for filename in filenames:
    images.append(imageio.imread(filename))

imageio.mimsave('gifs/out.gif', images)


delete_all_logs('png/to_gif/')