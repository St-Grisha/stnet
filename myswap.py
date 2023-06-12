import os
import time
import subprocess
import argparse
from web3 import Web3


def myswap(eth_amount, wallet='__default__'):
    contract_address = '0x010884171baf1914edc28d7afb619b40a4051cfae78a094a55d230f19e944a28'

    gwei_amount = ('{:.0f}'.format(eth_amount*(10**18))) 

    os.environ["STARKNET_NETWORK"] = "alpha-mainnet"
    os.environ["STARKNET_WALLET"] = "starkware.starknet.wallets.open_zeppelin.OpenZeppelinAccount"

    # команда ниже разрешает использование эфира 0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7
    # контракту 0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023 -- это JediSwap
    # команда тратит газ   
    
    address_book = dict()
    address_book["ETH"] = '0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7'
    address_book["USDT"] = '0x068f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8'
    
    address_from = address_book["ETH"]
    address_to = address_book["USDT"]
    command_approve = f'starknet invoke --address {address_from} --function approve --abi approve.json --account {wallet} --inputs {contract_address} {gwei_amount} 0 ' 


    p = subprocess.Popen(command_approve, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for i in p.stdout.readlines():
        print(i)

    
    get_out_amount = f'starknet call --address {contract_address} --function get_pool --abi myswap.json --inputs 4'
    time.sleep(60*3)
    
    # Тут сервера ложатся неприлично часто, поэтому надо проверять, что колл прошел
    eth_count = 'while'
    while eth_count == 'while':
        p = subprocess.Popen(get_out_amount, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        answer = p.stdout.readlines()

        answet_list =  str(answer[0]).split()
        eth_count = answet_list[2]
        usdt_count = answet_list[5]

    w3 = Web3()
    eth_int_count = int(w3.to_hex(hexstr=str(eth_count)), 16)
    min_out = int(int(usdt_count)/eth_int_count * int(gwei_amount) * 0.97) # Допустимое проскальзывание 3%
    
    # теперь непосредственно свапаем разрешенное количество эфира 0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7
    # на USDT 0x68f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8 
    # команда тратит газ
    
    myswap_command = f"starknet invoke --address {contract_address} --function swap --abi myswap.json --account {wallet} --inputs 4 {address_from} {gwei_amount} 0 {min_out} 0" 
    
    
    p = subprocess.Popen(myswap_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for i in p.stdout.readlines():
        print(i)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Choose address and amount')
    parser.add_argument('eth_amount', type=float, help='Choose amount of ETH to swap in USDT')
    args = parser.parse_args()
    myswap(args.eth_amount)
