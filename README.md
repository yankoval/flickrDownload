# flickrDownload
Download from Flickr all user images in all albums.

## api key & secret
You have to get flickr api key and secret to register in app garden. Put it as params when lunch script.
https://www.flickr.com/services/api/misc.api_keys.html

## User Auth token
Then script prompt you to get user autherisation for read all images including private. 
Script open url in browser or you can do it by yourself. On page you heve to grant requested premissions. 
Then you wil be redirected to xml with token veiefier tag. Jast cipy it and paste into the script prompt.
Script save token in the .tokenVerifier.txt file.

## Download all albums or just specified
By default script will try to download all albums except you put --album param.
Script will be create "photos" folder or will create folder specified in --dir param.
All images will be downloaded in corresponding albums folders.

## Script update folders
if album folder or image file alredy exist script not owerwrite it. 
Algoritm goes thrugh album & page list and download only absent images.
