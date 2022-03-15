from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2
import os


def app():
    '''initialise'''
    model = load_model('CV/keras_model.h5')     # Load the model from TM
    img_dir = 'CV/img'                  # define the image directory
    live = 5           # If not using pre-loaded images, analyse the number of live images stated

    data = np.ndarray(shape=(live, 224, 224, 3), dtype=np.float32)  # Create data array based on live images
    size = (224, 224)                                               # resize image to TM for data array


    for i in range(live):                   # repeat for the number of live images to be analyse
        cam = cv2.VideoCapture(0)           # (0) defines camera ID
        image = cam.read()[1]               # position [1] stores the image captured
        cv2.imshow("image_%s" % (i + 1), image)                         # show image
        # cv2.imwrite(img_dir + "/" + 'image_%s.jpg' % (i + 1), image)    # save image
        image = Image.open(img_dir + "/" + 'image_%s.jpg' % (i + 1))
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)                     # turn the image into a numpy array
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1  # Normalize the image
        data[i] = normalized_image_array 
        cv2.waitKey(100)                    # (0) press any key to exit, else (x) will hold image for x ms
        cv2.destroyAllWindows()             # close all images

    print("Analysing", len(data), "images.")
    # Copy & Paste


    '''predict'''
    prediction = model.predict(data)            # predict based on model with data
    print(prediction)                           # show prediction
    # Copy & Paste


    my_dict ={}
    line = 0
    print("\n---------Labels---------")
    labels_file = open("CV/labels.txt", "r")    # open labels.txt file
    print(labels_file.read())                   # show labels
    labels_file.close()

    with open('CV/labels.txt') as f:
        for l in f:
            my_dict[line]=[]
            line += 1




    print("\n---------Results--------")
    predict = prediction.tolist()                       # convert prediction to list
    for j in range(len(predict)):                       # for the number of images analysed,...
        max_value = max(predict[j])                     # identify the max value in the entire list
        max_index = predict[j].index(max_value)
        print(max_index)
        print(my_dict[max_index])
        my_dict[max_index].append(j+1)

    print(my_dict.keys(), my_dict.values())
    max_key = 0

    for key,value in my_dict.items():
        if len(value) > len(my_dict[max_key]):
            max_key = key
            print(max_key)

    return max_key