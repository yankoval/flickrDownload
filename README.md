# flickrDownload
Download from Flickr all user images in all albums.
python flickrDownload.py -k=11dab5613dbf3bf5b88ed965bb75e4c -s
=a37717766375c11b -u=flickrUserName "-d=C:\Users\Pictures\photos"

## api key & secret
You have to get flickr api key and secret to register in the app garden. Put it as script params.
https://www.flickr.com/services/api/misc.api_keys.html

## User Auth token
Then script prompts you to get user authorization for read permission of all images including private. 
Script open url in browser or you can do it by yourself. On page you have to grant requested permissions. 
Then you will be redirected to xml with a token verifier tag. Just copy it and paste into the script prompt.
Script save token in the .tokenVerifier.txt file.

## Download all albums or just specified
By default script will try to download all albums except you put --album param.
Script will create "photos" folder or will create a folder specified in --dir param.
All images will be downloaded in corresponding albums folders.

## Script update folders
if the album folder or image file already exists, do not overwrite it. Just update.
Algorithm goes through album & page list and downloads only absent images.
So in case of a crash you can just rerun the script again.
