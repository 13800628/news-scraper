import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import logging


# ログ設定
logging.basicConfig(level=logging.INFO)


def fetch_html(url):
    """
    URLからHTMLコンテンツを取得
    :param url: 取得するURL
    :return: HTMLコンテンツまたはNone
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # ステータスコードが200番台じゃない場合は例外
        return response.content
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTPリクエストエラー: {e}")
        return None


def parse_html(html_content):
    """
    HTMLコンテンツをパースして記事タイトルとリンクを抽出
    :param html_content: 取得したHTMLコンテンツ
    :return: 記事タイトルとリンクのリスト
    """
    soup = BeautifulSoup(html_content, "html.parser")
    news_items = []

    for item in soup.select('a[href^="https://news.yahoo.co.jp/articles/"]'):
        title = item.get_text(strip=True)
        link = item.get("href")
        if title and link:
            news_items.append({"Title": title, "Link": link})

    return news_items


def save_to_csv(data, output_path="data/yahoo_news.csv"):
    """
    取得した記事データをCSVに保存
    :param data: 保存する記事データ
    :param output_path: 出力するCSVファイルのパス
    """
    if not os.path.exists("data"):
        os.makedirs("data")

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    logging.info(f"{len(data)} 件の記事を {output_path} に保存しました。")


def fetch_and_save_news(url="https://news.yahoo.co.jp/", output_path="data/yahoo_news.csv"):
    """
    ニュースを取得してCSVに保存する一連の流れ
    :param url: 取得するURL
    :param output_path: 出力するCSVファイルのパス
    """
    logging.info("Yahoo!ニュースの記事を取得しています...")
    
    html_content = fetch_html(url)
    if html_content is None:
        logging.error("HTMLの取得に失敗しました。")
        return
    
    news_data = parse_html(html_content)
    if news_data:
        save_to_csv(news_data, output_path)
    else:
        logging.warning("記事の取得に失敗しました。")


def main():
    fetch_and_save_news()


if __name__ == "__main__":
    main()

# Git操作：スクレイピング完了後に自動でコミットしてpush
os.system("cd /Users/isayamayuto/Desktop/news.scraper && git add .")
os.system('cd /Users/isayamayuto/Desktop/news.scraper && git commit -m "Auto-update: scraped data"')
os.system("cd /Users/isayamayuto/Desktop/news.scraper && git push origin main")