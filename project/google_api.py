# -*- coding: utf-8 -*-
"""
Created on Sunday May 8 2022

@author: Baptiste Bordet : https://orcid.org/0000-0002-9994-7813

This file is part of ALWIC-tool.

ALWIC-tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

ALWIC-tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ALWIC-tool. If not, see http://www.gnu.org/licenses

this code is adpated from : "https://www.thepythoncode.com/article/using-google-drive--api-in-python", written by "https://github.com/x4nth055"
"""

import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import requests
from tqdm import tqdm

# If modifying these scopes, delete the file token.pickle.
# Scopes are authorisations to write, read, and modify files in google drive
SCOPES = ['https://www.googleapis.com/auth/drive.metadata',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file'
          ]

def get_gdrive_service():
    """
    Initiate the connexion with google drive through API. 
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_code.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    return build('drive', 'v3', credentials=creds)

def search_folder(service, query):
    """
    Search a folder in the google drive. 
    Parameters
    ----------
    service : Service
        Google drive API. 
    query : str
        Folder to search in 

    Returns
    -------
    result : str
        Folder name

    """
    # search for the file
    result = []
    page_token = None
    while True:
        response = service.files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                        spaces="drive", pageToken=page_token,).execute()
        # iterate over filtered files
        for file in response.get("files", []):
            result.append((file["id"], file["name"], file["mimeType"]))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            # no more files
            break
    for resulte in result:
        if resulte[1]==query:
            result=resulte
            break
    return result

def upload_files(filepath,filename,query="Treated_data"):
    """
    Upload a file into a google drive folder 

    Parameters
    ----------
    filepath : str
        Path to the file.
    filename : str
        File to upload (with extension)
    query : str, optional
        folder where upload is made. The default is "treated_data".

    Returns
    -------
    None.

    """
    # authenticate account
    service = get_gdrive_service()
    # search the folder
    folder = search_folder(service, query)
    # get the folder id
    folder_id = folder[0]
    # upload a file text file
    # first, define file metadata, such as the name and the parent folder ID
    file_metadata = {
        "name": filename,
        "parents": [folder_id]}
    # upload
    media = MediaFileUpload(filepath+"/"+filename, resumable=True)
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        


def search(service, query):
    """
    Search a file in google drive 

    Parameters
    ----------
    service : Service
        Google drive API.
    query : str
        Filename formated to google drive API format 

    Returns
    -------
    result : list
        Contains the location of the query     

    """
    # search for the file
    result = []
    page_token = None
    while True:
        response = service.files().list(q=query,
                                        spaces="drive",
                                        fields="nextPageToken, files(id, name, mimeType)",
                                        pageToken=page_token).execute()
        # iterate over filtered files
        for file in response.get("files", []):
            result.append((file["id"], file["name"], file["mimeType"]))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            # no more files
            break
    return result

def download_file_from_google_drive(id, destination):
    """
    Download a file from google drive into destination 

    Parameters
    ----------
    id : list
        Informations needed to retreive the file on google drive 
    destination : str
        Where to dowload file 

    Returns
    -------

    """
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768
        progress = tqdm(response.iter_content(CHUNK_SIZE), unit="Byte", unit_scale=True, unit_divisor=1024,disable=True)
        with open(destination, "wb") as f:
            for chunk in progress:
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # update the progress bar
                    #progress.update(len(chunk))
        progress.close()

    # base URL for download
    URL = "https://docs.google.com/uc?export=download"
    # init a HTTP session
    session = requests.Session()
    # make a request
    response = session.get(URL, params = {'id': id}, stream=True)
    # get confirmation token
    token = get_confirm_token(response)
    if token:
        params = {'id': id, 'confirm':token}
        response = session.get(URL, params=params, stream=True)
    # download to disk
    save_response_content(response, destination)  

def download(filename):
    """
    Wrapper to dowload a file with a name. 

    Parameters
    ----------
    filename : str
        Name of the file to download.

    Returns
    -------
    error : int
        If the file is not found this raise this error

    """
    service = get_gdrive_service()
    # the name of the file you want to download from Google Drive 
    filename=filename+".csv"
    # search for the file by name
    search_result = search(service, query=f"name='{filename}'")
    if search_result==[]:
        error=1
        return error
    # get the GDrive ID of the file
    file_id = search_result[0][0]
    # make it shareable
    service.permissions().create(body={"role": "reader", "type": "anyone"}, fileId=file_id).execute()
    # download file
    download_file_from_google_drive(file_id, "./files/raw_files_temp/"+filename)
    

    