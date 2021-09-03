from __future__ import print_function
import os

from oauth2client import client  # type: ignore
from oauth2client import tools
from oauth2client.file import Storage  # type: ignore
import argparse
import typing

try:
    flags: typing.Union[None, argparse.Namespace] = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class Auth:
    def __init__(self, scopes: str, client_secret_file: str, application_name: str) -> None:
        self.SCOPES = scopes
        self.CLIENT_SECRET_FILE = client_secret_file
        self.APPLICATION_NAME = application_name

    def get_credentials(self) -> tools.client:
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
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            credentials = tools.run_flow(flow, store, flags)
            print("Storing credentials to " + credential_path)
        return credentials
