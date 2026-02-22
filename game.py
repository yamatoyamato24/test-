import pygame
from PIL import Image
import asyncio

# プレイヤーやエネミーなど「小さいキャラ」用の変換関数
def pil_to_surface(pil_image, max_size=(50, 50)):
    # 1. 縦横比を維持したまま、指定したサイズ内に収める
    pil_image.thumbnail(max_size, Image.Resampling.LANCZOS)
    if pil_image.mode != "RGBA":
        pil_image = pil_image.convert("RGBA")
    mode = pil_image.mode
    size = pil_image.size
    data = pil_image.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()

class Player:
    def __init__(self):
        try:
            self.image = pygame.image.load("assets/run_away.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (100, 100)) # サイズ調整
        except:
            self.image = pygame.Surface((100, 100))
            self.image.fill((0, 200, 255))

        self.rect = self.image.get_rect(center=(400, 300))
        # ★追加：画像の透明じゃない部分の「型」をとる
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = 5
        self.hp = 3
        self.invincible_timer = 0 # 無敵時間の残り時間（フレーム数）

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:    self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:  self.rect.y += self.speed
        if keys[pygame.K_LEFT]:  self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed

        # 画面外に出ないように制限
        self.rect.clamp_ip(pygame.Rect(0, 0, 800, 600))

        # 無敵時間のカウントダウン
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    def draw(self, screen):
        # 無敵時間中は点滅させる（少し透明にするなど、見た目の変化）
        if self.invincible_timer % 10 < 5: 
            screen.blit(self.image, self.rect)

class Enemy:
    def __init__(self):
        try:
            pil_img = Image.open("assets/enemy.png").convert("RGBA")
            # エネミーも同様に縦横比を維持してリサイズ
            self.image = pil_to_surface(pil_img,(300, 300))
        except:
            self.image = pygame.Surface((100, 100))
            self.image.fill((255, 0, 0))
        
        self.rect = self.image.get_rect(topleft=(20, 20)) #敵の初期位置
        # ★追加：敵の画像の「型」もとる
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = 2

    def update(self, player_rect):
        if self.rect.x < player_rect.x: self.rect.x += self.speed
        if self.rect.x > player_rect.x: self.rect.x -= self.speed
        if self.rect.y < player_rect.y: self.rect.y += self.speed
        if self.rect.y > player_rect.y: self.rect.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Background:
    def __init__(self):
        try:
            # 背景画像の読み込み
            pil_bg = Image.open("assets/background.png").convert("RGBA")
            # 背景は thumbnail ではなく、画面サイズ(800x600)にきっちり合わせる
            pil_bg = pil_bg.resize((800, 600), Image.Resampling.LANCZOS)

            # 背景専用の変換処理（縮小されないように直接書きます）
            mode = pil_bg.mode
            size = pil_bg.size
            data = pil_bg.tobytes()
            self.image = pygame.image.fromstring(data, size, mode).convert_alpha()

        except:
            # 画像がない場合は緑色の塗りつぶし
            self.image = pygame.Surface((800, 600))
            self.image.fill((34, 139, 34))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# スマホでキャラ移動ができるよう画面上のボタンをプログラムに取り組む
class Controller:
    def __init__(self):
        # 画面の右下あたりに配置するボタンの枠(Rect)を作る
        # (横位置, 縦位置, 幅, 高さ)
        self.up_rect = pygame.Rect(700, 450, 50, 50)
        self.down_rect = pygame.Rect(700, 530, 50, 50)
        self.left_rect = pygame.Rect(640, 490, 50, 50)
        self.right_rect = pygame.Rect(760, 490, 50, 50)

    def draw(self, screen):
        # 半透明のボタンを描く
        for r in [self.up_rect, self.down_rect, self.left_rect, self.right_rect]:
            pygame.draw.rect(screen, (255, 255, 255, 100), r, 2) # 白い枠線

    def get_input(self):
        # マウス（または指）が押されているかチェック
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0] # 左クリック
        
        result = {"up": False, "down": False, "left": False, "right": False}
        
        if mouse_pressed:
            if self.up_rect.collidepoint(mouse_pos):    result["up"] = True
            if self.down_rect.collidepoint(mouse_pos):  result["down"] = True
            if self.left_rect.collidepoint(mouse_pos):  result["left"] = True
            if self.right_rect.collidepoint(mouse_pos): result["right"] = True
            
        return result

async def play_game(screen):

    # --- ゲーム用BGMに切り替え ---
    # try:
    #  pygame.mixer.music.load("assets/game_bgm.ogg")
    #  pygame.mixer.music.play(-1)
    # except:
    #  print("BGM load failed")

    bg = Background()
    player = Player()
    enemy = Enemy()
    # スマホ用コントローラーの準備
    controller = Controller()

    clock = pygame.time.Clock()
    score = 0

    font_name = None
    font_ui = pygame.font.SysFont(font_name, 48)
    # カウントダウン用の大きなフォント
    font_count = pygame.font.SysFont(font_name, 150)
    font_basic = pygame.font.SysFont(font_name, 32)

    # 開始時間を記録
    start_ticks = pygame.time.get_ticks()

    # 文字を表示するための準備（フォント）
    font = pygame.font.SysFont(None, 48)

    running = True
    while running:
        # 1. 経過時間とカウントダウンの計算
        current_ticks = pygame.time.get_ticks()
        seconds = (current_ticks - start_ticks) // 1000
        countdown = 3 - seconds

        # 2. イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT", 0

        # 3. 入力処理（キーボード + スマホ用コントローラー）
        keys = pygame.key.get_pressed()
        ctrl_input = controller.get_input()

        # --- 更新処理 ---
        # カウントダウンが終わった(0以下)ときだけ動かす
        if countdown <= 0:
            # プレイヤーの移動（スマホボタン入力も反映）
            if ctrl_input["up"]:    player.rect.y -= player.speed
            if ctrl_input["down"]:  player.rect.y += player.speed
            if ctrl_input["left"]:  player.rect.x -= player.speed
            if ctrl_input["right"]: player.rect.x += player.speed

            player.update()
            enemy.update(player.rect)
        
        # ★追加：1フレーム（1/60秒）ごとに、少しずつスコアを増やす
            # 60回足されると、ちょうど「1秒」分くらいになります
            score += 1 / 60 

        # ★修正：四角(colliderect)ではなく、マスク(overlap)で判定
        # 1. まず「二人の位置のズレ」を計算する
        offset_x = enemy.rect.x - player.rect.x #敵と自分のX座標の引き算をして、どれくらい離れているか（ズレ）を出している
        offset_y = enemy.rect.y - player.rect.y
        
        # 2. プレイヤーのマスクと敵のマスクが「重なっているか」チェック
        if player.mask.overlap(enemy.mask, (offset_x, offset_y)) and player.invincible_timer <= 0:
            
            player.hp -= 1
            player.invincible_timer = 60 # 約1秒間の無敵（60フレーム）

            if player.hp <= 0:
                # 3回当たったのでゲームオーバー
                print("ゲームオーバー！タイトルに戻ります。")
                return "GAMEOVER",int(score) # これでmain02のループがGAMEOVERを返す 「文字」と「スコア」を返す

        # 3. 描画
        bg.draw(screen)
        player.draw(screen)
        enemy.draw(screen)
        controller.draw(screen) # ボタンを表示

        # UI表示
        score_text = font_ui.render(f"SCORE: {int(score)}s", True, (255, 255, 255))
        screen.blit(score_text, (20, 70)) # スコア表示

        # ライフを画面に表示
        hp_text = font.render(f"LIFE: {player.hp}", True, (255, 255, 255))
        screen.blit(hp_text, (20, 20))


        # --- カウントダウンの表示 ---
        if countdown > 0:
            # 少し背景を暗くする（お好みで）
            overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100)) # 黒の半透明
            screen.blit(overlay, (0, 0))
            
            # 文字を作成
            count_text = font_count.render(str(countdown), True, (255, 215, 0)) # ゴールド色
            count_rect = count_text.get_rect(center=(400, 300))
            
            screen.blit(count_text, count_rect)
            # ★ここで if countdown > 0 のブロックを終わらせる

        pygame.display.flip()
        clock.tick(60)

        await asyncio.sleep(0)  # ★ゲームオーバー判定は「カウント中かどうか」に関係なくチェックする場所に置く


    return "GAMEOVER", int(score)
