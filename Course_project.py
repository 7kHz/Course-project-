import datetime
import json
from tqdm import tqdm
from time import sleep
from VK import VK
from YA import YA
from README import VK_TOKEN, YA_TOKEN, user_id


def photos_upload_to_disk(photos_data, path_name):
    dct_likes = {}
    list_data = []
    for likes, url_photos, date, type_ in photos_data:
        date_time = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d')
        dct_likes[likes] = dct_likes.setdefault(likes, 0) + 1
        if dct_likes.setdefault(likes) != 1:
            if ya.url_upload(f'{path_name}/{likes}\U00002764 {date_time}.jpg', url_photos) == 202:
                list_data.append({'file_name': f'{likes} {date_time}.jpg', 'size': type_})
        else:
            if ya.url_upload(f'{path_name}/{likes}\U00002764.jpg', url_photos) == 202:
                list_data.append({'file_name': f'{likes}.jpg', 'size': type_})
    file_name = [data['file_name'] for data in list_data]
    progress_bar = tqdm(file_name, ncols=60, colour='#3CB371', bar_format='{l_bar} {bar} {n}')
    for name in progress_bar:
        sleep(0.5)
        progress_bar.set_description("Processing %s" % name)
    with open('data_file.json', 'w') as data:
        json.dump(list_data, data, indent=2)


if __name__ == '__main__':
    vk = VK(VK_TOKEN)
    ya = YA(YA_TOKEN)
    photos_upload_to_disk(vk.photos_get_data(vk.user_ids_get(user_id)), ya.folder_create('/Photos_1'))
