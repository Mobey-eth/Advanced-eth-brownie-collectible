from scripts.helpful_scripts import (
    get_account,
    opensea_url,
    get_contract,
    fund_with_link,
)
from brownie import AdvancedCollectible, config, network


def run_script():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )
    fund_with_link(advanced_collectible.address)
    print("Contract funded with Link! @dev!")
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("success @dev! new token has been created")
    # return advanced_collectible, creating_tx


def main():
    run_script()
