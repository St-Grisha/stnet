import os
import time
import requests
import argparse

from binance.spot import Spot as Client


def get_deposit_address(eth_amount, stark_address):


    data_init = {"n":"Swap initiated",
        "u":f"https://www.layerswap.io/?destAddress={stark_address}&destNetwork=starknet_mainnet&lockNetwork=true&lockAddress=true&from=&to=starknet_mainnet&lockFrom=&lockTo=true",
        "d":"layerswap.io",
        "r":None,
        "p":{}}
    
    header = {"accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "access-control-request-headers": "access-control-allow-origin,authorization,content-type,x-ls-correlation-id",
    "origin": "https://www.layerswap.io",
    "referer": "https://www.layerswap.io/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
            }
    r2 = requests.post('https://plausible.io/api/event', data=data_init, headers=header)
    print(r2)


    data_r1 = {"client_id": "layerswap_bridge_ui",
    "grant_type": "credentialless"}

    r1 = requests.post('https://identity-api.layerswap.io/connect/token', data=data_r1)
    print(r1)
    creds = r1.json()
    creds['expires_in'] = str(creds['expires_in'])


    data = {"n":"Swap details confirmed",
        "u":f"https://www.layerswap.io/?destAddress={stark_address}&destNetwork=starknet_mainnet&lockNetwork=true&lockAddress=true&from=&to=starknet_mainnet&lockFrom=&lockTo=true",
        "d":"layerswap.io",
        "r":None,
        "p":{}}
    r3 = requests.post('https://plausible.io/api/event', data=data, headers=creds)
    assert r3.status_code == 202



    data = {
    "client_id": "layerswap_bridge_ui",
    "grant_type": "refresh_token",
    "refresh_token": creds["refresh_token"]
    }

    r4 = requests.post(f'https://identity-api.layerswap.io/connect/token', data=data)
    print(r4)



    header = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "access-control-request-headers": "access-control-allow-origin,authorization,content-type,x-ls-correlation-id",
    "access-control-request-method": "POST",
    "origin": "https://www.layerswap.io",
    "referer": "https://www.layerswap.io/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }

    r5 = requests.options('https://bridge-api.layerswap.io//api/swaps', headers=header)
    header_6 ={
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "access-control-allow-origin": "*",
    'authorization':  r4.json()['token_type']+' '+r4.json()['access_token'],
    "content-type": "application/json",
    "origin": "https://www.layerswap.io",
    "referer": "https://www.layerswap.io/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
}

    data_r6 = {"amount":f"{eth_amount}",
            "source_exchange":"BINANCE",
            "source_network":None,
            "deposit_type": "0",
            "destination_network":"STARKNET_MAINNET",
            "destination_exchange":None,
            "asset":"ETH",
            "destination_address":f"{stark_address}",
            "refuel":False}

    swap_resp = requests.post('https://bridge-api.layerswap.io//api/swaps', 
                              headers=header_6, 
                              json=data_r6)
    print(swap_resp.status_code)
    assert swap_resp.status_code == 200, 'Repeat later'

    r7 = requests.get('https://bridge-api.layerswap.io//api/deposit_addresses/BSC_MAINNET?source=0', headers=header_6)
    swap_id = swap_resp.json()['data']['swap_id']
    deposit_address = r7.json()['data']['address']
    # print(swap_id)
    # time.sleep(10)
    # # SWAP INFO
    # swap_info = requests.get(f'https://bridge-api.layerswap.io//api/swaps/{swap_id}', headers=header)
    # print(swap_info.json()['data'])
    # deposit_address = swap_info.json()['data']['deposit_address']
    return deposit_address, swap_id, header_6


def binance_withdraw(eth_amount,
                     deposit_address):
    apikey = os.getenv('apikey')
    secret_key = os.getenv('secretkey')


    client = Client(apikey, secret_key)
    print(float(eth_amount) + 0.000056)
    client.withdraw('ETH', 
                    amount=float(eth_amount) + 0.000056, # HARDCODE. TODO: Check fee
                    address=deposit_address, 
                    network='BSC')
    
    
def main(eth_amount, stark_address):
    
    deposit_address, _, _ = get_deposit_address(eth_amount, stark_address)
    binance_withdraw(eth_amount, deposit_address)
    
    return_final = 'Deposit done'
    return return_final

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Choose address and amount')
    parser.add_argument('eth_amount', type=str, help='Choose amount of ETH to withdraw')
    parser.add_argument('deposit_address', type=str, help='deposit address in starknet')
    
    
    
    args = parser.parse_args()
    
    return_final = main(args.eth_amount, args.deposit_address)
    
    print(return_final)
