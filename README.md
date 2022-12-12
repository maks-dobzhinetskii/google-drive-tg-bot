# Google drive telegram bot app

  

## Description

  

This app allows you to manage your google drive (upload, share, delete files) through telegram bot.

  

## Built with

* Python

* Telebot

* Docker

* PostgreSQL

  

## Getting Started

  

In order to use this app: clone this repository to your machine, in terminal go to project directory and run this commands:

### Start database container with:

```

docker compose up -d --build

```

### Apply latest migration to the database:

```

alembic upgrade head

```

### Run bot application with:

```

python bot_startup.py

```

### Now application is ready.

## Usage tips

Files can be uploaded by 3 different ways:

* Using direct upload of files
* Using zip archives
* Specifying the path to the folder from which you want to upload the files

Files can be shared using google spreadsheets. There you have to include Email and Filename header in first and second columns respectively and starting from second row specify the email - files list pairs. You can specify multiple files in filename section by separating different files with comma.

You also can delete files by:

* Specifying lifetime (in days). Files that are older than specified timedelta will be deleted.
* Clearing all files from your drive

After you started any of the operations you will be prompted to log in to your google account to create connection with your drive and spreadsheets services. If you are not redirected you can just follow link that will appear in terminal. This process may happen twice: first time for drive service and second time for spreadsheets service.

