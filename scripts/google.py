from __future__ import print_function
import httplib2  # type: ignore
import os

from apiclient import discovery  # type: ignore
from oauth2client import client  # type: ignore
from oauth2client import tools
from oauth2client.file import Storage  # type: ignore
import argparse
import typing

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = "https://www.googleapis.com/auth/drive.metadata.readonly"
CLIENT_SECRET_FILE = "client_secrets.json"
APPLICATION_NAME = "Drive API Python Quickstart"

try:
    flags: typing.Union[None, argparse.Namespace] = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


def get_credentials() -> tools.client:
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, ".credentials")
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "drive-python-quickstart.json")

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print("Storing credentials to " + credential_path)
    return credentials


def main() -> None:
    """Shows basic usage of the Google Drive API.
    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("drive", "v3", http=http)

    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get("files", [])
    if not items:
        print("No files found.")
    else:
        print("Files:")
        for item in items:
            print("{0} ({1})".format(item["name"], item["id"]))


# def uploadFile(filename, filepath):
#     media = MediaFileUpload('files/photo.jpg', mimetype='image/jpeg')
#     file = drive_service.files().create(body=file_metadata,
#                                         media_body=media,
#                                         fields='id').execute()
#     print('File ID: %s' % file.get('id'))


if __name__ == "__main__":
    main()
    # uploadFile('test_image.jpg')
