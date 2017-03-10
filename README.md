# google-sheet-dl
Downloads Google sheets shared with service account as csv


--------------
Authorisation:
--------------

To get the authorisation working:
- Create service account https://developers.google.com/identity/protocols/OAuth2ServiceAccount
- Save JSON Web Token (JWT) for service account to folder called "auth" in program home directory


------------------
Running the script
------------------

Navigate to the folder in which google-sheet-dl.py is located and run "python google-sheet-dl.py <export directory> <file 1> [<file 2> ... <file n>]"
