import json
import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

google_auth = GoogleAuth()

google_auth.LocalWebserverAuth()
drive = GoogleDrive(google_auth)

def upload():
    headers = {"Authorization": "Bearer ya29.a0ARrdaM-fW6IdnWdu_mt-EXf_lxRU7vJn2Q3Weaf2CpvblUlilX-s9tTJgNo7AjsaOpzoDI-SbGMN96Pbb18Y0x7Td2-AkOUshCCGsh13MSmTU37q_lXLacOhzhkMxHtZXZBXFQvq38XnzMVUruWSfcF-heDj"}
    para = {
        "name": "testfile.png",
    }
    files = {
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': open("./testimage.png", "rb")
    }
    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files
    )
    print(r.text)

upload()


# from __future__ import print_function
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
#
# # If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
#
# def main():
#     """Shows basic usage of the Drive v3 API.
#     Prints the names and ids of the first 10 files the user has access to.
#     """
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())
#
#     service = build('drive', 'v3', credentials=creds)
#
#     # Call the Drive v3 API
#     results = service.files().list(
#         pageSize=10, fields="nextPageToken, files(id, name)").execute()
#     items = results.get('files', [])
#
#     if not items:
#         print('No files found.')
#     else:
#         print('Files:')
#         for item in items:
#             print(u'{0} ({1})'.format(item['name'], item['id']))
#
# if __name__ == '__main__':
#     main()
# # [END drive_quickstart]
#
