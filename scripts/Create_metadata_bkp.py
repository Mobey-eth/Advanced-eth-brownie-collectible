import json
from brownie import AdvancedCollectible, network
from metadata.sample_metadata import metadata_template
from scripts.helpful_scripts import get_breed
from pathlib import Path
import requests


def upload_to_ipfs(file_path):
    with Path(file_path).open("rb") as fp:
        image_binary = fp.read()
        # Upload stuff, be aware of curl
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # "./img/pug.png" -> "pug.png"
        file_name = file_path.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={file_name}"
        print(image_uri)
        return image_uri


def create_metadata():
    advanced_collectible = AdvancedCollectible[-1]
    print(advanced_collectible.address)
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_collectibles} collectibles")
    # @dev needs to range to get the tokenID
    for token_id in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_filename = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        # Initialize mapping
        collectible_metadata = metadata_template
        if Path(metadata_filename).exists():
            print(f"{metadata_filename} already exists, delete it to override")
        else:
            print(f"Creating metadatafile {metadata_filename}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} puppy!"
            # Set the Image URI with an upload to IPFS fxn
            # image_uri = upload_to_ipfs(image_path)
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image-URI"] = image_uri
            with open(metadata_filename, "w") as file:
                json.dump(collectible_metadata, file)
            metadata_uri = upload_to_ipfs(metadata_filename)
            print("Our meatadata URI is ", metadata_uri)


# Image URI = https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png
# metadata URI = https://ipfs.io/ipfs/QmWzWJJpYxm3zjYEFMPRzsHkbdGNHpaTz9PZ1jni198fdr?filename=0-ST_BERNARD.json
def main():
    create_metadata()
