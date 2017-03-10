from __future__ import print_function
import sys
import argparse
import os

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.service_account import ServiceAccountCredentials


HOME_DIR = os.path.dirname(os.path.realpath(__file__))

# Set up oauth2 constants
OAUTH2_JSON = 'auth/Travelbar-2ff0a8df2e4c.json'
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
creds = ServiceAccountCredentials.from_json_keyfile_name(HOME_DIR + '/' + OAUTH2_JSON,
                                                         SCOPES)
http_auth = creds.authorize(Http())
DRIVE = discovery.build('drive', 'v3', http=http_auth)

SRC_MIMETYPE = 'application/vnd.google-apps.spreadsheet'
DST_MIMETYPE = 'text/csv'


def exportFile(file_name, export_dir):
    """Exports file from Google Drive to specified local directory

	file_name: name of file on Google Drive to export
	export_dir: name of local directory to export to
    """

    files = DRIVE.files().list(
        q='name="%s" and mimeType="%s"' % (file_name, SRC_MIMETYPE),
        orderBy='modifiedTime desc,name').execute().get('files', [])	# Get latest version of file if there are duplicate file names

    if files:
        fn = '%s.csv' % os.path.splitext(files[0]['name'].replace(' ', '_'))[0]	# Clean file path name
        print('Exporting "%s" as "%s"... ' % (files[0]['name'], fn), end='')
        data = DRIVE.files().export(fileId=files[0]['id'], mimeType=DST_MIMETYPE).execute()
        if data:
            with open(export_dir + '/' + fn, 'wb') as f:
                f.write(data)
            print('DONE')
        else:
            print('ERROR: Could not download file')
    else:
        print('ERROR: File not found')


def main():

    # Check if there is a parameter denoting the export directory
    try:
        arg1 = sys.argv[1]
    except IndexError:
        print("Parameter denoting export directory not found")
        raise

    # Check if there is (are) parameter(s) denoting the Google Sheet files to be exported
    file_names = sys.argv[2:]
    if len(file_names) == 0:
        #file_names = TEST_FILE_NAMES
        print("Parameter(s) denoting Google Sheet name(s) not found")
        raise IndexError

    for file in file_names:
        exportFile(file, arg1)


if __name__ == '__main__':
    main()

