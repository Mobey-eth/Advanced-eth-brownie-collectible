import os
from pathlib import Path
import requests

pinata_secret_api_key = os.getenv("PINATA_API_SECRET")
pinata_api_key = os.getenv("PINATA_API_KEY")
PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"
# file_path = "./img/pug.png"
# file_name = file_path.split("/")[-1:][0]
headers = {
    "pinata_api_key": pinata_api_key,
    "pinata_secret_api_key": pinata_secret_api_key,
}


def upload_to_pinata(file_path):
    with Path(file_path).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (file_name, image_binary)},
            headers=headers,
        )
        file_name = file_path.split("/")[-1:][0]
        print(response.json())
        ipfs_hash = response.json()["IpfsHash"]
        image_uri = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
        return image_uri


def main():
    upload_to_pinata()
