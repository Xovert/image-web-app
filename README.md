# Image Web App

A Simple Web App for Uploading Images
The design is very human.

## Dependencies

This app requires python>=3.8 to run. If you don't have python, install it first.

## How-to-run

1. Clone this repository and switch directory to the cloned repo
```console
$ git clone https://github.com/Xovert/image-web-app.git
$ cd image-web-app
```

2. In your terminal, enter this command
```console
$ python3 -m venv .venv
$ . .venv/bin/activate
```
You should now be running a python virtual environment

3. Install the needed dependencies
```console
$ pip install -r requirements.txt
```

5. Setup Database
```console
$ flask --app imgwebapp init-db
```

6. Run the App
```console
$ flask --app imgwebapp run 
```

### Notes/Config

##### Config
Several things that you can config (config can be found at `instance/config.py`):
```
SECRET_KEY='[input_your_secret_key]'
MAX_CONTENT_LENGTH = [your_size] * 1024*1024
```
`MAX_CONTENT_LENGTH` can be configured for size limit. The syntax is as follows
``` [Size] * [Bytes (1024)] * [KBytes (1024)] * <...> ```
If needed, may add more 1024 for MB, GB, etc.
`[Size]` is your desired size, for example 5 kb means put 5.

##### Guide
1. Register user first
2. Then login using that user