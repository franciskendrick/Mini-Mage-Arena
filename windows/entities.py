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
    # enemies = [Boomshroom()]
    enemies = []
    update_enemies = []

    # Supports
    # mana_crystals = [ManaCrystal((100, 100)) for _ in range(10)]
    mana_crystals = []

    # healing_potions = [HealingPotion()]
    healing_potions = [StaminaPotion()]
    # healing_potions = []

    # Return Entities
    entities = [
        player, 
        player_gauge, 
        [enemies, update_enemies], 
        [mana_crystals, healing_potions]]
    return entities
