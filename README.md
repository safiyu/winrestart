# winrestart
a flask server that can be accessed remotely using a webui to restart your windows

# Installation
Add the below trigger conditions to windows task scheduler to start at every startup
'''
program\script : cmd
arguments: /c "cd path\to\winrestart && pip install flask && python app.py > output.log 2>&1"
'''
Replace path\to\winstart with the path of the app directory.

# User credentials
You can configure config.py to store the username password. Since the password is not in the main app script, it is safe to store it. Make sure to reset this file before pushing to the repo.
