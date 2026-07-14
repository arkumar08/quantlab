import yfinance as yf
import yaml
import logging
import sys

from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),    #print to terminal
        logging.FileHandler("quantlab.log", mode="a")       #save in file quantlab.log 
    ]
)

def load_config(filepath = "base.yaml"):
    with open(filepath, "r") as file:
        return yaml.load(file, Loader=yaml.SafeLoader)


def download_market_data(ticker, start, end):
    logging.info("Downloading market data from Yfinance")

    data = yf.download(f"{ticker}", start=f"{start}", end=f"{end}")
    
    if data.empty:
        logging.warning("Yfinance returned an empty dataset!")
        raise ValueError(f"Data for ticker: {ticker} is empty.")
        
    else:
        logging.info("Successfully retrieved ticker data.")
        return(data)
        

def save_market_data(df, output_path):
    logging.info("Saving ticker symbol data")
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    if not df.empty:
        df.to_csv(output_path)
        logging.info(f"Data successfully saved to {output_path}")
    else:
        logging.info(f"Data is empty, nothing saved to {output_path}")



def main():
    config = load_config("configs/base.yaml")
    ticker = config["data"]["ticker"]
    start_date = config["data"]["start_date"]
    end_date = config["data"]["end_date"]
    output_path = config["data"]["output_path"]

    try:
        ticker_data = download_market_data(ticker, start_date, end_date)
    except ValueError:
        logging.error("Critical Error: No data downloaded. Cannot proceed.")
        sys.exit(1)

    try:
        save_market_data(ticker_data, output_path)
    except Exception as e:
        logging.error(f"An unexpected error has occured: {e}")
        sys.exit(1)

    row_count = len(ticker_data)
    data_start_date = ticker_data.index.min().strftime("%Y-%m-%d")
    data_end_date = ticker_data.index.max().strftime("%Y-%m-%d")
    logging.info("Process complete.")
    logging.info(f"Ticker info\n Symbol = {ticker}\n Row count: {row_count} \n Start date: {data_start_date}\n End date: {data_end_date}")



if __name__ == "__main__": 
    main()
