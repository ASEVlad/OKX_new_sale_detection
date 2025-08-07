import os
import requests
from loguru import logger
from bs4 import BeautifulSoup


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DAPP_FILE = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "dapps.txt"))


def get_current_dapps():
    try:
        # Your target URL
        okx_link = 'https://web3.okx.com/cryptopedia/event/unlocktge'

        response = requests.get(okx_link)

        # Step 2: Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        divs = soup.find_all('div', class_=lambda x: x and 'index_dapp__' in x)

        current_dapps = []
        for div in divs:
            current_dapps.append(div.text.split(' ')[0])

        return set(current_dapps)

    except Exception as e:
        logger.error(f"Error fetching dapps from website: {e}")



def save_dapps(dapps):
    with open(DAPP_FILE, 'w', encoding='utf-8') as f:
        for dapp in sorted(dapps):
            f.write(f"{dapp}\n")

def retrieve_dapps():
    if not os.path.exists(DAPP_FILE):
        return set()
    with open(DAPP_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

