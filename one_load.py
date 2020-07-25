# パッケージのインポート
from game import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
from pathlib import Path
from threading import Thread
import tkinter as tk

# パラメータの準備
G_MASU_NUM = 64 # マス数
G_ROW_COL_NUM = 8 # 行列数

# ベストプレイヤーのモデルの読み込み
model = load_model('./model/best.h5')

# ゲーム状態の生成
state = State()

print(state.pieces)
print(state.enemy_pieces)
print(state.depth)
