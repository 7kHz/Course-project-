import requests
import datetime
import json
from tqdm import tqdm
from time import sleep
from README import VK_TOKEN, YA_TOKEN, user_id


class VK:
    def __init__(self, access_token, version='5.131'):
        self.token = access_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def photos_get(self, owner_id, album_id, extended='1', photo_sizes='1'):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': owner_id, 'album_id': album_id, 'extended': extended, 'photo_sizes': photo_sizes}
        response = requests.get(url, params={**self.params, **params})
        photos_list = [albums['sizes'][-1]['url'] for albums in response.json()['response']['items'][:5]]
        photos_type = [albums['sizes'][-1]['type'] for albums in response.json()['response']['items'][:5]]
        photos_likes = [albums['likes']['count'] for albums in response.json()['response']['items'][:5]]
        photos_date = [albums['date'] for albums in response.json()['response']['items'][:5]]
        photos_data = zip(photos_likes, photos_list, photos_date, photos_type)
        return photos_data


class YA:
    host = 'https://cloud-api.yandex.net/'

    def __init__(self, oauth_token):
        self.token = oauth_token

    def get_headers(self):
        return {'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': self.token
                }

    def url_upload(self, yandex_path, url_file):
        uri = 'v1/disk/resources/upload/'
        url_request = self.host + uri
        params = {'path': yandex_path, 'url': url_file}
        response = requests.post(url_request, headers=self.get_headers(), params=params)
        return response.status_code


if __name__ == '__main__':
    vk = VK(VK_TOKEN)
    ya = YA(YA_TOKEN)
    dct_likes = {}
    list_data = []
    for likes, url_photos, date, type_ in vk.photos_get(user_id, 'profile'):
        date_time = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d')
        dct_likes[likes] = dct_likes.setdefault(likes, 0) + 1
        if dct_likes.setdefault(likes) != 1:
            if ya.url_upload(f'/Download/{likes}\U00002764 {date_time}.jpg', url_photos) == 202:
                list_data.append({'file_name': f'{likes} {date_time}.jpg', 'size': type_})
        else:
            if ya.url_upload(f'/Download/{likes}\U00002764.jpg', url_photos) == 202:
                list_data.append({'file_name': f'{likes}.jpg', 'size': type_})

    with open('data_file.json', 'w') as data:
        json.dump(list_data, data, indent=2)

    file_name = [data['file_name'] for data in list_data]
    progress_bar = tqdm(file_name, ncols=60, colour='#00FF7F', bar_format='{l_bar} {bar} {n}')
    for name in progress_bar:
        sleep(0.5)
        progress_bar.set_description("Processing %s" % name)
