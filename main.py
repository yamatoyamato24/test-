import pygame
import asyncio

async def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 80)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 50, 150)) # 青い画面
        text = font.render("HELLO PYGBAG!", True, (255, 255, 255))
        screen.blit(text, (200, 250))
        
        pygame.display.flip()
        
        # Web版の必須セット
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

# 起動部分
asyncio.run(main())
