# Feistel Cipher URL Shortener

A URL shortener that obfuscates sequential database IDs with a symmetric Feistel cipher and Base62 encoding. It produces compact, collision-free short codes while preventing URL enumeration and predictable analytics.

## Overview
This project stores long URLs and maps them to short codes by:

- writing each URL to the database to obtain an auto-incrementing ID,
- applying a reversible Feistel cipher to obfuscate the numeric ID,
- encoding the obfuscated value in Base62,
- resolving the short code back to the original URL with a direct lookup.

## Key components
- `shortener/utils.py`: Feistel cipher implementation and Base62 encoder/decoder.
- `shortener/models.py`: persistent URL storage.
- `shortener/views.py`: API and redirect handling.
- `main/settings.py`: SQLite configuration for local development.

## How it works
1. Submit a long URL.
2. Store the URL and receive an auto-increment database ID.
3. Scramble the ID with the Feistel cipher into a pseudo-random 32-bit value.
4. Encode the scrambled value in Base62 to generate the short code.
5. Redirect requests for `/{short_code}` back to the stored URL.

## Usage
- API: POST to `/api/shorten/` with `long_url`.
- Web: use the home page form if available.
- Redirect: visit `/{short_code}` to reach the original URL.

## Design considerations
- **Feistel cipher** avoids exposed sequential IDs and makes short codes hard to enumerate.
- **Base62 encoding** keeps codes compact and URL-safe.
- **SQLite** keeps the project simple for local development.

## Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Notes
This implementation is optimized for simplicity and local development. In a production deployment, replace SQLite with a production database and secure the encryption key material appropriately.
