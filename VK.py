import requests, os

class VK:
    url = 'https://api.vk.com/method/'

    with open('token.txt', 'r') as file_object:
        token = file_object.read().strip()

    with open('user.txt', 'r') as file_object:
        id = file_object.read()

    def __init__(self, version = '5.131'):
        self.version = version
        self.params = {
            'access_token': self.token,
            'user_id': self.id,
            'v': self.version
        }

    def photos_get(self, album_id = 'wall'):
        photos_url = self.url + 'photos.get'
        photos_get_params = {
            'owner_id': self.id,
            'album_id': album_id,
            'extended': 1
        }

        res = requests.get(photos_url, params= {**self.params, **photos_get_params}).json()
        return res['response']['items']
    
    def photos_lst(self):
        res = self.photos_get()
        photos_lst = []

        for i in res:
            sum_size = []
            for k in i['sizes']:
                sum = int(k['height'] + k['width'])
                sum_size.append(sum)
            for k in i['sizes']:
                if max(sum_size) == int(k['height']) + int(k['width']):
                    photos_lst.append(k['url'])

        return photos_lst
    
    def likes(self):
        res = self.photos_get()
        likes_lst = []

        for i in res:
            likes_lst.append(i['likes']['count'])
        
        return likes_lst

    def size(self):
        photos_all = self.photos_get()
        photos_lst = self.photos_lst()
        size_lst = []

        for i in photos_all:
            for k in i['sizes']:
                for photo in photos_lst:
                    if photo in k['url']:
                        size_lst.append(k['type'])
        
        return size_lst

    def download(self):
        photo_lst = self.photos_lst()
        likes = self.likes()
        count = 0
        target_folder = os.path.join(os.path.join(os.path.expanduser('~'), 'Desktop'))
        target_folder = os.path.join(target_folder, 'VKphotos')
        os.makedirs(target_folder, exist_ok=True)
        target_folder = os.path.abspath(target_folder)

        for url in photo_lst:
            file_to_download = requests.get(url)
            with open(os.path.join(target_folder, str(f'Количество_лайков_{likes[count]}_номер_фото{count + 1}') + ".jpg"), 'wb') as file:
                file.write(file_to_download.content)
                count += 1
                print(f'')

        return target_folder.split(os.path.sep)[-1]