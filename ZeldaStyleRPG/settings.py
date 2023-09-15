# Configuração da janela
width = 1290
height = 720

# frames por segundo
fps = 60

# Cores
tileSize = 64

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\font\\joystix.ttf'
UI_FONT_SIZE = 18

# cores gerais
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# cores da ui
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# deficinao das armas
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': 'projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\weapons\\sword\\full.png'},
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': 'projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\weapons\\lance\\full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': 'projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\weapons\\axe\\full.png'},
    'rapier': {'cooldown': 50, 'damage': 8, 'graphic': 'projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\weapons\\rapier\\full.png'},
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': 'projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\weapons\\sai\\full.png'},
}

# magica
magic_data = {
    'flame': {'strenght': 5, 'cost': 20, 'graphic': 'projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\flame\\fire.png'},
    'heal': {'strenght': 20, 'cost': 10, 'graphic': 'projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\heal\\heal.png'}
}

# enemy
monster_data = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'../audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'../audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}

