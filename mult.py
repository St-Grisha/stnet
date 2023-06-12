import argparse
import random

from wallets import wallets
from myswap import myswap
from jediswap import jediswap
from layerswap import main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Choose address and amount')
    parser.add_argument('--deposit', type=bool, default=False, required=False, help='True if deposit is needed')
    parser.add_argument('--swap', type=bool, default=False, required=False, help='True if swap is needed')
    parser.add_argument('--eth_amount_to_deposit', type=float, required=False, help='Choose amount of ETH to spend from Binance to all accounts (sum)')
    parser.add_argument('--eth_amount_to_swap', type=float, required=False, help='Choose max amount of ETH to swap')
    args = parser.parse_args()

    if args.deposit:
        amounts = []
        wallet_count = len(wallets.keys())
        default_ammount = args.eth_amount_to_deposit / wallet_count
        for i in range(wallet_count):
            if i%2==0:
                random_part = random.gauss(0, 0.05)
                amounts.append(default_ammount * (1+random_part))
            else:
                amounts.append(default_ammount * (1-random_part))
        
        if sum(amounts) > args.eth_amount_to_deposit:
            amounts[-1] = amounts[-1] - (sum(amounts) - args.eth_amount_to_deposit) * 1.1
        


        for wallet, amount in zip(wallets.values(), amounts):
            main(amount, wallet, 1, True)
    elif args.swap:
        for wallet in wallets.keys():
            amount = args.eth_amount_to_swap * 1-(abs(random.gauss(0, 0.1)))
            if random.random > 0.5:
                myswap(amount, wallet)
            else:
                jediswap(amount, wallets[wallet], 'ETH', random.choice(['USDT', 'USDC', 'DAI', 'WBTC']))
 