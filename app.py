import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'roms/'

# ホームページ
@app.route('/')
def index():
    return render_template('index.html')

# ROMのアップロード
@app.route('/upload_rom', methods=['POST'])
def upload_rom():
    if 'rom' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['rom']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'success': 'File uploaded successfully', 'filename': filename})

# メモリの表示と編集
@app.route('/memory', methods=['GET', 'POST'])
def memory():
    if request.method == 'GET':
        # メモリを読み取る処理
        # ここにjsnesでのメモリ読み取りコードを追加
        
        # 仮のデータを返す
        memory_data = {'0000': 'FF', '0001': '00', '0002': 'A9', '0003': '05'}
        return jsonify(memory_data)
    
    elif request.method == 'POST':
        # メモリを書き換える処理
        address = request.form['address']
        value = request.form['value']
        # ここにjsnesでのメモリ書き換えコードを追加
        
        return jsonify({'success': 'Memory updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
