import os
import argparse
from PIL import Image

def clean(path):
    for path, dirs, files in os.walk(path):
        for filename in files:
            fullpath = os.path.join(path, filename)
            if ".jpg" in fullpath:
                try:
                    Image.open(fullpath)
                except:
                    print("Delete", fullpath)
                    os.remove(fullpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest="path", required=True, help="Path to clean")
    args = parser.parse_args()
    clean(args.path)
