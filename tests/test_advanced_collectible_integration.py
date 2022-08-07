import pytest
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from brownie import network
from scripts.deploy_and_create import run_script
import time


def test_can_create_advanced_collectible_integration():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Not for local testing.")
    account = get_account()
    advanced_collectible, creating_tx = run_script()
    # nft = advanced_collectible.createCollectible({"from": account})
    time.sleep(250)
    assert advanced_collectible.tokenCounter() == 1
    # assert advanced_collectible.ownerOf(0) == get_account()

    # assert advanced_collectible.tokenIdToBreed(0) == 0
