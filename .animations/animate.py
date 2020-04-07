import imageio, os

images = []
filenames = sorted(os.listdir("png/"))

for i in range(len(filenames)):
	filenames[i] = 'png/'+ filenames[i]

print(filenames)

for filename in filenames:
    images.append(imageio.imread(filename))

imageio.mimsave('gifs/out.gif', images)