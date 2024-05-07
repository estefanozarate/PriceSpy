import re
import time 
import random
import requests
import vonage
import threading 
from bs4 import BeautifulSoup
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



title  = """

 _______            __                       ______                      
/       \          /  |                     /      \                     
$$$$$$$  | ______  $$/   _______   ______  /$$$$$$  |  ______   __    __ 
$$ |__$$ |/      \ /  | /       | /      \ $$ \__$$/  /      \ /  |  /  |
$$    $$//$$$$$$  |$$ |/$$$$$$$/ /$$$$$$  |$$      \ /$$$$$$  |$$ |  $$ |
$$$$$$$/ $$ |  $$/ $$ |$$ |      $$    $$ | $$$$$$  |$$ |  $$ |$$ |  $$ |
$$ |     $$ |      $$ |$$ \_____ $$$$$$$$/ /  \__$$ |$$ |__$$ |$$ \__$$ |
$$ |     $$ |      $$ |$$       |$$       |$$    $$/ $$    $$/ $$    $$ |
$$/      $$/       $$/  $$$$$$$/  $$$$$$$/  $$$$$$/  $$$$$$$/   $$$$$$$ |
                                                     $$ |      /  \__$$ |
                                                     $$ |      $$    $$/ 
                                                     $$/        $$$$$$/ 

By Estefano M. Zarate
Github @estefanozarate

"""    

dicc_symbols = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "binance coin": "BNB",
    "solana": "SOL",
    "cardano": "ADA",
    "ripple": "XRP",
    "dogecoin": "DOGE",
    "polkadot": "DOT",
    "shiba inu": "SHIB",
    "litecoin": "LTC",
    "chainlink": "LINK",
    "matic network": "MATIC",
    "stellar": "XLM",
    "ethereum classic": "ETC",
    "vechain": "VET",
    "bitcoin cash": "BCH",
    "eos": "EOS",
    "theta network": "THETA",
    "filecoin": "FIL",
    "tron": "TRX",
    "tezos": "XTZ",
    "aave": "AAVE",
    "maker": "MKR",
    "cosmos": "ATOM",
    "crypto.com coin": "CRO",
    "compound": "COMP",
    "terra": "LUNA",
    "avalanche": "AVAX",
    "pancakeswap": "CAKE",
    "ftx token": "FTT",
    "huobi token": "HT",
    "sushi": "SUSHI",
    "compound": "COMP",
    "uniswap": "UNI",
    "the graph": "GRT",
    "dash": "DASH",
    "bitcoin sv": "BSV",
    "iota": "MIOTA",
    "monero": "XMR",
    "algorand": "ALGO",
    "zilliqa": "ZIL",
    "matic network": "MATIC",
    "elrond": "EGLD",
    "quant": "QNT",
    "ravencoin": "RVN",
    "yearn.finance": "YFI",
    "decred": "DCR"
}

def check_coin_exists(url_website ,cryptoname) -> bool:
    print(f"[+] asking: {url_website+cryptoname}")
    if requests.get( url_website + cryptoname).status_code == 200:
        return True
    return False


def get_price_max_min(crypto, url) -> list:
    code_crypto = ""
    current_price_crypto = get_price_one_time(url=url, crypto=crypto)
    try:
        code_crypto = dicc_symbols[crypto] 
    except:
        pass
    while True:
        time.sleep(0.2)
        print("comparando el precio minimo...")
        try:
            min_price = float(input(f"Set min price [{crypto}] {code_crypto}: "))
            max_price = float(input(f"Set max price [{crypto}] {code_crypto}: "))
            break
        except:
            print("wrong values, try again!")
            pass
    if ( min_price < current_price_crypto ) and (current_price_crypto <  max_price):
            _time_ = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print("valores ingresados correctamente!")
            time.sleep(0.2)
            print(f"SHOWING ALL THE DATA ABOUT [{crypto.upper()}]")
            print(f"  CRYPTO NAME: {crypto.upper()} ")
            time.sleep(1)
            if code_crypto:
                print(f"  SIMBOL IF EXIST: [{code_crypto}]")
                time.sleep(1)
            else:
                time.sleep(1)
            print(f"  CURRENT PRICE: USD${current_price_crypto}") 
            time.sleep(0.7)
            print(f"  TIME NOW:{_time_}")
            time.sleep(1.5)
            print(f"  Data extracted from {url} at {_time_}")
            list_return = [str(min_price), str(max_price), True]
            return list_return
    
    elif  min_price > current_price_crypto:
            time.sleep(0.2)
            print(f"the price if already below {min_price}")
            time.sleep(0.3)
            print("try again")
            get_price_max_min(crypto=crypto, url=url)
    elif current_price_crypto > max_price:
            time.sleep(0.2)
            print(f"the price if already over {max_price}")
            time.sleep(0.3)
            print("try again")
            get_price_max_min(crypto=crypto, url=url)


def ask_coins(url) -> dict:
    crypto_file  = open("crypto_file.txt", "w")
    number_of_coins = ""
    contador = 0
    crypto_dic = dict()
    while True:
        try:
            number_of_coins = int(input("how many coins do you want to track?: "))
            break
        except Exception as E:
            print("[!] wrong value")
            pass
    while contador < number_of_coins:
        cryptoname = str(input(f"[{contador+1}] crypto: ").strip())
        crypto_exist_boolean = check_coin_exists(url, cryptoname=cryptoname)
        if crypto_exist_boolean and (len(crypto_dic) == 0 or not cryptoname in crypto_dic.values()):
            time.sleep(2)
            print("all good!")
            print("getting min, max price...")
            lst_min_max_bool = get_price_max_min(crypto=cryptoname,url="https://coinmarketcap.com/currencies/")
            str_to_file = f"#{contador+1},{cryptoname},{lst_min_max_bool[0]},{lst_min_max_bool[1]}\n"
            crypto_file.write(str_to_file)
            crypto_dic[contador+1] = cryptoname
            contador = contador + 1
            print(f"{cryptoname} has been stored on file!")
        elif crypto_exist_boolean and (cryptoname in crypto_dic.values()):    
            print("crypto already stored!")
            pass
        else:
            print("crypto does not exist!")
            pass

    time.sleep(1)
    print(f"all the cryptos stored: {crypto_dic}")



def get_price_one_time(url ,crypto):
    response_price_one_time = requests.get(url + crypto)
    soup = BeautifulSoup(response_price_one_time.content, "html.parser")
    target_span = soup.find("span",class_="sc-f70bb44c-0 jxpCgO base-text")
    try:
        if target_span:
            target_str = target_span.text
            target_str = str(target_str)
            target_str = target_str.replace("$", "")
            target_str = target_str.replace(",", "")
            return float(target_str)            
    except:
        return target_span
    

def get_price_real_time():
    while True:
        response = requests.get("https://www.coingecko.com/en/coins/bitcoin")
        soup = BeautifulSoup(response.content, "html.parser")
        target_span = soup.find('span', {'data-converter-target': 'price', 'data-coin-id': '1'})
        time_current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print("PRICE [BTC]:",target_span.text, "TIME [NOW]:",time_current)
        time.sleep(0.1)


def show_price_all_your_coins(url,):

    list_cryptos = list()
    with open("crypto_file.txt", "r") as f:
        for l in f:
            index, crypto =  l.split(":")
            list_cryptos.append(crypto.replace("\n", "").strip())

    for crypto in list_cryptos:
        time.sleep(0.2)
        if "coingecko" in url:
            response = requests.get(f"https://www.coingecko.com/en/coins/{crypto}")
            soup = BeautifulSoup(response.content, "html.parser")
            target_span = soup.find('span', {'data-converter-target': 'price'})
            k = crypto.replace("\n", "").strip()
            print(f"CRYPTO: {crypto.upper()} SYMBOL: {dicc_symbols[k]} PRICE: {target_span.text} TIME: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}")
        elif "coinmarketcap" in url:
            url = f"https://coinmarketcap.com/currencies/{crypto}/"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            price = soup.find("span", class_="sc-f70bb44c-0 jxpCgO base-text")
            k = crypto.replace("\n", "").strip()
            
            print(f"CRYPTO: {crypto.upper()} SYMBOL: {dicc_symbols[k]} PRICE: {price.text} TIME: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}")


def send_SMS_vonage(data_info_sms):
    try:
        crypto_name, below_value, over_value, current_price, time_now = data_info_sms

        client = vonage.Client(key="", secret="") #key and secret from vonage API 
        sms = vonage.Sms(client)

        if over_value == 0:
            message = f"""
[ALERT] The price of {crypto_name} has fallen below: US${below_value}
Current price: US${current_price}
Time of the fall: {time_now}\n\n\n\n
Sent by: PriceSpy Inc.
"""
        else:
            message = f"""
[ALERT] The price of {crypto_name} has risen above: US${over_value}
Current price: US${current_price}
Time of the rise: {time_now}\n\n\n\n
Sent by: PriceSpy Inc.
"""

        response = sms.send_message({
            "from": "Vonage APIs",
            "to": "", #phone number
            "text": message
        })

        return response["messages"][0]["status"] == "0"
    except Exception as e:
        return False



def get_price_all_coins_stored_file(url="https://coinmarketcap.com/currencies/") -> None:
    text_to_send = ["", 0, 0, 0.0, ""]
    crypto_dict =  dict()
    with open("crypto_file.txt", "r") as file_crypto:

        for crypto_min_max in file_crypto:
            list_temp = list()
            crypto_j = crypto_min_max.split(",")
            list_temp.append(float(crypto_j[2]))
            list_temp.append(float(crypto_j[3].replace("\n", "")))
            crypto_dict[str(crypto_j[1]).strip()] = list_temp

    time.sleep(1)
    for crypto, value in crypto_dict.items():
        print(f"Get Value Of {crypto.upper()}")
        time.sleep(0.5)
        print(f"MIN_PRICE: {value[0]} MAX_PRICE: {value[1]}")
        current_price_crypto = get_price_one_time(url=url, crypto=crypto)
        time.sleep(1.1)
        print(f"CURRENT PRICE: US$ {current_price_crypto}")
        if float(value[0]) > current_price_crypto:
            print(f"The current price is below US$ {value[0]}")
            time_now_below = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            text_to_send = [crypto, value[0], 0, current_price_crypto, time_now_below]

            if send_SMS_vonage(text_to_send):
                time.sleep(1.2)
                print("Message sent successfully.")
            else:
                time.sleep(1.2)
                print("Message failed ")

        elif float(value[1]) < current_price_crypto:
            print(f"The current price is over $US {value[1]}")
            time_now_over = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) )
            text_to_send = [crypto, 0, value[1] , current_price_crypto, time_now_over]
            valor_SMS = send_SMS_vonage(text_to_send)
            if valor_SMS:
                time.sleep(1.2)
                print("Message sent successfully.")
            else:
                time.sleep(1.2)
                print("Message failed ")
        else: 
            pass


def main():  
    coingecko_url = "https://www.coingecko.com/en/coins/"
    coinmarketcap_url = "https://coinmarketcap.com/currencies/"
    opt = 0
    pattern_source_coingecko = r"1+"
    pattern_source_coinmarketcap =  r"2+"
    time.sleep(1)
    print("Welcome to PriceSpy! Here, you can track the price of as many cryptocurrencies as you want!")
    print("Select the source of the information!")  
    time.sleep(0.5)
    print(colored("[Option #1]: https://www.coingecko.com/", "green"))
    time.sleep(0.5)
    print(colored("[Option #2]: https://coinmarketcap.com/", "green"))
    time.sleep(0.5)
    source_opt = str(input("Your Option: "))

    if re.match(pattern_source_coingecko, source_opt):
        print("El usuario eligio coingecko!")
        ask_coins(coingecko_url)
        opt = 1
    elif re.match(pattern_source_coinmarketcap, source_opt):
        print("El usuario eligió coinmarketcap!")
        ask_coins(coinmarketcap_url)
        opt = 2
    else:
        print("fucking moron!")

    time.sleep(0.5)
    print("getting all the prices!")
    time.sleep(1)
    print("")
    while True:
        print("function get_price_all_crypto() has been executed...")
        time.sleep(0.8)
        get_price_all_coins_stored_file()
        print("code is waiting 3min and then we will scan all the prices again...")
        time.sleep(1.5)
        print("If the price of cryptocurrencies rises above or falls below a certain value, we will send you a message...")
        time.sleep(180)
"""
    if opt == 1:
        print("connecting -> coingecko.com")
        show_price_all_your_coins(coingecko_url)
    else:
        print("connecting -> coinmarketcap.com")
        show_price_all_your_coins(coinmarketcap_url)
"""

if __name__ == "__main__":
    print(colored(title, "blue"))
    crypto = "BTC"
    url = f"https://www.binance.com/es-MX/trade/BTC_USDT?_from=markets&type=spot"
    coingecko_url = "https://www.coingecko.com/en/coins/"
    coinmarketcap_url = "https://coinmarketcap.com/currencies/"
    main()
