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

Теперь можно запускать скрипт. Он принимает на вход адрес кошелька, количество токенов, токен для свапа и токен для получения:
```
python jediswap.py 0.001 0x020f2547adbda790ec290a7366446f98e200def6245b9a02cfab88061e608cc2 ETH USDT
```

## Myswap

Нужно сделать все то же, что для Jediswap.
Потом есть скрипт, который свапает с ETH на USDT. Пока есть только одна пара, надо лишь написать объем:
```
python myswap.py 0.001
```

## Мульты

Делаем все по инструкции выше. Добавляем в файл starknet_open_zeppelin_accounts.json данные всех своих мультов.

```
{"alpha-mainnet":
   {"__default__":{"address":"YOUR_ACCOUNT_ADDRESS",
                   "private_key":"YOUR_ACCOUNT_PRIVATE_KEY"},
   "account_name_2":{"address":"YOUR_ACCOUNT_ADDRESS_2",
                   "private_key":"YOUR_ACCOUNT_PRIVATE_KEY_2"},
   "account_name_3":{"address":"YOUR_ACCOUNT_ADDRESS_3",
                   "private_key":"YOUR_ACCOUNT_PRIVATE_KEY_3"},
   ...
   }
}
```
Далее нужно раскидать по всем кошелькам средства, используя Binance. Для этого нужно создать файл wallets.py со следующим содержанием (название кошелька и его адрес):

```
wallets = {"account_name_2":"YOUR_ACCOUNT_ADDRESS_2",
"account_name_3":"YOUR_ACCOUNT_ADDRESS_3"} 
```

После чего запустить  
```
python mult.py --deposit True --eth_amount_to_deposit 0.1 
```

Скрипт раскидает примерно одинаковые рандомные суммы (+- 5%) на каждый кошелек с максимальным ограничением 0.1 ETH (внимание: сумма всех выводов не превысит 0.1 ETH). То есть если 5 кошельков и 0.1 ETH, то на каждом окажется примерно 0.02. 

Если аккаунты еще не задеплоены, то нужно руками прокликать deploy account в расширении. Хз, как сделать нормально.

Дальше для массового свапа ETH на околорандомные суммы нужно запустить:

```
python mult.py --swap True --eth_amount_to_swap 0.01 
```

Этот скрипт на каждом кошельке проведет одну транзакцию обмена ETH на один из стейблов или обернутый биткоин. Рандомно выберет делать это на myswap или на jediswap. GL HF