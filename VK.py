import requests

class VK:
    def __init__(self, access_token, version='5.131'):
        self.token = access_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def user_ids_get(self, user_ids):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': user_ids}
        response = requests.get(url, params={**self.params, **params})
        return response.json()['response'][0]['id']

    def photos_get_data(self, owner_id, album_id='profile', extended='1', photo_sizes='1'):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': owner_id, 'album_id': album_id, 'extended': extended, 'photo_sizes': photo_sizes}
        response = requests.get(url, params={**self.params, **params})
        photos_quantity = int(input('Введите количество загружаемых фото: '))
        photos_list = [albums['sizes'][-1]['url'] for albums in response.json()['response']['items'][:photos_quantity]]
        photos_type = [albums['sizes'][-1]['type'] for albums in response.json()['response']['items'][:photos_quantity]]
        photos_likes = [albums['likes']['count'] for albums in response.json()['response']['items'][:photos_quantity]]
        photos_date = [albums['date'] for albums in response.json()['response']['items'][:photos_quantity]]
        photos_data = zip(photos_likes, photos_list, photos_date, photos_type)
        return photos_data
