from src.utils.all_utils import read_yaml
from src.utils.embed_utils import extract_uri_id_link, folder_items_response, videos_response
# import logging
import os
import time
import vimeo
from glob import glob
import pandas as pd
import wget
import requests
from urllib.request import Request, urlopen, urlretrieve


# logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
# log_dir = "logs"
# os.makedirs(log_dir, exist_ok=True)
# logging.basicConfig(filename=os.path.join(log_dir, 'running_logs.log'), level=logging.INFO, format=logging_str,
#                     filemode="a")


class VimeoEmbed:
    def __init__(self, secret_path, config_path, video_list_path):
        self.secrets = read_yaml(secret_path)
        self.config = read_yaml(config_path)
        self.video_list_path = read_yaml(video_list_path)


        # vimeo authentication
        self.vimeo_path = self.secrets["vimeo"]
        self.tokens = self.vimeo_path["token"]
        self.keys = self.vimeo_path["key"]
        self.sec = self.vimeo_path["secret"]

        self.downloaded_videos_list = self.video_list_path['downloaded_videos_list']
        self.failed_videos_list = self.video_list_path['failed_videos_list']
        

        # config setup
        self.video_path = self.config["video_path"]
        self.current_path = os.getcwd()
        os.makedirs(self.video_path, exist_ok=True)
        self.uploader_path = os.path.join(self.current_path, self.video_path)
        self.client = vimeo.VimeoClient(token=self.tokens, key=self.keys, secret=self.sec)
    
    def level_0_embed_link(self, link):
        try:
            # logging.info('>>>>>>>Level 0 Process Started')
            print(self.downloaded_videos_list, self.failed_videos_list)
            uri_id = extract_uri_id_link(link)
            video_response_data_list = videos_response(self.client, uri_id)
            
            response = self.client.get(f"/users/127902260/folders/{uri_id}")
            link_response = response.json()
            folder_name = link_response['name']
            video_id = link_response['uri'].split('/')[-1]
            # create folder for each folder
            os.makedirs(os.path.join(self.uploader_path, folder_name), exist_ok=True)

            # link_response['uri'].split('/')[-1]
            #read video response data and save in yaml

            root_folder_name = []
            for video_data in video_response_data_list:
                for i in video_data:
                    video_name = i['name']
                    # download_link_list.append(i['player_embed_url'])
                    root_folder_name.append(folder_name)
                    for downloads in i['download']:
                        if downloads['height'] == 1080:
                            # download_link_list.append(downloads['link'])
                            r = requests.get(downloads['link'], stream=True)
                            # prin status code
                            if r.status_code == 200:
                                open(os.path.join(os.path.join(self.uploader_path, folder_name), f'{video_name}.mp4')\
                                            , 'wb').write(r.content)
                                self.downloaded_videos_list.append(video_id)
                            else:
                                self.failed_videos_list.append(video_id)
                                pass
            
                # wget.download(download_link, self.uploader_path, )
        except Exception as e:
            # logging.info(e)
            raise e
    
    def level_1_embed_link(self, link):
        try: 
            uri_id = extract_uri_id_link(link)
            folder_response_data_list = folder_items_response(self.client, uri_id)
            
            response = self.client.get(f"/users/127902260/folders/{uri_id}")
            folder_name = response.json()['name']
            
            embedded_link_list = []
            video_name_list = []
            parent_folder_list = []
            subfolder_uri_id_list = []
            root_folder_name = []
            for folder_data in folder_items_response(self.client, uri_id):
                for i in folder_data:
                    if i['type'] == 'folder':
                        subfolder_uri_id_list.append(extract_uri_id_link(i['folder']['uri']))

            for ids in subfolder_uri_id_list:
                for video_data in videos_response(self.client, ids):
                    for i in video_data:
                        video_name_list.append(i['name'])
                        embedded_link_list.append(i['player_embed_url'])
                        parent_folder_list.append(i['parent_folder']['name'])
                        root_folder_name.append(folder_name)
                        
            data = {'Root Folder': root_folder_name, 'Section Name': parent_folder_list, 'Lesson Title': video_name_list,'Lesson URL': embedded_link_list}
            df = pd.DataFrame(data)
            # os.makedirs('artifacts/level_1', exist_ok= True)
            
            if '/' in folder_name:
                folder_name = folder_name.replace('/', '_')

            df.to_excel(f'artifacts/{folder_name}.xlsx', index= False)
        except Exception as e:
            # logging.error(e)
            raise e
                
    def level_2_embed_link(self, link):
        try:
            uri_id = extract_uri_id_link(link)
            
            response = self.client.get(f"/users/127902260/folders/{uri_id}")
            folder_name = response.json()['name']
            
            sub_subfolder_uri_id_list = []
            video_name_list = []
            embedded_link_list = []
            parent_folder_list = []
            root_folder_name = []
            subject_name_list = []
            subfolder_uri_id_list = []
            for folder_data in folder_items_response(self.client, uri_id):
                for i in folder_data:
                    if i['type'] == 'folder':
                        sub_subfolder_uri_id_list.append(extract_uri_id_link(i['folder']['uri']))
            
            for ids in sub_subfolder_uri_id_list:
                for folder_data in folder_items_response(self.client, ids):
                    for i in folder_data:
                        if i['type'] == 'folder':
                            subfolder_uri_id_list.append(extract_uri_id_link(i['folder']['uri']))

            for ids in subfolder_uri_id_list:
                for video_data in videos_response(self.client, ids):
                    for i in video_data:
                        video_name_list.append(i['name'])
                        embedded_link_list.append(i['player_embed_url'])
                        parent_folder_list.append(i['parent_folder']['name'])
                        root_folder_name.append(folder_name)
                        subject_name_list.append(i['parent_folder']['metadata']['connections']['ancestor_path'][0]['name'])
                        
            data = {'Root Folder': root_folder_name, 'Subject Name': subject_name_list,'Section Name': parent_folder_list, 'Lesson Title': video_name_list,'Lesson URL': embedded_link_list}
            df = pd.DataFrame(data)
            # os.makedirs('artifacts/level_2', exist_ok= True)
            df.to_excel(f'artifacts/{folder_name}.xlsx', index= False)
        except Exception as e:
            # logging.error(e)
            raise e
