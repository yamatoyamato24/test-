import pygame
import asyncio
import math

async def show_title(screen):

    # --- BGMの再生 ---
    # pygame.mixer.music.load("assets/title_bgm.ogg") # ファイルを読み込む
    # pygame.mixer.music.play(-1) # ループ再生開始
    
    # 使うフォント名の設定
    font_name = None
    font_main = pygame.font.SysFont(font_name, 40)
    font_sub = pygame.font.SysFont(font_name, 25)
    
    clock = pygame.time.Clock()
    waiting = True

    while waiting:
        # 1. 点滅のための計算
        # math.sinを使って0.0〜1.0の間をなめらかに行き来させる
        alpha = (math.sin(pygame.time.get_ticks() * 0.005) + 1) / 2
        
        # 2. 画面を塗りつぶす（前のフレームの絵を消す）
        screen.fill((136, 136, 136))
        
        # 3. メインタイトルの描画（alphaが0.3より大きい時だけ表示＝点滅）
        if alpha > 0.3:
            text_main = font_main.render("スペースキーでスタート", True, (255, 255, 255))
            rect_main = text_main.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text_main, rect_main)

        # 4. サブタイトルの描画（こちらは常時表示）
        text_sub = font_sub.render("かいぶつから逃げ切れ！", True, (220, 220, 220))
        rect_sub = text_sub.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 60))
        screen.blit(text_sub, rect_sub)

        # 5. イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
            # ★追加：画面クリック（タッチ）でもスタートできるようにする
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

        # ★重要：ここを while の中に入れます
        pygame.display.flip() # 描画内容を画面に反映
        clock.tick(60)        # 1秒間に60回実行
    # これが抜けていると灰色の画面から進みません！
        await asyncio.sleep(0) 
    # pygame.mixer.music.stop() # 最後に「PLAY」を返してゲームが始まる直前に止める
    
    # whileを抜けたら「PLAY」を返す
    return "PLAY"
