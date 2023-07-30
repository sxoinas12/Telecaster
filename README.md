# Telecaster Project Instructions

### Fetch repository
#### `git clone http://onarbooks.com/Klapi/Telecaster.git`

## Setup
#### `cd telecaster`

### Install requirments
#### `pip3 install -r requirments.txt`

### How to test?

#### `cd telecaster`

#### `python manage.py runserver`

#### Open postman and perform a `POST` request with the below payload

#### `url: localhost:8000/generate/xml`
```
{
    "url": "prestashop_domain",
    "token": "your_secret_token"
}
```