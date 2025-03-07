import requests
from bs4 import BeautifulSoup



HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

URLS = {
    "yahoo_finance": "https://finance.yahoo.com/quote/{stock_symbol}/news?p={stock_symbol}",
    "market_watch": "https://www.marketwatch.com/investing/stock/{stock_symbol}",
    "cnbc_trader_talk": "https://www.cnbc.com/trader-talk/",
    "yahoo_topic": "https://finance.yahoo.com/topic/stock-market-news/"
}

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


