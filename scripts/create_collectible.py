from brownie import AdvancedCollectible
from scripts.helpful_scripts import get_account, fund_with_link


def create_collectible():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address)
    tx = advanced_collectible.createCollectible({"from": account})
    tx.wait(1)
    print(f"Done, collectible created at {advanced_collectible.address} !")


def main():
    create_collectible()
