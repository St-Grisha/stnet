import os
import time
import requests
import argparse

from binance.spot import Spot as Client


def get_deposit_address(eth_amount, stark_address, stark_pubkey=1):
#     eth_amount = 1

    # AUTH
    data_auth = {"client_id": "layerswap_bridge_ui",
    "grant_type": "credentialless"}

    auth_resp = requests.post('https://identity-api.layerswap.io/connect/token', data=data_auth)
    assert auth_resp.status_code == 200, 'Repeat later'
    creds = auth_resp.json()
    creds['expires_in'] = str(creds['expires_in'])

    # INIT
    data = {"n":"Swap initiated",
            "u":f"https://www.layerswap.io/?addressSource=braavos&destAddress={stark_address}&destNetwork=starknet_mainnet&lockNetwork=true&lockAddress=true&from=&to=starknet_mainnet&lockFrom=&lockTo=true",
            "d":"layerswap.io",
            "r":None,
            "p":{}}
    init_resp = requests.post('https://plausible.io/api/event', data=data, headers=creds)
    assert init_resp.status_code == 202, 'Repeat later'


    # GET SWAP ID
    data_swap = {"amount":f"{eth_amount}",
                "source_exchange":"BINANCE",
                "source_network":None,
                "destination_network":"STARKNET_MAINNET",
                "destination_exchange":None,
                "asset":"ETH",
                "destination_address":stark_address,
                "refuel":False}

    header = {'authorization':creds['token_type']+' '+creds['access_token']}
    swap_resp = requests.post('https://bridge-api.layerswap.io//api/swaps', json=data_swap, headers=header)
    assert swap_resp.status_code == 200, 'Repeat later'


    swap_id = swap_resp.json()['data']['swap_id']

    
    # SWAP INFO
    swap_info = requests.get(f'https://bridge-api.layerswap.io//api/swaps/{swap_id}', headers=header)
    
    deposit_address = swap_info.json()['data']['deposit_address']
    return deposit_address, swap_id, header


def binance_withdraw(eth_amount,
                     deposit_address):
    apikey = os.getenv('apikey')
    secret_key = os.getenv('secretkey')


    client = Client(apikey, secret_key)
    client.withdraw('ETH', 
                    amount=eth_amount + 0.000056, # HARDCODE. TODO: Check fee
                    address=deposit_address, 
                    network='BSC')
    
    
def main(eth_amount, stark_address, stark_pubkey, return_starknet_transaction):
    
    deposit_address, swap_id, header = get_deposit_address(eth_amount, stark_address, stark_pubkey)
    binance_withdraw(eth_amount, deposit_address)
    
    return_final = 'Done'
    if return_starknet_transaction:
        
        while return_final == 'Done':
            swap_info = requests.get(f'https://bridge-api.layerswap.io//api/swaps/{swap_id}', headers=header)
            if 'output_transaction' in swap_info.keys():
                return_final = 'https://starkscan.co/tx/'+swap_info['output_transaction']['transaction_id']
            else:
                time.sleep(10)
    return return_final

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Choose address and amount')
    parser.add_argument('eth_amount', type=float, help='Choose amount of ETH to withdraw')
    parser.add_argument('deposit_address', type=str, help='deposit address in starknet')
    #parser.add_argument('starknet_pubkey', type=str, help='starknet pubkey')
    parser.add_argument('starknet_transaction', type=bool, help='print a starknet transaction', 
                        default=False)
    
    
    
    args = parser.parse_args()
    
    return_final = main(args.eth_amount, args.deposit_address, 1, args.starknet_transaction)
    
    print(return_final)
