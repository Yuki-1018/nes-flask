from flask import Flask, Response
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    # スクレイピングするURL
    url = 'https://www.jorudan.co.jp/unk/'
    
    # HTTP GETリクエストを送信
    response = requests.get(url)
    
    # レスポンスのステータスコードを確認
    if response.status_code != 200:
        return Response("<p>Failed to retrieve the webpage</p>", status=500, mimetype='text/html')
    
    # エンコーディングをUTF-8に設定
    response.encoding = 'utf-8'
    
    # BeautifulSoupを使ってHTMLを解析
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # class属性が"unktable"の<table>タグを検索
    table = soup.find('table', class_='unktable')
    
    if table is None:
        return Response("<p>No table found with class 'unktable'</p>", status=404, mimetype='text/html')
    
    # テーブルのデータをパース
    data = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 3:
            row_data = {
                "date": cols[0].get_text(strip=True),
                "line": cols[1].get_text(strip=True),
                "info": cols[2].get_text(strip=True)
            }
            data.append(row_data)
    
    # HTMLの表を作成
    html_table = '<table border="1"><tr><th>Date</th><th>Line</th><th>Info</th></tr>'
    for row in data:
        html_table += f'<tr><td>{row["date"]}</td><td>{row["line"]}</td><td>{row["info"]}</td></tr>'
    html_table += '</table>'
    
    # HTMLをレスポンスとして返す
    return Response(html_table, mimetype='text/html')

if __name__ == '__main__':
    app.run(debug=True)
