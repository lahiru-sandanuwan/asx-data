import os

import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_ticker_details(ticker):
    # Create a URL for the request based on the ticker symbol
    url = f"https://asx.api.markitdigital.com/asx-research/1.0/companies/{ticker}/getTradingDaysInLast20Days"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return 0, 0

    data = response.json()
    try:
        # Calculate the number of trading days based on the current and listed dates
        days = data["data"]["currentDate"] - data["data"]["dateListed"] + 1
        xid = data["data"]["xid"]
    except KeyError:
        print(f"Error: {data}")
        days = 0
        xid = 0

    return days, xid


def get_historical_data(ticker, token):
    # Ensure data folder exists
    data_folder = 'data'
    os.makedirs(data_folder, exist_ok=True)

    csv_file = os.path.join(data_folder, f"{ticker}.csv")
    # Check if the data file already exists to avoid re-fetching
    if os.path.exists(csv_file):
        print(f"{csv_file} already exists. Skipping data retrieval.")
        return

    days, xid = get_ticker_details(ticker)

    # Skip data retrieval if there are no trading days
    if days == 0:
        print(f"No trading days found for {ticker}. Skipping data retrieval.")
        return

    # Set up parameters and the URL for the historical data request
    url = f"https://api.markitondemand.com/apiman-gateway/MOD/chartworks-data/1.0/chartapi/series?access_token={token}"
    data = {
        "days": days,
        "dataNormalized": False,
        "dataPeriod": "Day",
        "dataInterval": 1,
        "realtime": False,
        "yFormat": "0.###",
        "timeServiceFormat": "JSON",
        "returnDateType": "ISO8601",
        "elements": [
            {"Type": "price", "Symbol": xid, "OverlayIndicators": [], "Params": {}},
            {"Type": "volume", "Symbol": xid, "OverlayIndicators": [], "Params": {}}
        ]
    }
    response = requests.post(url, json=data)
    data = response.json()

    # Filter the data to include only necessary details
    filtered_data = {
        "dates": data["Dates"],
        "open": data["Elements"][0]["ComponentSeries"][0]["Values"],
        "high": data["Elements"][0]["ComponentSeries"][1]["Values"],
        "low": data["Elements"][0]["ComponentSeries"][2]["Values"],
        "close": data["Elements"][0]["ComponentSeries"][3]["Values"],
        "volume": data["Elements"][1]["ComponentSeries"][0]["Values"]
    }

    # Ensure all columns have the same length
    min_length = min(len(filtered_data[key]) for key in filtered_data)
    for key in filtered_data:
        filtered_data[key] = filtered_data[key][:min_length]

    # Convert the filtered data into a DataFrame and save it to a CSV file in the 'data' folder
    df = pd.DataFrame(filtered_data)
    df.to_csv(csv_file, index=False)

    print(f"{csv_file} saved.")


# Load API token from environment variable
api_token = os.getenv('API_TOKEN')

# Load the list of tickers from a CSV file
tickers_list = pd.read_csv("tickers/tickers.csv")

# Retrieve historical data for each ticker in the list
for item in tickers_list["ticker"]:
    get_historical_data(item, api_token)
