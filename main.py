from enemies import Boomshroom
from windows import window, background, entities
from windows.menu import menu
import pygame
import sys


# Functions
def placeholder():  # !!!   
    pass


# Redraw
def redraw_game():
    all_enemies_list = enemies + update_enemies
    enemies_list = []
    exploded_boomshrom_list = []
    for enemy in all_enemies_list:
        if isinstance(enemy, Boomshroom) and enemy.exploded:
            exploded_boomshrom_list.append(enemy)
        else:
            enemies_list.append(enemy)

    # Background
    background.draw_background(display)
    background.draw_inside_arena(display)

    # Enemies
    for enemy in enemies_list:
        enemy.draw(display)
    
    # Supports
    for mana in mana_crystals:
        mana.draw(display)
    for potion in healing_potions:
        potion.draw(display)
    for potion in stamina_potions:
        potion.draw(display)

    # Player
    player.draw(display)

    # Background
    background.draw_outside_arena(display)

    # Exploded Boomshroom
    for enemy in exploded_boomshrom_list:
        enemy.draw(display)

    # Status Bar
    player_gauge.draw(display)

    # Blit to Screen ---------------------------------------------- #
    resized_display = pygame.transform.scale(display, win_size)
    win.blit(resized_display, (0, 0))

    pygame.display.update()


def redraw_menu():
    # Menu
    menu.draw(display)

    # Player
    player.draw_sprite(display)

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

            if enemy.delete:
                enemy.mana_reward(mana_crystals)
                remove_enemies.append(enemy)
            elif enemy.is_dead:
                enemy.mana_reward(mana_crystals)
                remove_enemies.append(enemy)
                update_enemies.append(enemy)

        for enemy in remove_enemies:
            enemies.remove(enemy)

        # Update Enemies
        remove_enemies = []
        for enemy in update_enemies:
            enemy.dead_update(player)

            if enemy.delete:
                remove_enemies.append(enemy)

        for enemy in remove_enemies:
            update_enemies.remove(enemy)

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

        # Stamina Potion
        remove_potion = []
        for potion in stamina_potions:
            potion.update(player)
            if potion.absorbed:
                update_stamina_potions.append(potion)
                remove_potion.append(potion)

        for potion in remove_potion:
            if potion in stamina_potions:
                stamina_potions.remove(potion)

        # Update Stamina Potion
        remove_potion = []
        for potion in update_stamina_potions:
            potion.update(player)
            if potion.absorbed and potion.effect_lasted:
                remove_potion.append(potion)

        for potion in remove_potion:
            if potion in stamina_potions:
                stamina_potions.remove(potion)

        # Player Gauge
        player_gauge.update(player.stats)

        # Update
        redraw_game()
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


def menu_loop():
    btn_switchcase = {
        "play": [game_loop],
        "options": [placeholder],
        None: [placeholder]
    }

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Menu Buttons
        btn_pressed = menu.get_button_pressed(event)
        for function in btn_switchcase[btn_pressed]:
            function()
        menu.handle_mousemotion(event)

        # Player
        player.facing()

        # Update
        redraw_menu()   
        clock.tick(window.framerate)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.init()

    # Window
    win_size = (
        window.rect.width * window.enlarge,
        window.rect.height * window.enlarge)
    win = pygame.display.set_mode(win_size)
    display = pygame.Surface(window.rect.size)
    pygame.display.set_caption("Mini Mage Arena")
    clock = pygame.time.Clock()

    # Entities
    [
        player, player_gauge, 
        (enemies, update_enemies), 
        (healing_potions, mana_crystals, (stamina_potions, update_stamina_potions))
    ] = entities.init()

    # Execute
    game_loop()
