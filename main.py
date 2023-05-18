import os
from vk import VK
from yadisk import Yandex

def json_file():
     json_file = []
     size_lst = vk.size()
     files = [os.path.join(ya.folder_path, f) for f in os.listdir(ya.folder_path) if os.path.isfile(os.path.join(ya.folder_path, f))]
     for file_path in files:
          file_name = os.path.basename(file_path)
          photo_dict = {}
          i = 0
          photo_dict['file name'] = file_name
          photo_dict['size'] = size_lst[i]
          i += 1
          json_file.append(photo_dict)
     return json_file

if __name__ == '__main__':
     id_vk = input("Введите свой 'id' пользователя 'vk' ")
     with open('user.txt', mode='w', encoding='utf-8') as file:
         file.write(id_vk)
     token_yandex = input('Введите свой Яндекс токен ')
     with open('YaDisk.txt', mode='w', encoding='utf-8') as file:
          file.write(token_yandex)
     vk = VK()
     ya = Yandex()
     vk.download()
     ya.upload_folder_to_yandex_disk()
     with open('json.txt', 'w', encoding= 'utf-8') as f:
          f.write(str(json_file()))
     vk.delete()