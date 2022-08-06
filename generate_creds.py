from pydrive.auth import GoogleAuth
from os import path
import os

if path.exists("client_secrets.json"):
    gauth = GoogleAuth()

    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("credentials.json")
    os.remove("client_secrets.json")
else:
    print("client_secrets.json file not found")
    exit()
