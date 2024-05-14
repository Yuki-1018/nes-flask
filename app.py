from flask import Flask, Response
from bs4 import BeautifulSoup
import requests
import dicttoxml

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    # スクレイピングするURL
    url = 'https://www.jorudan.co.jp/unk/'
    
    # HTTP GETリクエストを送信
    response = requests.get(url)
    
    # レスポンスのステータスコードを確認
    if response.status_code != 200:
        return Response("<error>Failed to retrieve the webpage</error>", status=500, mimetype='application/xml')
    
    # エンコーディングをUTF-8に設定
    response.encoding = 'utf-8'
    
    # BeautifulSoupを使ってHTMLを解析
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # class属性が"unktable"の<table>タグを検索
    table = soup.find('table', class_='unktable')
    
    if table is None:
        return Response("<error>No table found with class 'unktable'</error>", status=404, mimetype='application/xml')
    
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
    
    # データをXML形式に変換
    xml_data = dicttoxml.dicttoxml({"rows": data}, custom_root='root', attr_type=False)
    
    # XMLをレスポンスとして返す
    return Response(xml_data, mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug=True)
