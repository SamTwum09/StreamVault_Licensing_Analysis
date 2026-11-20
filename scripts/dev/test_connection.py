from pathlib import Path
import os
import requests
from dotenv import load_dotenv

# 1. Load variables from the .env file
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_PROJECT_ROOT / ".env")

# 2. Retrieve the API key without displaying it
api_key = os.getenv("TMDB_API_KEY")

# 3. Check whether the key was loaded
if not api_key:
    raise ValueError("TMDB API key not found. Check your .env file.")

print("API key loaded successfully.")

# 4. Connect to TMDb
url = "https://api.themoviedb.org/3/configuration"

params = {
    "api_key": api_key
}

response = requests.get(url, params=params, timeout=30)

# 5. Check the API response
if response.status_code == 200:
    print("TMDb connection successful!")
    print("API status:", response.status_code)
else:
    print("Connection failed.")
    print("Status code:", response.status_code)
    print("Response:", response.text[:500])
