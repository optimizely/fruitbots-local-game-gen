#!/usr/bin/env python

import os
import shutil
import sys

PLAYER_1_SUB = '[REPLACE_WITH_PLAYER_1]'
PLAYER_2_SUB = '[REPLACE_WITH_PLAYER_2]'

player_1 = sys.argv[1]
player_2 = sys.argv[2]

cwd = os.getcwd()

game_name = 'fruitbots-%s-v-%s' % (player_1, player_2)

if not os.path.isdir('tournament'):
    os.mkdir('tournament')

shutil.copytree('../robot-fruit-hunt', os.path.join('tournament', game_name))

# Move to the game's dir.
os.chdir(os.path.join('tournament', game_name))

def get_bot_src(player):
    return os.path.join('bots', player + '.js')

def namespace_function(player_code, fn_name, player_num):
    for i, line in enumerate(player_code):
        if fn_name in line:
            player_code[i] = line.replace(fn_name, fn_name + '_' + str(player_num))
    return player_code

def switch_position_and_item_count_functions(player_code):
    # switches get_my_x, get_my_y with get_opponent_x and get_opponent_y
    for i, line in enumerate(player_code):
        line = line.replace('get_my_x', 'want_my_x').replace('get_my_y', 'want_my_y')
        line = line.replace('get_opponent_x', 'get_my_x').replace('get_opponent_y', 'get_my_y')
        line = line.replace('want_my_x', 'get_opponent_x').replace('want_my_y', 'get_opponent_y')
        line = line.replace('get_my_item_count', 'want_my_item_count')
        line = line.replace('get_opponent_item_count', 'get_my_item_count')
        line = line.replace('want_my_item_count', 'get_opponent_item_count')
        player_code[i] = line
    return player_code

shutil.copyfile(get_bot_src(player_1), 'player_1.js')
shutil.copyfile(get_bot_src(player_2), 'player_2.js')

# Namespace functions
for player_num in [1, 2]:
    lines = None
    with open('player_%s.js' % player_num) as player_src:
        lines = player_src.readlines()
        lines = namespace_function(lines, 'new_game', player_num)
        lines = namespace_function(lines, 'make_move', player_num)
        if player_num == 2:
            lines = switch_position_and_item_count_functions(lines)
    with open('player_%s.js' % player_num, 'w') as player_src:
        player_src.write(''.join(lines))


# Sub player names
player_asset = 'assets/js/player.js'
lines = None
with open(player_asset) as player_file:
    lines = player_file.readlines()

for i, line in enumerate(lines):
    if PLAYER_1_SUB in line:
        lines[i] = line.replace(PLAYER_1_SUB, player_1)
    if PLAYER_2_SUB in line:
        lines[i] = line.replace(PLAYER_2_SUB, player_2)

with open(player_asset, 'w') as player_file:
    player_file.write(''.join(lines))

os.system('open game.html')
