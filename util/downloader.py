from requests import get
from os.path import join, basename, exists, dirname
from os import makedirs, listdir, remove
from pathlib import Path
from hashlib import md5
from PIL import Image

TRAIN_DIR_NAME = 'train'
VAL_DIR_NAME = 'test'

def load_url(url_path, img_path, label, train_frac=0.9):
    """
    Download the contents of a single URL file located at url_path,
    formatted with one URL per line. Downloads to location img_path.
    Will clean up invalid images and duplicates after running.
    """

    # Create the out path if it does not exist
    makedirs(img_path, exist_ok=True)

    # Iterate through URLS, downloading each of them
    with open(url_path, 'r') as f:
        urls = [line.strip() for line in f.read().split('\n') if len(line) > 0]
        num_train = train_frac * len(urls)
        for i, url in enumerate(urls):
            out_path = join(img_path, TRAIN_DIR_NAME if i < num_train else VAL_DIR_NAME, label, basename(url))
            out_dir = Path(dirname(out_path))
            out_dir.mkdir(parents=True, exist_ok=True)
            # Only re-download if you don't already have this image
            if not exists(out_path):
                try:
                    response = get(url)
                    with open(out_path, 'wb+') as out:
                        out.write(response.content)
                except:
                    # Some URLS may not be valid
                    pass

    # Clean up duplicates - especially for the "Can't find image" repeats
    for to_clean in [TRAIN_DIR_NAME, VAL_DIR_NAME]:
        digests = set()
        for f in listdir(join(img_path, to_clean, label)):
            f = join(img_path, to_clean, label, f)
            with open(f, 'rb') as fd:
                digest = md5(fd.read()).hexdigest()
            if digest in digests:
                # Remove files we have seen before
                remove(f)
            else:
                try:
                    # Remove invalid files as well
                    Image.open(f)
                except:
                    remove(f)
            digests.add(digest)