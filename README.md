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

2. In your terminal, enter the following commands

Linux:
```console
$ python3 -m venv .venv
$ . .venv/bin/activate
```
Windows:
```console
$ py -3 -m venv .venv
$ .venv\Scripts\activate
```
> ***You should now be running in a python virtual environment***

3. Install the needed dependencies
```console
$ pip install -r requirements.txt
```

5. Setup Database
```console
$ flask init-db
```

6. Run the App
```console
$ flask run 
```

## Notes/Config

##### Config
Several things that you can config (config must be created at `instance/config.py`):
```
SECRET_KEY='<YOUR_SECRET_KEY>'
MAX_CONTENT_LENGTH = <YOUR_SIZE> * 1024 * 1024
```
`MAX_CONTENT_LENGTH` can be configured for size limit. The syntax is as follows
``` <Size> * [KBytes (1024)] * [MBytes (1024)] * <...> ```
If needed, may add more 1024 for GB, TB, etc.
`<Size>` is your desired size, for example 5 kb means put 5.

##### Guide
1. By Default, there's no default user. Create one first.
2. Register user first.
3. Then login using the previously registered user.