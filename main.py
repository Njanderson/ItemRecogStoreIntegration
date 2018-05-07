from util import loader
from os.path import join
from os import listdir

URL_PATH = join('data', 'url')
IMG_PATH = join('data', 'img')

if __name__ == '__main__':
    print('Hello world!')
    for f in listdir(URL_PATH):
        loader.load_url(join(URL_PATH, f), IMG_PATH)