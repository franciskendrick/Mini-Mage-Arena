from windows import window
from game import PlayerGauge, game
from player import Player
from enemies import DarkMage, Slime
from supports import ManaCrystal
import pygame
import sys


# Redraw
def redraw_game():
    display.fill((50, 50, 70))

    # Window
    game.draw_statbar_bg(display)
    player_gauge.draw(display)

    # Player
    player.draw(display)

    # Enemies
    for enemy in enemies:
        enemy.draw(display)

    # Supports
    for mana in mana_crystals:
        mana.draw(display)

    # Blit to Screen ---------------------------------------------- #
    resized_display = pygame.transform.scale(display, win_size)
    win.blit(resized_display, (0, 0))

    pygame.display.update()


# Loop
def game_loop():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # Player
        player.update(enemies)

        # Enemies
        remove_enemies = []
        for enemy in enemies:
            enemy.update(player)

            if enemy.is_dead:
                remove_enemies.append(enemy)

        for enemy in remove_enemies:
            enemies.remove(enemy)
        
        # Player Gauge
        player_gauge.update(player.stats)

        # Update
        redraw_game()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # Window
    win_size = (
        window.rect.width * window.enlarge,
        window.rect.height * window.enlarge)
    win = pygame.display.set_mode(win_size)
    display = pygame.Surface(window.rect.size)
    pygame.display.set_caption("Mini Mage Arena")
    clock = pygame.time.Clock()

    # Player
    player = Player()

    # Windows
    player_gauge = PlayerGauge()

    # Enemies
    enemies = [DarkMage()]
    # enemies = []

    # Supports
    mana_crystals = [ManaCrystal((100, 100))]

    # Execute
    game_loop()
