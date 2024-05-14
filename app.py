from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    # スクレイピングするURL
    url = 'http://example.com'
    
    # HTTP GETリクエストを送信
    response = requests.get(url)
    
    # レスポンスのステータスコードを確認
    if response.status_code != 200:
        return jsonify({"error": "Failed to retrieve the webpage"}), 500
    
    # BeautifulSoupを使ってHTMLを解析
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # class属性が"unktable"の<table>タグを検索
    table = soup.find('table', class_='unktable')
    
    if table is None:
        return jsonify({"error": "No table found with class 'unktable'"}), 404
    
    # テーブルのデータをパース
    data = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)
    
    # JSON形式で返す
    return jsonify({"data": data})

if __name__ == '__main__':
    app.run(debug=True)
