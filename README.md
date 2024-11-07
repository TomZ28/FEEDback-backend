# FEEDback-backend
Backend service for "FEEDback", a restaurant social media website. It is written in Python with the [Django](https://www.djangoproject.com/) web framework.

## Setup
This server requires `Python 3.10` to run. You can download it from [the official Python website](https://www.python.org/downloads/).

First, change directory into the app.
```
$ cd src/FEEDback
```

Then, run the setup script.
```
$ ./setup.sh
```

If test data is needed, uncomment the following line in `setup.sh`, or run it in your terminal if you already ran the script:
```
echo 'import generate_data' | python manage.py shell
```

## Running the Server (Locally)
To run the server locally in developer mode, run the startup script:
```
$ ./run.sh
```
This should run the server on a local URL, such as `http://127.0.0.1:8000/`.

## API Documentation
This app includes [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/) for documentation.

You can visit the `/swagger/` or `/redoc/` endpoints to view the documentation.

For example, if the server is running on `http://127.0.0.1:8000/`, visit `http://127.0.0.1:8000/swagger/`.
