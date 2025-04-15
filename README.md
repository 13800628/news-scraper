# Yahooニュース自動スクレイパー

このプロジェクトは Yahoo! ニュースから記事を自動で取得し、CSV形式で保存する Python スクリプトです。cron によって毎朝7時に自動実行され、最新のニュースデータを収集できます。

---

## 機能（Features）

- Yahoo! ニュース記事の自動スクレイピング
- 毎日7:00AMに自動実行（cron 使用）
- 取得したニュースはCSVファイルに保存
- 他ニュースサイト向けにも簡単に拡張可能

---

## 技術スタック（Tech Stack）

- Python 3.x
- BeautifulSoup（Webスクレイピング）
- pandas（CSV処理）
- requests（HTTP通信）
- cron（スケジューリング）

---

## 使い方（Installation）

1. このリポジトリをクローン：
   ```bash
   git clone https://github.com/yourusername/news-scraper.git
