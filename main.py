import pygame
import asyncio # ★追加：非同期処理のためのライブラリ
import os #ブラウザに反映するためのおまじない？
import game
import title
import gameover

# Web環境でファイルを認識させるためのヒント
if not os.path.exists("assets"):
    print("Warning: assets folder not found!")

# スコアを一時的に保存しておく変数を作る
last_score = 0

async def main(): # async→Webブラウザ対応コード
    pygame.init()
    # タイトルバーの設定
    pygame.display.set_caption("My HUNTER Game")
    # 画面サイズの作成
    screen = pygame.display.set_mode((800, 600))

    state = "TITLE"

    # stateが "QUIT" になるまでループ
    while state != "QUIT":
        if state == "TITLE":
            # title.py の関数を呼び出す
            state = await title.show_title(screen)
        elif state == "PLAY":
            # game.py の関数を呼び出す ここで「文字」と「スコア」の2つを受け取る
            state, last_score = await game.play_game(screen)
        elif state == "GAMEOVER":
            # ゲームオーバー画面を呼ぶときに、スコアを渡す
            state = await gameover.show_gameover(screen, last_score)

        # ★超重要：ブラウザがフリーズしないように1回休ませる
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main()) #このコードもブラウザ用に。
