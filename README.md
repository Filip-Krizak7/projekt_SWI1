# Booking search engine

Application used for search and book accommodation.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install these packages or switch to venv:

```bash
-   pip install pymysql
-   pip install apify-client
-   pip install uvicorn
-   pip install typer
-   pip install fastapi
-   pip install passlib
-   pip install python-multipart
-   pip install sqlmodel
-   pip install "python-jose[cryptography]"
-   pip install bcrypt
-   pip install npm
-   or run this single command: pip install pymysql, apify-client, uvicorn, typer, fastapi, passlib, python-multipart, sqlmodel, python-jose[cryptography], bcrypt, npm 
```

## Start of backend 
First enter the venv with command: venv/Scripts/Activate.ps1
Then use command: python main.py
Open 'localhost:8000/docs' in your browser

## Start of frontend
You need to have Node.js installed
Switch to 'frontend' folder by: cd frontend
Run 'npm install' if you are going to run the app for the first time
Run 'npm start'

### Read Users Me
Shows information about the logged in user.

### Create User
Used to register a new user.

### Search Hotel
Searches for accommodation according to specified parameters.

### Create Reservation
Used to create reservation foraccommodation according to specified parameters.

### User Reservations
Shows all reservations of the logged in user.

### Cancel reservations
Used to cancel reservation of the logged in user based of the reservation ID.

## License
&Filip Křižák, Martin Šašinka

