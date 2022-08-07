from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import get_account, get_breed, opensea_url

dog_metadata_dic = {
    "PUG": "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "ipfs://QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "ipfs://QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}


def set_tokenUri(tokenId, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(tokenId, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome job, you can veiw your nft at {opensea_url.format(nft_contract.address, tokenId)}"
    )
    print("Please wait some time and do well to refresh")


def main():
    print(f"working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {number_of_collectibles} collectibles")
    for tokenId in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(tokenId))
        if not advanced_collectible.tokenURI(tokenId).startswith("https://"):
            print(f"Setting tokenURI of {tokenId}")
            set_tokenUri(tokenId, advanced_collectible, dog_metadata_dic[breed])
