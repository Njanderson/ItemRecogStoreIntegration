from util import downloader
from os.path import join, exists
from os import listdir

URL_PATH = join('data', 'url')
IMG_PATH = join('data', 'img')

if __name__ == '__main__':
    for f in listdir(URL_PATH):
        name = f[:f.index('.')]
        downloader.load_url(join(URL_PATH, f), IMG_PATH, name)

