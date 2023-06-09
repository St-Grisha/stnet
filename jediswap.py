import os
import time
import subprocess
import argparse


def jediswap(eth_amount, my_address, token_from='ETH', token_to='USDT', wallet='__default__'):
    contract_address = '0x05900cfa2b50d53b097cb305d54e249e31f24f881885aae5639b0cd6af4ed298'

    gwei_amount = ('{:.0f}'.format(eth_amount*(10**18))) 

    os.environ["STARKNET_NETWORK"] = "alpha-mainnet"
    os.environ["STARKNET_WALLET"] = "starkware.starknet.wallets.open_zeppelin.OpenZeppelinAccount"

    # команда ниже разрешает использование эфира 0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7
    # контракту 0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023 -- это JediSwap
    # команда тратит газ   
    
    address_book = dict()
    address_book["ETH"] = '0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7'
    
    address_book["USDT"] = '0x068f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8'
    address_book["USDC"] = '0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8'
    address_book["DAI"] = '0x00da114221cb83fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3'
    address_book["WBTC"] = '0x03fe2b97c1fd336e750087d68b9b867997fd64a2661ff3ca5a7c771641e8e7ac'
    
    address_from = address_book[token_from]
    address_to = address_book[token_to]
    command_approve = f'starknet invoke --address {address_from} --function approve --abi approve.json --account {wallet}  --inputs 0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023 {gwei_amount} 0' 

    p = subprocess.Popen(command_approve, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for i in p.stdout.readlines():
        print(i)

    
    get_out_amount = f'starknet call --address 0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023 --function get_amounts_out --abi jediswap.json --inputs {gwei_amount} 0 2 {address_from} {address_to}'
    time.sleep(60*10)
    
    # Тут сервера ложатся неприлично часто, поэтому надо проверять, что колл прошел
    
    answer = b'trying'
    while answer == b'trying':
        p = subprocess.Popen(get_out_amount, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        answer = p.stdout.readlines()[0].split()
        print(answer)
        answer = answer[3]
        time.sleep(1)
        print('we here')
    
    out_amount = int(int(answer) * 0.98) # Допустимое проскальзывание 2%
    
    end_time = int(time.time()) + 60*60
    
    # теперь непосредственно свапаем разрешенное количество эфира 0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7
    # на USDT 0x68f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8 
    # команда тратит газ
    
    jediswap_command = f"starknet invoke --address 0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023 --account {wallet}  --function swap_exact_tokens_for_tokens --abi jediswap.json --inputs {gwei_amount} 0 {out_amount} 0 2 {address_from} {address_to} {my_address} {end_time}" 
    
    
    p = subprocess.Popen(jediswap_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for i in p.stdout.readlines():
        print(i)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Choose address and amount')
    parser.add_argument('eth_amount', type=float, help='Choose amount of ETH to swap in USDT')
    parser.add_argument('my_address', type=str, help='Choose address')
    parser.add_argument('token_from', type=str, help='Choose token')
    parser.add_argument('token_to', type=str, help='Choose token')
    
    args = parser.parse_args()
    if 'ETH' in [args.token_from, args.token_to]:
        jediswap(args.eth_amount, args.my_address, args.token_from, args.token_to)
    else:
        print('one of the token must be an ETH')