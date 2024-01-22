<h1>Program:</h1>
<ol>
<li>Within first execution the program sends the user to authenticate his google account, in order to create a token with permissions needed for the script's scopes</li>
<li>The program uses the available token credentials to connect to the user's drive via Google Drive API </li>
<li>The program lists files the user owns in his drive, and provides each file's sharing information</li>
<li>The program will add at the end the user's default sharing settings created for new files he creates</li>
<li>The program provide an option to secure files within public folders in the user's drive (-s, --secure-files)
	with this option the program checks if files are in a publicly accessible folder, and if so makes the file private to the user.</li>

 </ol>

All output is printed to output.txt within same path where script is executed. 


<h2>Prerequisites :</h2>
<li>Python 3.10.7 or greater</li>
<li>A Google account with google drive enabled</li>
<li>A Google Cloud Project</li>
<li>pip - package management tool</li>
	<p>Following packages installed:<br>
		google-api-python-client<br>
		google-auth-httplib2<br>
		google-auth-oauthlib<br></p>


<h2>Required Steps:</h2>
In order for the user to use the Program, the user has to follow the following steps within https://developers.google.com/drive/api/quickstart/python#set_up_your_environment
This in order to enable the Google Drive API and configure google authentication process
1. Enable the API (Google Drive API)
2. Configure the OAuth consent screen
3. Authorize credentials for a desktop application
4. Install the Google client library


<h2>Script Permissions:</h2>
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


<h2>sample outputs:</h2>

<h5>-- output example for a file that has a few sharing permissions, with one public</h5>

<p>
preload.js - 1Ze3JeSYN-4cnSf5rDnDWokdjJ8gmfDeS - text/javascript <br>
Sharing Status:<br>
user - writer - krissihatespotato@gmail.com<br>
anyone - reader<br>
 --- Publicly Accessible!<br>
 ------------------<br>
</p>

<h5>-- output example for a file that is private to the user</h5>

<p>
pupmain windows.js - 1pTBp4lnj5d1y2YgjM8jT7ytYl0acVcJN - text/javascript<br>
Sharing Status:<br>
Private<br>
 ------------------ <br>
</p>

 <h5>-- output example for a file that is located inside a publicly accessible folder, and the program converted his permissions to private to the user</h5>

<p>
 preload.js - 1Ze3JeSYN-4cnSf5rDnDWokdjJ8gmfDeS - text/javascript<br>
Sharing Status:<br>
user - writer - krissihatespotato@gmail.com<br>
anyone - reader<br>
 --- Publicly Accessible!<br>
2 permissions were removed -> file is now private to you<br>
 ------------------
</p>




<h2>Possible Further Improvements -</h2> 
1. Efficiency -
Currently the program sends an HTTP request for every action (for example every permission query / delete). 
Batch requests can be used in order to improve HTTP payload created by the program.
2. validation of multiple owners - 
Currently the program expects that each file/folder will have one owner. Potentially the program can validate that files/folders don't have multiple owners. 

