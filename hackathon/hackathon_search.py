# import numpy as np
import caffe
import tables
import os
from os import walk
import sys
import timeit
import numpy as np

proto_txt = 'ssdh.prototxt'
caffe_model = 'ssdh.caffemodel'
image = '/home/angle/hackathon/query/img.jpg'

#Function to generate hash codes, given the model and path to images
def ann_images(id):
    #Load the network its weights
    print '"Loading network and its weights ..."'
    net = caffe.Net(proto_txt, caffe_model, caffe.TEST)

    #Load input and configure preprocessing
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_mean('data', np.load('/home/angle/software/caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1))
    transformer.set_transpose('data', (2,0,1))
    transformer.set_channel_swap('data', (2,1,0))
    transformer.set_raw_scale('data', 255.0)

    #Read the database which is in HDF5 format
    print '"Reading the hashcode database ..."'
    f = tables.open_file('/home/angle/hackathon/hc_db.h5','r')

    t0 = timeit.default_timer()
    im = caffe.io.load_image(id)
    im = transformer.preprocess('data',im)

    net.blobs['data'].reshape(1, 3, 227, 227)
    net.blobs['data'].data[...] = im

    out = net.forward()
    h = out['latent_sigmoid']
    h[h<=0.5] = 0
    h[h>0.5] = 1
    h=h.astype(int)

    hc = f.root.hashcodes
    ids = f.root.imageids

    #Compute distance between the search image and nearest neighbors
    #g = tables.openFile('/home/vivek/visual_search/cluster_db.h5','r')
    #clusters = g.root.cluster
    #centers = g.root.cluster_centers

    #d = [sum(h[0,i]!=centers[n,i] for i in range(centers.shape[1])) for n in range(centers.shape[0])]
    #d = np.argsort(np.asarray(d))

    #h1 = np.where(clusters[:,0]==d[0])
    #h1 = np.asarray(h1)
    #h1 = h1.reshape(h1.shape[1],)

    #h2 = np.where(clusters[:,0]==d[1])
    #h2 = np.asarray(h2)
    #h2 = h2.reshape(h2.shape[1],)

    #ann_hcs = np.sort(np.concatenate((h1,h2),axis=0))
    #print 'Number of nearest neighbors'
    #print ann_hcs.shape

    ###ann = [sum(h[0,i]!=hc[j,i] for i in range(centers.shape[1])) for j in ann_hcs]
    ###ann = [sum(h[0,i]!=hc[j,i] for i in range(centers.shape[1])) for j in range(hc.shape[0])]

    #a_tile = np.tile(h[0,:], (ann_hcs.shape[0], 1))
    #ann = sum(a_tile[:,i]!=hc[ann_hcs[:,],i] for i in range(centers.shape[1]))


    #Compute distance between the search image & all the images in the database
    a_tile = np.tile(h[0,:], (hc.shape[0],1))
    #ann = sum(a_tile[:,i]!=hc[:,i] for i in range(hc.shape[1]))
    ann = np.sum(a_tile[:,]!=hc[:,], axis=1)

    #Find the images in the database with least hamming distance with the search image
    ann = np.argsort(ann)
    ann_image_ids = np.take(ids,ann[0:20])
    print ann_image_ids
    t1 = timeit.default_timer()

    print 'time for search'
    print t1-t0

    os.system('mkdir search_results')
    for id in ann_image_ids:
        os.system('cp '+id+' ./search_results/')

    f.close()


ann_images(image)
