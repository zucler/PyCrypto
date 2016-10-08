# PyCrypto
Python-powered trading algorithm for crypto currency markets.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.


### Prerequisites (Assuming Mac is used):

- MySQL server (default port)

- DB user (see python header for login/pass)

- DB schema as per pycrypto.sql

- Python environment with libraries listed in *pip_libraries.txt*

 - To install all packages with pip run:

   ```
   pip install -r path/to/pip_libraries.txt
   ```

### Installing

Create a new file _settings.py_.

Copy the contents from _settings.default.py_ into the new file.

Update the settings in new file to match your setup:

```
#Set your DB connection details below:
DATABASE = {
    'USER': 'pycrypto',
    'PASSWORD': 'crypto098',
    'HOST': 'localhost',
    'PORT': '3306',
    'SCHEMA': "pycrypto"
}
```
