# -*- coding: utf-8 -*-
from game import State
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib.parse import parse_qs
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model

# http://localhost:8080/
class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        print('path = {}'.format(self.path))

        # レスポンス作成
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'Hello')
        return

    def do_POST(self):
        # urlパラメータを取得
        parsed_path = urlparse(self.path)
        print('parsed: path = {}, query = {}'.format(parsed_path.path, parse_qs(parsed_path.query)))
        
        # body部を取得
        content_len  = int(self.headers.get("content-length"))
        req_body = self.rfile.read(content_len).decode("utf-8")
        req_json = json.loads(req_body)

        pieces = [int(str) for str in req_json['pieces'].split(',')]
        enemy_pieces = [int(str) for str in req_json['enemy_pieces'].split(',')]
        depth = int(req_json['depth'])

        # 状態の生成
        state = State(pieces, enemy_pieces, depth)
        # ベストプレイヤーのモデルの読み込み
        model = load_model('./model/best.h5')
        # PV MCTSで行動選択を行う関数の生成
        next_action = pv_mcts_action(model, 0.0)
        # 行動の取得
        action = next_action(state)
        # 次の状態の取得
        state = state.next(action)



        response = json.dumps({"pieces": state.pieces, "enemy_pieces": state.enemy_pieces, "depth": state.depth})

        # response = 'Hello POST Response'
        
        # リクエスト取得
        # content_len = int(self.headers.get('content-length'))
        # requestBody = json.loads(self.rfile.read(content_len).decode('utf-8'))
        # requestBody = self.rfile.read(content_len)
        
        # レスポンス作成
        self.send_response(200)
        self.send_header("Content-type", 'application/json')
        self.send_header("Content-Length", len(response))
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))
        
if __name__ == '__main__':
    
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, MyHandler)
    print('Serving HTTP on localhost port %d ...' % server_address[1])
    print('use <Ctrl-(C or break)> to stop')
    httpd.serve_forever()
    