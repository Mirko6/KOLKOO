# https://gist.github.com/astanin/626356

#from scipy.misc import imread
from matplotlib.pyplot import imread
from sklearn.metrics import classification_report
from numpy import average, round
import numpy as np

def main():
    file1_guess, file_correct = "fotecky/img_output_2.PNG","fotecky/img_correct_2.PNG"
    # read images as 2D arrays (convert to grayscale for simplicity)
    img_guess = to_grayscale(imread(file1_guess).astype(float))
    img_correct = to_grayscale(imread(file_correct).astype(float))
    print(img_guess.shape)
    print(img_correct.shape)
    width = min(img_guess.shape[0], img_correct.shape[0])
    height = min(img_guess.shape[1], img_correct.shape[1])
    img_guess.resize((width, height))
    img_correct.resize((width, height))
    compare_images(img_guess, img_correct)

def compare_images(img_true, img_guess):
    img_true = round(img_true) #0 -> landslide, 1-> neni landslide
    img_guess = round(img_guess)
    print(np.unique(img_true, return_counts=True))
    print(np.unique(img_guess, return_counts=True))

    print(classification_report(img_true.flatten(), img_guess.flatten()))

    

def to_grayscale(arr):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:
        return average(arr, -1)  # average over the last axis (color channels)
    else:
        return arr

def normalize(arr):
    rng = arr.max()-arr.min()
    if rng == 0:
        rng = 1
    amin = arr.min()
    return (arr-amin)*255/rng

main()