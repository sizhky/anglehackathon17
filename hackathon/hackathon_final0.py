# import the necessary libraries
import numpy as np
import caffe
import h5py
import tables
import sys
import timeit
import os
from os import walk



def initiallize_network():
	proto_txt = '/home/angle/hackathon/ssdh.prototxt'
	caffe_model = '/home/angle/hackathon/ssdh.caffemodel'
	query = '/home/angle/hackathon/query/img.jpg'
	path = '/home/angle/hackathon/ir'
	pwd = os.getcwd()
	batch_size=128
	bit_size = 48
	# Load the network its weights
	print '"Loading network and its weights ..."'
	net = caffe.Net(proto_txt, caffe_model, caffe.TEST)

	# Load input and configure preprocessing
	transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
	transformer.set_mean('data', np.load('/home/angle/software/caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1))
	transformer.set_transpose('data', (2,0,1))
	transformer.set_channel_swap('data', (2,1,0))
	transformer.set_raw_scale('data', 255.0)


# imq = caffe.io.load_image(query)
# im_query = transformer.preprocess('data',imq)

# # load the mini-batch in the data layer
# net.blobs['data'].reshape(1, 3, 227, 227)
# net.blobs['data'].data[...] = im_query

# # compute the hash codes of the mini-batch
# out = net.forward()
# #print type(out)
# #print out.keys()
# hq = out['latent_sigmoid']
# hq[h<=0.5] = 0
# hq[h>0.5] = 1

# hq[h>0.5] = 1
# hq=hq.astype(int)

#Function to generate hash codes, given the model and path to images
def generate_hash(path):
	#Find the number of image files in the directory
	print '"Calculating number of images in the directory ..."'
	files_per_subdir = []
	for (root, dirs, files) in walk(path):
		files_per_subdir.append(len(files))
	nfiles = sum(files_per_subdir)
	print 'Total number of files:',nfiles

	#os.chdir(path)
	#Read all the image files in the directory
	files = []
	for (root, dirs, img_files) in walk(path):
		for dir_file in img_files:
			files.append(os.path.join(root,dir_file))

	print 'Total train files: ',len(files)

	#Slpit the image files in the directory into mini batches
	print '"Spliting the images into mini-batches ..."'
	mini_batches = [files[i:i+batch_size] for i in range(0,len(files),batch_size)]

	#Iterate over each mini batch, create training data of the mini batch and generate hash codes for the same
	print '"Creating/updating the database ..."'
	f_hc = []
	f_id = []
	i = 0
	for batch in mini_batches:
		mb = []
		#Iterate over each image and appemd it to the mini-batch
		for id in batch:
			#im = caffe.io.load_image(path+'/'+id)
			im = caffe.io.load_image(id)
			im = transformer.preprocess('data',im)
			mb.append(im)
		#print('=>'),
		mb_size = len(mb)
		mb = np.asarray(mb)
		#print '\n'

		#load the mini-batch in the data layer
		net.blobs['data'].reshape(mb_size, 3, 227, 227)
		net.blobs['data'].data[...] = mb

		#compute the hash codes of the mini-batch
		out = net.forward()
		#print type(out)
		#print out.keys()
		h = out['latent_sigmoid']
		h[h<=0.5] = 0
		h[h>0.5] = 1

		h[h>0.5] = 1
		h=h.astype(int)

		#Update/append the hashcode_db.h5
		start = i*batch_size
		end = start+mb_size
		f_hc[start:end] = h
		f_id[start:end] = np.asarray(batch).reshape(mb_size,1)
		print 'Batch',i,'out of',len(mini_batches), 'done.'
		i+=1
		return f_hc, f_id


hcs, ids = generate_hash(path)

#Function to generate hash codes, given the model and path to images
def ann_images(id):

	im = caffe.io.load_image(id)
	im = transformer.preprocess('data',im)

	net.blobs['data'].reshape(1, 3, 227, 227)
	net.blobs['data'].data[...] = im

	out = net.forward()
	h = out['latent_sigmoid']
	h[h<=0.5] = 0
	h[h>0.5] = 1
	h=h.astype(int)

	#Compute distance between the search image & all the images in the database
	a_tile = np.tile(h[0,:], (hcs.shape[0],1))
	#ann = sum(a_tile[:,i]!=hc[:,i] for i in range(hc.shape[1]))
	ann = np.sum(a_tile[:,]!=hcs[:,], axis=1)

	#Find the images in the database with least hamming distance with the search image
	ann = np.argsort(ann)
	ann_image_ids = np.take(ids,ann[0:20])

	# if os.path.isdir('/home/angle/hackathon/search_results'):
	# 	os.system('rm -rf /home/angle/hackathon/search_results')

	# os.system('mkdir /home/angle/hackathon/search_results')
	# for id in ann_image_ids:
	# 	os.system('cp'+id+'/home/angle/hackathon/search_results/')


ann_images(image)

