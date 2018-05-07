from requests import get
from os.path import join, basename, exists
from os import makedirs

def load_url(url_path, img_path):
    """Download the contents of a single URL file located at url_path,
    formatted with one URL per line. Downloads to location img_path."""

    # Create the out path if it does not exist
    makedirs(img_path, exist_ok=True)

    # Iterate through URLS, downloading each of them
    with open(url_path, 'r') as f:
        urls = [line.strip() for line in f.read().split('\n') if len(line) > 0]
        for url in urls:
            out_path = join(img_path, basename(url))
            # Only re-download if you don't already have this image
            if not exists(out_path):
                try:
                    response = get(url)
                    with open(out_path, 'wb+') as out:
                        out.write(response.content)
                except:
                    # Some URLS may not be valid
                    pass