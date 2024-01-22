Program:
1. Within first execution the program sends the user to authenticate his google account, in order to create a token with permissions needed for the script's scopes
2. The program uses the available token credentials to connect to the user's drive via Google Drive API 
3. The program lists files the user owns in his drive, and provides each file's sharing information
4. The program will add at the end the user's default sharing settings created for new files he creates
5. The program provide an option to secure files within public folders in the user's drive (-s, --secure-files)
	with this option the program checks if files are in a publicly accessible folder, and if so makes the file private to the user.

All output is printed to output.txt within same path where script is executed. 


Prerequisites :
1. Python 3.10.7 or greater
2. A Google account with google drive enabled
3. A Google Cloud Project
4. pip - package management tool
	Following packages installed:
		google-api-python-client
		google-auth-httplib2
		google-auth-oauthlib


Required Steps:
In order for the user to use the Program, the user has to follow the following steps within https://developers.google.com/drive/api/quickstart/python#set_up_your_environment
This in order to enable the Google Drive API and configure google authentication process
1. Enable the API (Google Drive API)
2. Configure the OAuth consent screen
3. Authorize credentials for a desktop application
4. Install the Google client library


Script Permissions:
The script requests permissions for the following scopes:
1. drive - permissions to view and manage all of your Drive files.
2. drive.metadata - permissions to view and manage metadata of files in user's drive

Within first execution the script will send the user to authentication page and will request permissions mentioned above. After first authentication the script creates 'token.json' file within path which will provide the confirmed permissions for further executions. 

Within first execution google authentication page will warn the user that this program is not verified by google. 

Execution - 
1. The scripts has to be executed in path where credentials.json is saved from step "Authorize credentials for a desktop application"
2. Possible executions command lines:
python drive_client.py
python drive_client.py -s 


sample outputs:

-- output example for a file that has a few sharing permissions, with one public

preload.js - 1Ze3JeSYN-4cnSf5rDnDWokdjJ8gmfDeS - text/javascript
Sharing Status:
user - writer - krissihatespotato@gmail.com
anyone - reader
 --- Publicly Accessible!
 ------------------


 -- output example for a file that is private to the user

pupmain windows.js - 1pTBp4lnj5d1y2YgjM8jT7ytYl0acVcJN - text/javascript
Sharing Status:
Private
 ------------------ 

 -- output example for a file that is located inside a publicly accessible folder, and the program converted his permissions to private to the user

 preload.js - 1Ze3JeSYN-4cnSf5rDnDWokdjJ8gmfDeS - text/javascript
Sharing Status:
user - writer - krissihatespotato@gmail.com
anyone - reader
 --- Publicly Accessible!
2 permissions were removed -> file is now private to you
 ------------------ 




Possible Further Improvements - 
1. Efficiency -
Currently the program sends an HTTP request for every action (for example every permission query / delete). 
Batch requests can be used in order to improve HTTP payload created by the program.
2. validation of multiple owners - 
Currently the program expects that each file/folder will have one owner. Potentially the program can validate that files/folders don't have multiple owners. 

