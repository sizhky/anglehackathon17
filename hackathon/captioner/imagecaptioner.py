
# coding: utf-8

# In[14]:


import keras
from keras.layers import Embedding,GRU, Dense, RepeatVector, Merge, Activation, GlobalAveragePooling2D
from keras.preprocessing.text import one_hot
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.applications.inception_v3 import InceptionV3
import numpy as np
from PIL import Image


# In[7]:
root_folder = '/home/angle/hackathon/captioner/'

VOCAB = 400
def get_model(train=True):
    if train:
        max_caption_len = MAX_CAPTION_LEN
        BS = None
        _base_model_ = base_model
        _ip_ = base_model.inputs[0]
    else:
        max_caption_len = 1
        BS = (1, 1)
        ip = keras.layers.Input(batch_shape=((1, 220, 258, 3)))
        BASE_MODEL = InceptionV3(weights='imagenet', input_tensor=ip, include_top=False)
        _base_model_ = BASE_MODEL
        _ip_ = ip

    
#    print "Text model loading"
    language_model_input = keras.layers.Input((max_caption_len,), batch_shape=BS)
    language_model = Embedding(VOCAB, 256)(language_model_input)
    language_model = GRU(units=128, return_sequences=True, stateful=(not train))(language_model)
    language_model = Dense(128)(language_model)
#    print "Text model loaded"
    image_model = _base_model_.output
    for layer in _base_model_.layers:
        layer.trainable = False
    # let's repeat the image vector to turn it into a sequence.
#    print "Repeat model loading"
    image_model = GlobalAveragePooling2D()(image_model)
    image_model = RepeatVector(max_caption_len)(image_model)
#    print "Repeat model loaded"
    # the output of both models will be tensors of shape (samples, max_caption_len, 128).
    # let's concatenate these 2 vector sequences.
#    print "Merging"
#     return(image_model, language_model)
    model = keras.layers.merge([image_model, language_model], mode='concat', concat_axis=-1)
    # model.add(keras.layers.merge([image_model, language_model], mode='concat', concat_axis=-1))
    # let's encode this vector sequence into a single vector
    model = GRU(256, return_sequences=True, stateful=(not train))(model)
    # which will be used to compute a probability
    # distribution over what the next word in the caption should be!
    model = Dense(VOCAB)(model)
    model = Activation('softmax')(model)

    MODEL = keras.models.Model([_ip_, language_model_input], [model])
    MODEL.compile(loss='categorical_crossentropy', optimizer='rmsprop')
#    print "Merged"
    return(MODEL)


# In[19]:


f = np.array
my_image = 'img.jpg'
test_ = get_model(0)
test_.load_weights(root_folder+'IC_weights_FULL.h5')



def jpg_image_to_array(image_path):
    """
    Loads JPEG image into 3D Numpy array of shape 
    (width, height, channels)
    """
    from PIL import ImageFile
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    with Image.open(image_path) as image:
        image = image.resize((258, 220))
        im_arr = np.fromstring(image.tobytes(), dtype=np.uint8)
        im_arr = im_arr.reshape((image.size[1], image.size[0], 3))
    return im_arr
import pickle
with open(root_folder+'idx2word.dict_FULL.pkl', 'r') as g:
    i2w = pickle.load(g)

##################################################################
# test_.reset_states()
# ix = np.random.randint(0, 1467)
# p = 2
# preds = []
# i = 0
# while p not in [0, 1]:
#     p = test_.predict([f([jpg_image_to_array(my_image)]), f([p])])
#     p = p.argmax(axis=2)[0][0]
#     preds.append(p)
#     i+=1
#     if i%20==0:
#         print(i)
# print([i2w[i] for i in preds if i!=0])

# Image.fromarray(np.uint8(jpg_image_to_array(my_image)))
##################################################################
def get_captions(img):
    test_.reset_states()
    # ix = np.random.randint(0, 1467)
    p = 2
    preds = []
    i = 0
    while p not in [0, 1]:
        p = test_.predict([f([jpg_image_to_array(img)]), f([p])])
        p = p.argmax(axis=2)[0][0]
        preds.append(p)
        i+=1
        if i%20==0:
            print(i)
    return(' '.join([i2w[i] for i in preds if i!=0][:-1]))

# print(get_captions(my_image))


# In[ ]:




