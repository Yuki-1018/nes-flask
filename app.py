from flask import Flask, Response, jsonify
from bs4 import BeautifulSoup
import requests
import dicttoxml

app = Flask(__name__)

def fetch_and_parse_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None, f"Failed to retrieve the webpage. Status code: {response.status_code}"
    
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='unktable')
    if table is None:
        return None, "No table found with class 'unktable'"
    
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
    
    return data, None

@app.route('/scrape/json', methods=['GET'])
def scrape_json():
    url = 'https://www.jorudan.co.jp/unk/'
    data, error = fetch_and_parse_url(url)
    if error:
        return jsonify({"error": error}), 500
    
    return jsonify({"data": data})

@app.route('/scrape/xml', methods=['GET'])
def scrape_xml():
    url = 'https://www.jorudan.co.jp/unk/'
    data, error = fetch_and_parse_url(url)
    if error:
        return Response(f"<error>{error}</error>", status=500, mimetype='application/xml')
    
    xml_data = dicttoxml.dicttoxml({"rows": data}, custom_root='root', attr_type=False)
    return Response(xml_data, mimetype='application/xml')

@app.route('/scrape/html', methods=['GET'])
def scrape_html():
    url = 'https://www.jorudan.co.jp/unk/'
    data, error = fetch_and_parse_url(url)
    if error:
        return Response(f"<p>{error}</p>", status=500, mimetype='text/html')
    
    html_table = '<table border="1"><tr><th>Date</th><th>Line</th><th>Info</th></tr>'
    for row in data:
        html_table += f'<tr><td>{row["date"]}</td><td>{row["line"]}</td><td>{row["info"]}</td></tr>'
    html_table += '</table>'
    
    return Response(html_table, mimetype='text/html')

if __name__ == '__main__':
    app.run(debug=True)
