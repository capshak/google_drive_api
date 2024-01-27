import os.path
import argparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata",
    'https://www.googleapis.com/auth/drive']


def is_public(permission):
    """function recieves a permission object,
    checks if grants public access
    """
    if permission['type'] == 'anyone':
        if 'deleted' not in permission.keys() or not permission['deleted']:
            return True

    return False


def permissions_check(permissions_list):
    """
    The functione recieves the permissions list collected from a file
    - will iterate the file's permissions and provide sharing status
    - indicates public access if detects a permission to 'anyone'
    returns list of output lines (sharing _status)
    """
    public_flag = False
    sharing_status = ['Sharing Status:']

    for per in permissions_list:
        # skips owner permission
        if per['role'] != 'owner':
            permissions_str = f"{per['type']} - {per['role']}"
            if 'emailAddress' in per.keys():
                permissions_str += f" - {per['emailAddress']}"

            # appending permission output
            sharing_status.append(permissions_str)

            # monitors existence of public permission
            if not public_flag and is_public(per):
                public_flag = True

    if public_flag:
        sharing_status.append(' --- Publicly Accessible!')

    if len(sharing_status) == 1:
        sharing_status.append('Private')

    return sharing_status


def list_files(service, files):
    """
    Function will use the Drive API to list files in the users' drive
    function filters for files the user owns and excludes folders
    function returns files as a list
    """
    page_token = None
    while True:
        results = (
            service.files()
            .list(
                spaces='drive',
                pageToken=page_token,
                q="'me' in owners and not mimeType = \
                'application/vnd.google-apps.folder'",
                fields=(
                    "nextPageToken, files(id, name, parents, "
                    "mimeType, owners, permissions)"
                    )
                )
            .execute()
        )
        files.extend(results.get("files", []))

        # Drive returns 100 rows for each request
        # nextPageToken returned within response to indicate more rows
        page_token = results.get("nextPageToken", None)
        if page_token is None:
            break

    return files


def get_public_folders(service):
    """
    Function lists folders within the users' drive
    function iterates the folders and collects ids of
        folders with public access
    """
    page_token = None
    public_folders_ids = []
    folders = []
    while True:
        results = (
            service.files()
            .list(
                spaces='drive',
                pageToken=page_token,
                q="mimeType = 'application/vnd.google-apps.folder'",
                fields=(
                    "nextPageToken, files(id, name, mimeType, "
                    "owners, permissions)"
                    )
                )
            .execute()
        )
        folders.extend(results.get("files", []))

        page_token = results.get("nextPageToken", None)
        if page_token is None:
            break

    for folder in folders:
        if 'permissions' in folder.keys():
            for per in folder['permissions']:
                if is_public(per):
                    public_folders_ids.append(folder['id'])
                    break

    return public_folders_ids


def secure_file(service, file):
    """
    Function recieves a file object
    function uses Drive API to delete all
        permissions except owner's permission
    """
    not_owner_permissions = []
    permissions_deleted = 0

    # exclude owner permission
    for perm in file['permissions']:
        if perm['role'] != 'owner':
            not_owner_permissions.append(perm['id'])

    try:
        for permission_id in not_owner_permissions:
            service.permissions().delete(
                    fileId=file['id'],
                    permissionId=permission_id
                    ).execute()
            permissions_deleted += 1

    except HttpError as error:
        output = f"An error occurred: {error}"
        print(output)

    return permissions_deleted


def retrieve_default_sharing(service):
    """
    Function creates an empty file
    checks for default created permissions
    deletes the file and returns results
    """
    try:
        newFile = (service.files().create().execute())

        newFilePermissions = (service.permissions().list(
            fileId=newFile.get('id')).execute())

        sharing_status = permissions_check(
            newFilePermissions.get('permissions')
            )

        # deleting the file
        service.files().delete(
            fileId=newFile.get('id')).execute()

        if len(sharing_status) == 1:
            return ['The file is private to you']
        else:
            return sharing_status

    except HttpError as error:
        output = f"An error occurred: {error}"
        print(output)


def main():
    arg_parser = argparse.ArgumentParser(
        prog='DriveClient',
        description=(
            'program lists files in your drive '
            'and provide related sharing status'
            )
        )

    arg_parser.add_argument(
        '-s',
        '--secure-files',
        action='store_true',
        help=(
            'if selected, program turns files within '
            'public folders to private'
            )
        )

    args = arg_parser.parse_args()

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the
    # first time.
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    output_lines = ['Files:']
    public_folders = []
    files = []
    try:
        service = build("drive", "v3", credentials=creds)
        output = ""
        public_folders.extend(get_public_folders(service))
        files.extend(list_files(service, files))

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        output = f"An error occurred: {error}"
        output_lines.append(output)

    if not files:
        output_lines.append("No Files found.")
        return

    else:
        for item in files:
            output = f"{item['name']} - {item['id']} - {item['mimeType']}"

            output_lines.append(output)

            # providing sharing status for file
            output_lines.extend(permissions_check(item['permissions']))

            # checking need to secure file in a public folder
            if (
                args.secure_files and
                'parents' in item.keys() and
                item['parents'][0] in public_folders
            ):
                permissions_deleted_count = secure_file(service, item)

                # if called secure_file and permissions were deleted -
                #   indicating output
                if permissions_deleted_count > 0:
                    output_lines.append(
                        f"{permissions_deleted_count} "
                        "permissions were removed -> "
                        "file is now private to you")

            output_lines.append(' ------------------ ')

    output_lines.extend(
        ['Default Sharing for new files:']
        + retrieve_default_sharing(service))

    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))


if __name__ == "__main__":
    main()
