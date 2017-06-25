# import the necessary libraries
import numpy as np
import caffe
import h5py
import tables
import sys
import timeit
import os
from os import walk

#Use command line argumensts as variables
proto_txt = '/home/angle/hackathon/ssdh.prototxt'
caffe_model = '/home/angle/hackathon/ssdh.caffemodel'
path = '/home/angle/snapdeal_scrapper/output/full'
batch_size=128
bit_size = 48

#Function to generate hash codes, given the model and path to images
def generate_hash(proto_txt, caffe_model, path):
        #Load the network its weights
        print '"Loading network and its weights ..."'
        net = caffe.Net(proto_txt, caffe_model, caffe.TEST)

        #Load input and configure preprocessing
        transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
        transformer.set_mean('data', np.load('/home/angle/software/caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1))
        transformer.set_transpose('data', (2,0,1))
        transformer.set_channel_swap('data', (2,1,0))
        transformer.set_raw_scale('data', 255.0)

        #Find the number of image files in the directory
        print '"Calculating number of images in the directory ..."'
        #files_per_subdir = []
        #for (root, dirs, files) in walk(path):
        #        files_per_subdir.append(len(files))
        #nfiles = sum(files_per_subdir)
        #print 'Total number of files:',nfiles
	nfiles = 5000

        #Read the database which is in HDF5 format
        print '"Reading the hashcode database ..."'
        if(os.path.isfile('/home/angle/hackathon/hashcode_db.h5')):
                f = tables.open_file('/home/angle/hackathon/hc_db.h5', 'w')
        else:
                f = tables.open_file('/home/angle/hackathon/hc_db.h5','w')


	#Create group 'hashcodes' & 'imageids' group
	f.create_carray(f.root, 'hashcodes', tables.Int8Atom(), shape=(nfiles,bit_size), chunkshape=(batch_size*128,bit_size))
	# f.createCArray(f.root, 'features', tables.Float32Atom(), shape=(nfiles,4096), chunkshape=(batch_size*128,4096))
	f.create_carray(f.root, 'imageids', tables.StringAtom(256), shape=(nfiles,1), chunkshape=(batch_size*128,1))



	#os.chdir(path)
	#Read all the image files in the directory
	files = []
	for (root, dirs, img_files) in walk(path):
		for dir_file in img_files:
			files.append(os.path.join(root,dir_file))
			if len(files)==5000:
				break

	print 'Total train files: ',len(files)

	#Slpit the image files in the directory into mini batches
	print '"Spliting the images into mini-batches ..."'
	mini_batches = [files[i:i+batch_size] for i in range(0,len(files),batch_size)]

	#Iterate over each mini batch, create training data of the mini batch and generate hash codes for the same
	print '"Creating/updating the database ..."'
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

		#Store fc7 layer features
		# ft = net.blobs['fc7'].data

		#Update/append the hashcode_db.h5
		start = i*batch_size
		end = start+mb_size
		f.root.hashcodes[start:end] = h
		# f.root.features[start:end] = ft
		f.root.imageids[start:end] = np.asarray(batch).reshape(mb_size,1)
		f.flush()
		print 'Batch',i,'out of',len(mini_batches), 'done.'
		i+=1

	#Close the connection to HDF5 file
	print '"Database created/updated."'
	f.close()


#Call the function to generate hash codes
t0 = timeit.default_timer()
generate_hash(proto_txt, caffe_model, path)
t1 = timeit.default_timer()

print 'Time taken: '
pstype(int)

