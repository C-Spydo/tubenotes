import requests
from bs4 import BeautifulSoup
import json
import datetime
import time
import os

# %%
# Set headers to mimic a browser visit
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Define URLs for stock data sources
URLS = {
    "yahoo_finance": "https://finance.yahoo.com/quote/{stock_symbol}/news?p={stock_symbol}",
    "market_watch": "https://www.marketwatch.com/investing/stock/{stock_symbol}",
    "cnbc_trader_talk": "https://www.cnbc.com/trader-talk/",
    "yahoo_topic": "https://finance.yahoo.com/topic/stock-market-news/"
}


# %%
# Function to fetch stock news from Yahoo Finance
def fetch_stock_news(stock_symbol):
    news_url = URLS['yahoo_finance'].format(stock_symbol=stock_symbol)
    response = requests.get(news_url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Failed to fetch news for {stock_symbol}. Status Code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('h3')

    news_list = []
    for headline in headlines[:10]:  # Limit to top 10 articles
        news_title = headline.get_text(strip=True)
        link = headline.find('a')['href'] if headline.find('a') else None
        full_link = f"https://finance.yahoo.com{link}" if link and link.startswith('/') else link

        if full_link:
            news_content = fetch_news_content(full_link)
            news_list.append({
                # "title": news_title,
                # "link": full_link,
                "content": news_content
            })

    return news_list


def fetch_news_content(article_url):
    """ Fetches and extracts main content from a news article """
    if not article_url:
        return "No article link provided."

    response = requests.get(article_url, headers=HEADERS)
    if response.status_code != 200:
        return "Failed to fetch article content."

    soup = BeautifulSoup(response.text, 'html.parser')

    # Yahoo Finance article text is usually inside <p> tags
    paragraphs = soup.find_all('p')
    content = "\n".join(p.get_text(strip=True) for p in paragraphs)

    return content if content else "No content extracted."


# %%
# Function to fetch stock prices
def fetch_stock_price(stock_symbol):
    price_url = f"https://finance.yahoo.com/quote/{stock_symbol}?p={stock_symbol}"
    response = requests.get(price_url, headers=HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        price_tag = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})

        if price_tag:
            return price_tag.get_text(strip=True)
        else:
            print(f"Price element not found for {stock_symbol}.")
            return None
    else:
        print(f"Failed to fetch price for {stock_symbol}. Status Code: {response.status_code}")
        return None


# %%
# Function to save data to JSON file
def save_data(data, filename="stock_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")


# %%
# Function to load existing data if it's not older than 6 hours
def load_data_if_valid(filename="stock_data.json"):
    if os.path.exists(filename):
        file_time = os.path.getmtime(filename)
        current_time = time.time()
        if (current_time - file_time) < 6 * 3600:  # Check if the file is less than 6 hours old
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
    return None


# %%
# Main function to scrape stock data
def scrape_stocks(stock_symbols):
    # Check if existing data is valid
    existing_data = load_data_if_valid()
    if existing_data:
        print("Using cached data.")
        return existing_data

    stock_data = {}
    for symbol in stock_symbols:
        print(f"Fetching data for {symbol}...")
        news = fetch_stock_news(symbol)
        price = fetch_stock_price(symbol)

        stock_data[symbol] = {
            "news": news,
            "price": price,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    save_data(stock_data)
    return stock_data