import pygame
import asyncio
import ranking

async def show_gameover(screen, score):
    # スコアを登録して、最新のベスト5をもらう
    best_five = ranking.update_ranking(score)

    # フォント設定（Web環境への配慮）
    font_name = None 
    font_msg = pygame.font.SysFont(font_name, 60)
    font_score = pygame.font.SysFont(font_name, 40)
    font_back = pygame.font.SysFont(font_name, 30)
    font_rank = pygame.font.SysFont(font_name, 25)

    clock = pygame.time.Clock()
    waiting = True

    while waiting:
        # 1. 画面を塗りつぶす（ループ内で毎回描画するのがWeb版のコツ）
        screen.fill((50, 0, 0)) 

        # 2. メッセージとスコアの作成
        text_msg = font_msg.render("GAME OVER", True, (255, 0, 0))
        rect_msg = text_msg.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
        
        text_score = font_score.render(f"生き残った時間: {score}秒", True, (0, 255, 0))
        rect_score = text_score.get_rect(center=(400, 320))

        # 3. 操作説明（スマホ用に「クリック」を追加）
        text_back = font_back.render("クリック か スペースで戻る", True, (255, 255, 255))
        rect_back = text_back.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 150))

        # 4. ランキングの表示
        text_rank_title = font_rank.render("★ BEST 5 ★", True, (255, 215, 0))
        screen.blit(text_rank_title, (20, 20))
        for i, s in enumerate(best_five):
            rank_text = font_rank.render(f"{i+1}位: {s}秒", True, (255, 255, 255))
            screen.blit(rank_text, (20, 60 + i * 30))

        # 5. 描画を反映
        screen.blit(text_msg, rect_msg)
        screen.blit(text_score, rect_score)
        screen.blit(text_back, rect_back)
        
        pygame.display.flip()

        # 6. イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
            # ★追加：スマホ操作（タッチ）対応
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

        # --- Web版で必須の処理 ---
        clock.tick(60)
        await asyncio.sleep(0) # これを入れないとフリーズします！

    return "TITLE"
