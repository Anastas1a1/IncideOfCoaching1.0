from __future__ import print_function

import io

import os
import shutil
import google.auth
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
import httplib2
# from googleapiclient import discovery, errors
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseDownload

load_dotenv()
CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE')
diskId = os.getenv('diskId')
from . import db

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,  'https://www.googleapis.com/auth/drive')

httpAuth = credentials.authorize(httplib2.Http())
service = build('drive', 'v3', http = httpAuth)


def list_files_recursively(folder_id=diskId, prefix=''):
    page_token = None
    while True:
        try:
            query = "'{}' in parents".format(folder_id)
            results = service.files().list(
                q=query,
                pageSize=10,
                fields="nextPageToken, files(id, name, mimeType, webViewLink)",
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
                        path = prefix.split('/')
                        if len(path) < 4:
                            path.append('-')

                        name = file["name"]

                        db.add_google_file(
                            year=path[1],
                            category=path[2],
                            topic=path[3],
                            title=name,
                            google_id=file["id"],
                            link=file["webViewLink"]
                        )
                        
        except Exception as e:
            print("Произошла ошибка:", str(e))

        page_token = results.get('nextPageToken')
        if not page_token:
            break