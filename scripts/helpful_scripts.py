from brownie import accounts, network, config, Contract, LinkToken, VRFCoordinatorMock

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "mainnet-fork"]
opensea_url = "https://testnets.opensea.io/assets/{}/{}"
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print("deploying Mocks...")
    account = get_account()

    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})

    # return mock_price_feed.address
    print("Mocks deployed!")


contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """
    This function will grab the contact adresses from the brownie config
    if defined , otherwise it will deploy a mock contract and return that
    mock contract.
        args:
            contract_name (string)
        returns:
            brownie.network.contract.ProjectContract: The most recently
            deployed version of that contract.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            # contract type is same as MockV3Aggregator
            deploy_mocks()
        contract = contract_type[-1]
        # eg. MockV3Aggregator[-1]
    else:
        # else we walk down the config to deploy to testnet
        contract_address = config["networks"][network.show_active()][contract_name]
        # We always need address and the ABI
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # MockV3Aggregator.abi

    return contract


def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    # working with Interfaces!!
    print("Funded link contract")
    return tx


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]
