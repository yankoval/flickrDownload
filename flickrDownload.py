from pathlib import Path
import flickr_api
from time import sleep
import logging

import random
import webbrowser
import argparse
from urllib.error import HTTPError

verifierFileName = '.tokenVerifier.txt'
delay = 300 # second

# fwait waits and log every minute
def fwait(min):
    sleep(min%60)
    for m in range(min//60):
        logging.info(f'Waiting {m}/{min//60} minutes.')
        sleep(60)
# setupVerifier setup Verifier token from flickrDownload
def setupVerifier(api_key,api_secret):
    try:
        flickr_api.set_keys(api_key=api_key, api_secret=api_secret)
        a = flickr_api.auth.AuthHandler()
    except HTTPError as err:
        if err.code == 401:
            logging.error(f'Error 401: Unauthorized for this api key and secret.')
            exit(-1)
        else:
            raise
    perms = "read"
    url = a.get_authorization_url(perms)
    print("1. Copy the printed URL into a web browser and, if prompted,\n"
            "2. login to Flickr\n" 
            "3. accept requested permissions.\n" 
            "4. You will be redirected to an XML page.\n"
            "5. Locate the oauth_verifier tag. Copy the oauth_verifier tag\n"
            "6. Return here and paste the tag.")
    if input('Ready? y/n:') not in ['y','Y','yes']: exit(-1)
    print(f'Url: {url}')
    webbrowser.open(url, new=0, autoraise=True)
    verifier = input('Paste oauth_verifier tag here and press enter.')
    a.set_verifier(oauth_verifier=verifier)
    a.save(verifierFileName)

def main(**kwargs):
    flickr_api.set_keys(api_key = kwargs["api_key"], api_secret = kwargs["api_secret"])
    token = Path(verifierFileName)
    while not token.exists():
        setupVerifier(kwargs["api_key"], kwargs["api_secret"])
    flickr_api.set_auth_handler(token.name)
    # Path(kwargs["dir"]).mkdir(exist_ok=True)
    root = Path(kwargs["dir"])
    root.mkdir(exist_ok=True)

    user = flickr_api.Person.findByUserName(username=kwargs["user"])

    # get lalbum list
    albLst,album = user.getPhotosets(),None
    if kwargs['album'] != 'all':
        albLst = [a for a in albLst if a.title ==kwargs['album']]
        if not albLst:
            logging.error(f'There is no album:{kwargs["album"]} in {user} albums.')
            exit(-1)

    while True:
        errorCount, errorLimit = 0, 10
        try:
            if not albLst:
                logging.info('Finish! No more album to downland.')
                exit(0)
            album = album if album else albLst.pop(random.randint(0, len(albLst) - 1))
            logging.info(f'Album:{album.title}, {len(albLst)} albums rest.')
            Path(root, album.title).mkdir(exist_ok=True)
            total = album.getPhotos().info.total
            current = 0
            for page_nb in range(1, album.getPhotos().info.pages+1):
                localDir = [f.stem for f in Path(root, album.title).glob('*')]
                dir = [p for p in  album.getPhotos(page=page_nb) if p.title.replace("/", "-") + "_" + p.id  not in localDir]
                logging.info(f'Album:{str(album.title)}, page:{page_nb} of {album.getPhotos().info.pages},{len(dir) if dir else 0} photos to upload,'
                             f' {len(localDir) if localDir else 0} alredy downloaded.')
                if not dir: continue
                for index, photo in enumerate(dir):
                    sizes = photo.getSizes()
                    biggest_size = list(sizes.keys())[-1]
                    photo_file = photo.getPhotoFile(size_label=biggest_size)
                    file_ext = ('.' + photo_file.split('.')[-1]) if photo.media == "photo" else ".mp4"
                    filename = Path(root,album.title,photo.title.replace("/", "-") + "_" + photo.id + file_ext)
                    current += 1
                    if filename.exists():
                        logging.info(f'{Path(root, album.title, filename)} - exist.')
                        continue
                    logging.info(f"Page:{page_nb} {current}/{total} {filename}")
                    photo.save( str(Path(filename.parents[0],filename.stem)), size_label = biggest_size)
            album = None
        except TimeoutError:
            logging.info('Timeout error. Lets wait 10 min.')
            fwait(300)
            errorCount += 1
            if errorCount>errorLimit: exit(-1)
        except Exception as e:
            logging.info(f'Exception type:{type(e).__name__},{ e.args}.')
            # exit if qty of errors more then limit
            #TODO requests.exceptions.ConnectionError: urllib3.exceptions.MaxRetryError: urllib3.exceptions.NewConnectionError:HTTP Server Error 500:
            errorCount += 1
            if errorCount>errorLimit: exit(-1)
            fwait(300)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s',
        handlers=[
            logging.FileHandler("flickr.log"),
            logging.StreamHandler()
        ]
    )
    parser = argparse.ArgumentParser(description='Download from Flickr')
    parser.add_argument('-k','--api-key', help='api-key from https://www.flickr.com/services/api/misc.api_keys.html')
    parser.add_argument('-s','--api-secret', help='api-secret from https://www.flickr.com/services/api/misc.api_keys.html')
    parser.add_argument('-u','--user', help='flickrDownload user name where albums are stored.')
    parser.add_argument('-d','--dir', default ='photos', help='folder for download, default: "photos". Will be created if not exist.')
    parser.add_argument('-a','--album', default ='all', help='flickrDownload album title to download, default all albums. "--album=My album!"')
    args = parser.parse_args()
    logging.info(f'Statrting...')


    main(**vars(args))