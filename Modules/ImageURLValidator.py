import requests

def ImageURLValidator(url):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.head(url)
    if not r.headers["content-type"] in image_formats:
        return False
    else:
        return True