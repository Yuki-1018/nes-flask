from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_rom', methods=['POST'])
def upload_rom():
    rom = request.files['rom']
    rom_data = rom.read()
    return jsonify({'rom_data': rom_data.hex()})

@app.route('/save_state', methods=['POST'])
def save_state():
    state = request.json['state']
    # ここに状態を保存するロジックを追加
    return jsonify({'status': 'success'})

@app.route('/load_state', methods=['POST'])
def load_state():
    # ここに状態をロードするロジックを追加
    state = "loaded_state_data"
    return jsonify({'state': state})

@app.route('/memory', methods=['GET', 'POST'])
def memory():
    if request.method == 'GET':
        # ここにメモリの読み取りロジックを追加
        memory = "memory_data"
        return jsonify({'memory': memory})
    elif request.method == 'POST':
        address = request.json['address']
        value = request.json['value']
        # ここにメモリの書き込みロジックを追加
        return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
