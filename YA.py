import requests


class YA:
    def __init__(self, oauth_token):
        self.token = oauth_token

    def get_headers(self):
        return {'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': self.token}

    def folder_create(self, path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': path}
        response = requests.put(url, headers=self.get_headers(), params=params)
        while True:
            if response.status_code == 409:
                print(response.json()['message'])
                path_ = input('Введите новое имя папки по указанному или новому пути: ')
                return self.folder_create(path_)
            if response.status_code == 201:
                break
        return path

    def url_upload(self, ya_path, url_file):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'path': ya_path, 'url': url_file}
        response = requests.post(url, headers=self.get_headers(), params=params)
        return response.status_code
