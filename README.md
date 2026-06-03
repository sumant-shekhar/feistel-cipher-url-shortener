# Feistel Cipher URL Shortener

A collision-free URL shortener that obfuscates auto-incremented database IDs using a symmetric Feistel cipher before Base62 encoding. This prevents URL enumeration attacks and business metric leaks without the database overhead of hash-collision checks.

## Current Implementation
The project is fully functional and uses:
- **Django 6.0**: Core framework.
- **Django Rest Framework**: For the `api/shorten/` endpoint.
- **Custom Feistel Cipher**: A 32-bit block cipher implemented in `utils.py` to scramble sequential database IDs.
- **Base62 Encoding**: To convert scrambled IDs into compact short codes (max 6 characters).
- **SQLite**: Used for local development (configured in `settings.py`).

### How to use
1. **API**: POST to `/api/shorten/` with `long_url`.
2. **Web**: Use the home page form.
3. **Redirect**: Access `/{short_code}` to be redirected to the original URL.

## Architectural Trade-Offs

* **Why Feistel + Base62:** Traditional hashing algorithms (MD5/SHA) cause collisions that require expensive database lookups at scale. Exposing raw sequential IDs invites scraping. This approach balances $O(1)$ database lookup speeds with cryptographic obfuscation.
* **Limitations:** Introduces minor CPU overhead for bitwise operations per request. The block size must be constrained to keep the encoded output string short.

## Mathematical Core

The cipher splits the integer bit-block into left ($L$) and right ($R$) halves, executing over $i$ rounds:

$$L_i = R_{i-1}$$
$$R_i = L_{i-1} \oplus F(R_{i-1}, K_i)$$

The round function $F$ utilizes a pseudo-random bit-shuffling mechanism driven by a static internal key $K$.

# 🔗 Cipher URL Shortener

A high-performance URL shortener built with Django and Python. Instead of auto-incrementing public IDs or saving random strings in a database, this project secures internal database IDs using a Format-Preserving Feistel Cipher combined with Base62 encoding.

## 🚀 Technical Architecture
1. **Database Entry**: Stores the long URL and retrieves a standard sequential Auto-ID (e.g., `105`).
2. **Feistel Cipher**: Scrambles the sequential ID into a pseudo-random, non-sequential 32-bit integer using a private secret key. This prevents competitive intelligence or URL scanning attacks.
3. **Base62 Encoding**: Encodes the scrambled large integer into a highly compact alphanumeric short code string (using characters `0-9`, `a-z`, `A-Z`).

## 🛠️ Installation & Setup

This project uses **uv** by Astral for lightning-fast dependency and environment management.

### Prerequisite: Install uv
```bash
# macOS/Linux
curl -LsSf https://astral.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh | iex"
```

### Setup Environment
1. Clone this repository and navigate to the folder.
2. Initialize and sync the virtual environment dependencies automatically:
   ```bash
   uv sync
   ```

### Running the Application
Apply migrations and boot up the Django development server:
```bash
uv run python manage.py migrate
uv run python manage.py runserver
```
