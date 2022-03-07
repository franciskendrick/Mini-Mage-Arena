from windows import window
from game import PlayerGauge, game
from player import Player
from enemies import DarkMage, Fireshroom, Mushroom, Slime
from supports import HealingPotion, ManaCrystal
import pygame
import sys


# Redraw
def redraw_game():
    display.fill((100, 100, 120))

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
    for potion in healing_potions:
        potion.draw(display)

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
                enemy.mana_reward(mana_crystals)
                remove_enemies.append(enemy)

        for enemy in remove_enemies:
            enemies.remove(enemy)
        
        # Mana Crystals
        remove_mana = []
        for mana in mana_crystals:
            mana.update(player, mana_crystals)
            if mana.absorbed:
                remove_mana.append(mana)

        for mana in remove_mana:
            if mana in mana_crystals:
                mana_crystals.remove(mana)

        # Healing Potion
        remove_potion = []
        for potion in healing_potions:
            potion.update(player)
            if potion.absorbed:
                remove_potion.append(potion)

        for potion in remove_potion:
            if potion in healing_potions:
                healing_potions.remove(potion)

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
    enemies = [Fireshroom()]
    # enemies = []

    # Supports
    # mana_crystals = [ManaCrystal((100, 100)) for _ in range(10)]
    mana_crystals = []

    # healing_potions = [HealingPotion()]
    healing_potions = []

    # Execute
    game_loop()
