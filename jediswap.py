import os
import time
import subprocess
import argparse


def main(eth_amount, my_address):
    contract_address = '0x05900cfa2b50d53b097cb305d54e249e31f24f881885aae5639b0cd6af4ed298'
#     my_address = '0x054e3682d5227b7f0c72cfcba78c77e133909180faba7f2deb581547ab2eca76'

#     eth_amount = 0.001
    gwei_amount = ('{:.0f}'.format(eth_amount*10**18)) 

    os.environ["STARKNET_NETWORK"] = "alpha-mainnet"
    os.environ["STARKNET_WALLET"] = "starkware.starknet.wallets.open_zeppelin.OpenZeppelinAccount"

    # команда ниже разрешает использование эфира 0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7
    # контракту 0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023 -- это JediSwap
    # команда тратит газ     
    command_approve = f'starknet invoke --address 0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7 --function approve --abi approve.json --inputs 0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023 {gwei_amount} 0' 


    p = subprocess.Popen(command_approve, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for i in p.stdout.readlines():
        print(i)

    
    get_out_amount = f'starknet call --address 0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023 --function get_amounts_out --abi jediswap.json --inputs {gwei_amount} 0 2 0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7 0x68f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8'
    
    answer = b'trying'
    while answer == b'trying':
        p = subprocess.Popen(get_out_amount, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        answer = p.stdout.readlines()[0].split()
        print(answer)
        answer = answer[3]
        time.sleep(1)
        print('we here')
    # if answer != b'trying':
    
    out_amount = int(answer)
    
    
    time.sleep(60*10)
    
    end_time = int(time.time()) + 60*60
    
    # теперь непосредственно свапаем разрешенное количество эфира 0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7
    # на USDT 0x68f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8 
    # команда тратит газ
    jediswap_command = f"starknet invoke --address 0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023 --function swap_exact_tokens_for_tokens --abi jediswap.json --inputs {gwei_amount} 0 {out_amount} 0 2 0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7 0x68f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8 {my_address} {end_time}" 
    
    p = subprocess.Popen(jediswap_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for i in p.stdout.readlines():
        print(i)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Choose address and amount')
    parser.add_argument('eth_amount', type=float, help='Choose amount of ETH to swap in USDT')
    parser.add_argument('my_address', type=float, help='Choose address')
    
    main(parser.eth_amount, parser.my_address)