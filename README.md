# stnet

Для начала 
```
pip install -r requirements.txt
```

## Layerswap
Мы будем использовать переменные среды для хранения персональных данных. Скрипт layerswap.py требует наличия двух переменных в окружении: binance apikey, binance secretkey.
Чтобы их установить, на маке нужно перед запуском скрипта в командной строке написать: 
```export apikey=xxx```
```export secretkey=xxx```

Для данного ключа API должно быть разрешение на вывод средств с белых IP-адресов, куда необходимо записать IP машины, на которой будет запускаться скрипт. 

После этого запустить команду
``` 
layerswap.py ETH_AMOUNT STARKNET_ADDRESS 
```
Пример:
``` 
layerswap.py 0.05 0x020f2547adbda790ec290a7366446f98e200def6245b9a02cfab88061e608cc2  
```

Дальше ждем 20-40 минут для начисления средств. Если необходимо получить ссылку на транзакцию для отслеживания ее выполенния, необходимо в конце еще дописать True:
``` 
layerswap.py 0.05 0x020f2547adbda790ec290a7366446f98e200def6245b9a02cfab88061e608cc2 True
```

## Jediswap
Приготовьтесь настраивать среду долго и мучительно. Для начала установите python3.9 и Rust в своем окружении. 
https://www.python.org/downloads/release/python-390/
https://www.rust-lang.org/tools/install

Далее установим каиро. Для Ubuntu или Mac:
```
sudo apt install -y libgmp3-dev
pip install ecdsa fastecdsa sympy
pip install cairo-lang
starknet --version
```
Последняя команда должна вывести версию starknet 0.11.0.2 !

Далее необходимо создать образ кошелька, к которому вы будете подключаться с помощью Starknet CLI. Для этого создаем в корне папку .starknet_accounts, помещаем туда файл starknet_open_zeppelin_accounts.json:
```
mkdir .starknet_accounts
cd .starknet_accounts
touch starknet_open_zeppelin_accounts.json
nano starknet_open_zeppelin_accounts.json 
```
В открывшемся окне вставляем:
```
{"alpha-mainnet":
   {"__default__":{"address":"YOUR_ACCOUNT_ADDRESS",
                   "private_key":"YOUR_ACCOUNT_PRIVATE_KEY"}
   }
}
```
И помещаем это в энвы среды: ```export STARKNET_WALLET=starkware.starknet.wallets.open_zeppelin.OpenZeppelinAccount```

Теперь можно запускать скрипт. Он принимает на вход только адрес кошелька и количество эфиров для свапа в USDT:
```
python jediswap.py 0.001 0x020f2547adbda790ec290a7366446f98e200def6245b9a02cfab88061e608cc2
```

