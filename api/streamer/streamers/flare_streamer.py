import os
import time

import pandas as pd
from streamer.utils.flare import get_latest_price

PRICE_FILE = 'flare_prices.feather'
REFRESH_RATE = 20  # seconds


async def block_loop():
    data_path = os.environ.get("SHARED_DATA_PATH", "./data/")
    file_path = f"{data_path}/{PRICE_FILE}"

    flare_prices = pd.read_feather(file_path) if os.path.exists(file_path) else pd.DataFrame()

    os.makedirs(data_path, exist_ok=True)

    while True:
        price = get_latest_price()
        latest_price = pd.DataFrame([price])
        flare_prices = pd.concat([flare_prices, latest_price])
        flare_prices = flare_prices.drop_duplicates()

        print("Storing", len(flare_prices), "flare_prices...")
        flare_prices.to_feather(file_path)
        print("Stored", len(flare_prices), "flare_prices.")

        time.sleep(REFRESH_RATE)

    await binance.close()
