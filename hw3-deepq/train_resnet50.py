# 2018 HTC Corporation. All Rights Reserved.
#
# This source code is licensed under the HTC license which can be found in the
# LICENSE file in the root directory of this work.
import os
import shutil

import tensorflow as tf

def get_random_seed():
    """
    this function is called once before the training starts

    returns:
        an integer as the random seed, or None for random initialization
    """
    seed = None
    return seed

def get_model_spec():
    """
    this function is called once for setting up the model

    returns:
        a dictionary contains following items:
            model_name: one of the 'resnet50' and 'mobilenetv2'
            pretrained: a boolean value indicating whether to use pre-trained model
                        if False is returned, default initialization will be used
            arg_scope_dict: a dictionary which will be used as keyword arguments when
                            initializing the arg_scope of the model.
                            please refer to tf.contrib.slim.arg_scope for details

    notes:
        any key in arg_scope_dict starts with batch_norm will be disabled
        typically, only 'weight_decay' is nessasary to be in arg_scope_dict
    """
    return {"model_name": "resnet50", "pretrained": True, "arg_scope_dict": {}}

lr = None
def get_optimizer():
    """
    this function is called once for setting up the optimizer

    returns:
        a tf.train.Optimizer

    notes:
        you should track placeholder using global variables yourself
    """
    global lr
    lr = tf.placeholder(tf.float32, shape=[])
    
    #optimizer = tf.train.AdamOptimizer(learning_rate=lr, beta1=0.9, beta2=0.999, epsilon=1e-08) #tf.train.GradientDescentOptimizer(learning_rate=lr)
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=lr) #GradientDescent
    return optimizer

def get_eval_spec():
    """
    this function is called once for setting up evaluation / inferencing

    returns:
        a dictionary contains following items:
            transform: a transform used to preprocess evalutaion / inferencing images
                       should be a callable which takes a 256 x 256 x 3 tensor of type tf.float32
                       and produces either a 244 x 244 x 3 tensor or a NC x 244 x 244 x 3 tensor
                        in the latter case:
                            NC stands for the number of crops of an image,
                            NC predictions will be inferenced on the NC crops
                            then those predictions will be average to produce a final prediction
            batchsize: an integer between 1 and 64
    """
    transform = lambda image: tf.image.resize_images(image, [224, 224])
    return {"transform": transform, "batchsize": 32}


def before_epoch(train_history, validation_history):
    """
    this function is called before every training epoch

    args:
        train_history:
            a 3 dimensional python list (i.e. list of list of list)
            the j-th element in i-th list is a list containing two entries,
            stands for the [accuracy, loss] for the j-th batch in the i-th epoch

            len(train_history) indicate the index of current epoch
            this value should be within the range of 1~50

        validation_history:
            a 2 dimentsional python list (i.e. list of list)
            the i-th element is a list containing two entry,
            stands for the [accuracy, loss] for the validation result of the i-th epoch

    returns:
        a dictionary contains following items:
            transform: a transform used to preprocess training images
                       should be a callable which takes a 256 x 256 x 3 tensor of type tf.float32
                       and produces a 224 x 224 x 3 tensor
            batchsize: an integer between 1 and 64
    """
    transform = lambda image: tf.image.resize_images(image, [224, 224])
    n_epoch = len(train_history)
    return {"transform": transform, "batchsize": 32}

def before_batch(train_history, validation_history):
    """
    this function is called before each training batch

    args: please refer to before_epoch()

    returns:
        a dictionary contains the following items:
            feed_dict: a dictionary, will be used as the feed_dict to the graph operations
            batch_norm: a float stands for the value of momentum in all batch normalization layers
                        or None indicating no changes should be made
            drop_out: a float stands for the value of drop out probability
                      or None indicating no changes should be made

    notes:
        drop_out should always be None when using resnet50 since there are no dropout layers in it
    """
    global lr
    return {'feed_dict': {lr: 0.01}, 'batch_norm': 0.99, 'drop_out': 0.3}

max_val_acc = -1
def save_model_as(train_history, validation_history):
    """
    this function is called after each epoch's training
    the returned value will be used to determine whether to save the model at this point or not

    args: please refer to before_epoch()

    returns:
        a string, the directory name where the model is going to be saved
        or None indicating no saving is desired for this epoch
    """
    n_epoch = len(train_history)
    global max_val_acc
    savemodel = None
    if validation_history[n_epoch - 1][0] > max_val_acc:
        max_val_acc = validation_history[n_epoch - 1][0] 
        savemodel = "resnet0.99_do0.3retrain"
        print("val_acc {} Storing new model: {}".format(max_val_acc,savemodel))
        if os.path.isdir(savemodel):
            shutil.rmtree(savemodel)
    return savemodel
