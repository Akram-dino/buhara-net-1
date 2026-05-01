import requests

API_KEY = "I4Cgw4EMQdi2yf9hGcCE"
MODEL_ID = "tea-7vpyp/1"
IMAGE_PATH = "test.webp"

# try classification first
url = f"https://classify.roboflow.com/{MODEL_ID}"

with open(IMAGE_PATH, "rb") as image_file:
    response = requests.post(
        url,
        files={"file": image_file},
        params={"api_key": API_KEY},
        timeout=60
    )

print(response.status_code)
print(response.text)