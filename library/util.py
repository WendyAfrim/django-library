import requests
from django.conf import settings

def get_book_cover_url(book_name, book_author=None):
    url = 'https://www.googleapis.com/books/v1/volumes?q='
    url += f'intitle:{book_name}'
    if book_author:
        url += '+inauthor:' + book_author
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['totalItems'] > 0 and 'imageLinks' in data['items'][0]['volumeInfo']:
            cover_url = data['items'][0]['volumeInfo']['imageLinks']['thumbnail'].replace('http://', 'https://')
            # cover_url = cover_url.replace('zoom=1', 'zoom=0') # zoom=0 for better quality but some images are not available
            return cover_url
        else:
            return None
    return None

def upload_image_to_imgbb(image):
    url = 'https://api.imgbb.com/1/upload'
    payload = {
        'key': settings.IMGBB_API_KEY,
        'image': image,
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        data = response.json()
        return data['data']['url']
    return None