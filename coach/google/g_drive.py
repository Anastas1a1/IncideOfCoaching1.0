from __future__ import print_function

import io

import os
import shutil
import google.auth
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseDownload

load_dotenv()
CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE')
diskId = os.getenv('diskId')
from coach.bot import db


credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,  'https://www.googleapis.com/auth/drive')

httpAuth = credentials.authorize(httplib2.Http())
service = build('drive', 'v3', http = httpAuth)



# def download_file(file_name, file_Id):
#     try:
#         request = service.files().get_media(fileId=file_Id)
#         file = io.FileIO(file_name, 'wb')
#         downloader = MediaIoBaseDownload(file, request)
#         done = False
#         while done is False:
#             status, done = downloader.next_chunk()
#             print(F'\tЗагрузка {int(status.progress() * 100)}.')     
                
#     except HttpError as error:
#         print(F'An error occurred: {error}')
#         file = None



# def list_files_recursively(folder_id, prefix):
#     page_token = None
#     while True:
#         try:
#             query = "'{}' in parents".format(folder_id)
#             results = service.files().list(
#                 q=query,
#                 pageSize=10,
#                 fields="nextPageToken, files(id, name, modifiedTime, mimeType, webViewLink)",
#                 pageToken=page_token
#             ).execute()
#             files = results.get('files', [])
#             if not os.path.exists(prefix):
#                 os.makedirs(prefix)

#             if not files:
#                 print('Файлов не найдено.')
#             else:
#                 # print(f'Список файлов в папке "{prefix}":')
#                 for file in files:
#                     if file['mimeType'] == 'application/vnd.google-apps.folder' or file['mimeType'] =='application/vnd.google-apps.shortcut':

#                         # doc_to_db = ['-', file["name"], '-', '-', file["id"], file["modifiedTime"] ]
                        
#                         list_files_recursively(file['id'], prefix + '/' + file['name'])
#                     else:
#                         # print(f'{file["name"]} ({file["id"]})    {file["mimeType"]}')
#                         print(prefix)
#                         path = prefix.split('/')
#                         # print(path)

#                         if path[2]=='Договор' or path[2]=='Дегустационное меню':
#                             path.append('-')

#                         doc_to_db = [path[1], path[2], path[3], file["name"], file["id"], file["modifiedTime"], file["webViewLink"] ]
#                         download_flag = server.new_doc(doc_to_db)

#                         file_name = prefix + '/' + file["name"]
#                         # if not os.path.exists(file_name) or download_flag:
#                         #     print('download ', file_name)
#                         #     download_file(file_name, file["id"])
#                         # else:
#                         #     print('not download')

#         except Exception as e:
#             print("Произошла ошибка:", str(e))

#         page_token = results.get('nextPageToken')
#         if not page_token:
#             break



# def new_month(folder_name, folder_serv):
#     # if not os.path.exists(CREDENTIALS_FILE):
#     #     raise FileNotFoundError(f'Файл {CREDENTIALS_FILE} не найден')

#     query = "name='{}' and mimeType='application/vnd.google-apps.folder'".format(folder_name)
#     results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
#     items = results.get('files', [])
#     if not items:
#         print(f'Папка с названием "{folder_name}" не найдена.')
#         return

#     folder_id = items[0]['id']
#     list_files_recursively(folder_id, folder_serv)




#access
# def access_disk(spreadsheetId, email):
#     driveService = discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
#     access = driveService.permissions().create(
#         fileId = spreadsheetId,
#         body = {'type': 'user', 'role': 'writer', 'emailAddress': email},  # Открываем доступ на редактирование
#         fields = 'id'
#     ).execute()






def list_files_recursively(folder_id, prefix):
    page_token = None
    while True:
        try:
            query = "'{}' in parents".format(folder_id)
            results = service.files().list(
                q=query,
                pageSize=10,
                fields="nextPageToken, files(id, name, modifiedTime, mimeType, webViewLink)",
                pageToken=page_token
            ).execute()
            files = results.get('files', [])

            if not files:
                print('Файлов не найдено.')
            else:
                for file in files:
                    if file['mimeType'] == 'application/vnd.google-apps.folder' or file['mimeType'] =='application/vnd.google-apps.shortcut':
                        list_files_recursively(file['id'], prefix + '/' + file['name'])
                    else:
                        # print(prefix)
                        path = prefix.split('/')
                        print(path)
                        print(len(path))
                        if len(path) < 4:
                            path.append('-')
                            print(path)
                            print('______'*20)
                        name = file["name"].replace(' ', '_').replace('-', '_')

                        doc_to_db = [path[1], path[2], path[3], name, file["id"], file["webViewLink"]]
                        # print(doc_to_db)
                        download_flag = db.add_google_file(doc_to_db)
                        # db.add_google_file(year, category, topic, title, google_id, link)

                        file_name = prefix + '/' + file["name"]
 

        except Exception as e:
            print("Произошла ошибка:", str(e))

        page_token = results.get('nextPageToken')
        if not page_token:
            break



def new_month(folder_name, folder_serv):
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(f'Файл {CREDENTIALS_FILE} не найден')

    query = "name='{}' and mimeType='application/vnd.google-apps.folder'".format(folder_name)
    results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print(f'Папка с названием "{folder_name}" не найдена.')
        return

    folder_id = items[0]['id']
    list_files_recursively(folder_id, folder_serv)


new_month('incide_of_coaching', 'docs')