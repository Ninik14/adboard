# GeoBazaar

## Create virtual environment

```bash
python -m venv env
```

## Activate virtual environment

macOS/Linux

```bash
source env/bin/activate
```

Windows

```bash
env\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Apply migrations

```bash
python manage.py migrate
```

## Run the server

```bash
python manage.py runserver
```