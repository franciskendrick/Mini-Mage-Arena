from enemies import Slime, DarkMage, Mushroom, Fireshroom, Boomshroom, NormalKnight
from supports import HealingPotion, ManaCrystal, StaminaPotion
from player import Player
from windows.game import PlayerGauge


def init():
    # Player
    player = Player()

    # Windows
    player_gauge = PlayerGauge()

    # Enemies
    enemies = [NormalKnight()]
    # enemies = []
    update_enemies = []

    # Supports
    # healing_potions = [HealingPotion()]
    healing_potions = []

    # mana_crystals = [ManaCrystal((100, 100)) for _ in range(10)]
    mana_crystals = []

    # stamina_potions = [StaminaPotion()]
    stamina_potions = []
    update_stamina_potions = []

    # Return Entities
    entities = [
        player, 
        player_gauge, 
        [enemies, update_enemies], 
        [healing_potions, mana_crystals, [stamina_potions, update_stamina_potions]]]
    return entities
