# from all_utils import read_yaml, video_info, user_info, folder_info
import logging
import os
import vimeo
from glob import glob
import pandas as pd

def extract_uri_id_link(link):
    """return uri_id from the given link
    """
    uri_id = str(link).split('/')[-1]
    return uri_id

def folder_page_response(client, uri_id):
    """
    Response to check the number of pages 
    """
    response = client.get(f"/users/127902260/projects/{uri_id}/items")
    folders = response.json()
    pages = int(folders['paging']['last'].split('=')[-1])
    return pages

def folder_items_response(client, uri_id):
    """
    Response all the items folders and videos in this folder
    """
    
    folder_response_data_list = []
    pages = folder_page_response(client, uri_id)
    for i in range(1, pages + 1):
        response = client.get(f"/users/127902260/projects/{uri_id}/items?page={i}")
        folder_response_data_list.append(response.json()['data'])
        
    return folder_response_data_list

def videos_response(client, uri_id):
    """
    Response only to list all the videos in the folders
    """
    
    video_response_data_list = []
    pages = folder_page_response(client, uri_id)
    for i in range(1, pages + 1):
        response = client.get(f"/users/127902260/projects/{uri_id}/videos?page={i}")
        video_response_data_list.append(response.json()['data'])
        
    return video_response_data_list


def check_if_video_is_downloaded(client, uri_id):
    pass