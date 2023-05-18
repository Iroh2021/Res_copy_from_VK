import requests
import os
import time
from tqdm import tqdm

class Yandex:
    with open('YaDisk.txt', 'r') as file_object:
        token = file_object.read().strip()

    folder_path = os.getcwd()
    folder_path = os.path.join(folder_path, 'VKphotos')

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def upload_folder_to_yandex_disk(self, destination_folder_name= 'VKphotos'):

        files = [os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]

        create_folder_response = requests.put(
            'https://cloud-api.yandex.net/v1/disk/resources',
            headers={'Authorization': f'OAuth {self.token}'},
            params={'path': destination_folder_name},
        )

        for file_path in tqdm(files):
            file_name = os.path.basename(file_path)
     
            upload_response = requests.get(
                f'https://cloud-api.yandex.net/v1/disk/resources/upload',
                headers={'Authorization': f'OAuth {self.token}'},
                params={'path': f'{destination_folder_name}/{file_name}', 'overwrite': 'true'},
            )
        
            upload_url = upload_response.json()['href']
        
            with open(file_path, 'rb') as f:
                upload_file = requests.put(upload_url, files={'file': f})
                
            time.sleep(1)
            
        print(f'Папка {destination_folder_name} была успешно создана на Ядиске и все фотографии загруженны.')