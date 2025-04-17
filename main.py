import requests
from bs4 import BeautifulSoup
import os
import logging
import sqlite3
import pandas as pd

# ログ設定
logging.basicConfig(level=logging.INFO)

# データベース作成
def create_database():
    conn = sqlite3.connect('news_scraper.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# データベースにニュースを挿入
def insert_news(title, url):
    conn = sqlite3.connect('news_scraper.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO news (title, url) VALUES (?, ?)
    ''', (title, url))

    conn.commit()
    conn.close()

# URLからHTMLコンテンツを取得
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # ステータスコードが200番台じゃない場合は例外
        return response.content
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTPリクエストエラー: {e}")
        return None

# HTMLコンテンツをパースして記事タイトルとリンクを抽出
def parse_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    news_items = []

    for item in soup.select('a[href^="https://news.yahoo.co.jp/articles/"]'):
        title = item.get_text(strip=True)
        link = item.get("href")
        if title and link:
            news_items.append({"Title": title, "Link": link})

    return news_items

# スクレイピングして記事データをCSVに保存
def save_to_csv(data, output_path="data/yahoo_news.csv"):
    if not os.path.exists("data"):
        os.makedirs("data")

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    logging.info(f"{len(data)} 件の記事を {output_path} に保存しました。")

# ニュースを取得してデータベースに保存する一連の流れ
def fetch_and_save_news(url="https://news.yahoo.co.jp/", output_path="data/yahoo_news.csv"):
    logging.info("Yahoo!ニュースの記事を取得しています...")
    
    html_content = fetch_html(url)
    if html_content is None:
        logging.error("HTMLの取得に失敗しました。")
        return
    
    news_data = parse_html(html_content)
    if news_data:
        save_to_csv(news_data, output_path)
        for news_item in news_data:
            insert_news(news_item['Title'], news_item['Link'])
    else:
        logging.warning("記事の取得に失敗しました。")

# Git操作：スクレイピング完了後に自動でコミットしてpush
def git_commit_and_push():
    os.system("cd /Users/isayamayuto/Desktop/news.scraper && git add .")
    os.system('cd /Users/isayamayuto/Desktop/news.scraper && git commit -m "Auto-update: scraped data"')
    os.system("cd /Users/isayamayuto/Desktop/news.scraper && git push origin main")

def main():
    # データベース作成
    create_database()

    # ニュースデータをスクレイピングして保存
    fetch_and_save_news()

    # Gitでのコミットとpush
    git_commit_and_push()

if __name__ == "__main__":
    main()