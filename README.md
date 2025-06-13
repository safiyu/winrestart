# winrestart
a flask server that can be accessed remotely using a webui to restart your windows

# Installation
Add the below trigger conditions to windows task scheduler to start at every startup
```
program\script : cmd
arguments: /c "cd path\to\winrestart && pip install flask && python app.py > output.log 2>&1"
```
Replace path\to\winstart with the path of the app directory.

# User credentials
Default values {username: admin, password: winrestart}
You can configure config.py to store the username password. Since the password is not in the main app script, it is safe to store it. Make sure to reset this file before pushing to the repo.

# Docker
Running this program as docker container will work only if your docker engine OS is type windows and not linux. A dockerfile is included if you wish to dockerize.

## License
This project is licensed under the [GNU General Public License v3.0](LICENSE).

