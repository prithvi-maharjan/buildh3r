
from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,   
)

algorand = AlgorandClient.default_local_net()

dispenser = algorand.account.dispenser()
print("Dispenser Address", dispenser.address)
print("Dispenser Account Info:", algorand.account.get_information(dispenser.address))
print("")

creator = algorand.account.random()
print("Creator Address:", creator.address)
algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )
)
print("Creator Account Info:", algorand.account.get_information(creator.address))

asset_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=1000,
        asset_name="BUILDH3R_ASSET",
        unit_name="ETH",
        manager=creator.address,
        clawback=creator.address,
        freeze=creator.address
    )
)
asset_id = asset_txn["confirmation"]["asset-index"]
print("Asset ID:", asset_id)
print("Creator Account Info After Creating Asset:", algorand.account.get_information(creator.address))
print("")

print("Receiver Account Info After Funding:")
receivers = [algorand.account.random() for _ in range(3)]
for i, receiver in enumerate(receivers, start=1):  
    algorand.send.payment(
        PayParams(
            sender=dispenser.address,
            receiver=receiver.address,
            amount=10_000_000
        )
    )

for i, receiver in enumerate(receivers, start=1):    
    print(f"Receiver {i} Account Info:", algorand.account.get_information(receiver.address))

print("")

for i, receiver in enumerate(receivers, start=1):
    group_txn = algorand.new_group()

    group_txn.add_asset_opt_in(
        AssetOptInParams(
            sender=receiver.address,
            asset_id=asset_id
        )
    )

    group_txn.add_asset_transfer(
        AssetTransferParams(
            sender=creator.address,
            receiver=receiver.address,
            asset_id=asset_id,
            amount=100
        )
    )

    group_txn.execute()

print("Receiver Account Info After Transferring Assets:")

for i, receiver in enumerate(receivers, start=1):
    receiver_info = algorand.account.get_information(receiver.address)
    print(f"Receiver {i} Account Info:", receiver_info)

for i, receiver in enumerate(receivers, start=1):
    balance = algorand.account.get_information(receiver.address)['assets'][0]['amount']
    print(f"Receiver {i} Asset Balance:", balance)