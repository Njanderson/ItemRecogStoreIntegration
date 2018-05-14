from util import imagedownloader
from os.path import join
from os import listdir
from model.cnn import run_model

URL_PATH = join('data', 'url')
IMG_PATH = join('data', 'img')

if __name__ == '__main__':
    for f in listdir(URL_PATH):
        imagedownloader.load_url(join(URL_PATH, f), IMG_PATH)