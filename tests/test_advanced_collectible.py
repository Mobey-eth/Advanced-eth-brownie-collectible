import pytest
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
)
from brownie import network
from scripts.deploy_and_create import run_script


def test_can_create_advanced_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("for local testing.")
    account = get_account()
    advanced_collectible, creating_tx = run_script()
    # nft = advanced_collectible.createCollectible({"from": account})
    request_id = creating_tx.events["requestedCollectible"]["requestId"]
    STATIC_RANDNUM = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RANDNUM, advanced_collectible.address, {"from": account}
    )
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.ownerOf(0) == get_account()
    assert advanced_collectible.tokenIdToBreed(0) == STATIC_RANDNUM % 3
    assert advanced_collectible.tokenIdToBreed(0) == 0
