"""Generates the game world"""


from elements.activator import Activator
from elements.door import Door
from elements.food import Food
from elements.location import Location
from elements.player import Player
from elements.rope import Rope
from elements.thing import Thing
from elements.tool import Tool
from save_handler import SaveHandler
from texts import BED_DESCRIPTION, BED_NAME, BEDROOM_BUTTON_DESCRIPTION, BEDROOM_BUTTON_NAME,\
BEDROOM_DESCRIPTION, BEDROOM_DOOR_DESCRIPTION,\
BEDROOM_DOOR_NAME, BEDROOM_HOOK_DESCRIPTION, BEDROOM_HOOK_NAME, BEDROOM_KEY_DESCRIPTION,\
BEDROOM_KEY_NAME, BEDROOM_NAME, BEDROOM_PILE_OF_DUST_DESCRIPTION, BEDROOM_PILE_OF_DUST_NAME, BEDROOM_RUG_DESCRIPTION, BEDROOM_RUG_NAME, BREAKFAST_KNIFE_DESCRIPTION, BREAKFAST_KNIFE_NAME, CELLAR_DESCRIPTION, CELLAR_NAME, DINING_ROOM_CRATE_DESCRIPTION, DINING_ROOM_CRATE_NAME, DINING_ROOM_DESCRIPTION, DINING_ROOM_FOOD_DESCRIPTION, DINING_ROOM_FOOD_NAME, DINING_ROOM_FOOD_TASTE,\
DINING_ROOM_NAME, DINING_ROOM_PLATE_DESCRIPTION, DINING_ROOM_PLATE_NAME, DINING_ROOM_TABLE_DESCRIPTION, DINING_ROOM_TABLE_NAME, DINING_ROOM_TRAPDOOR_DESCRIPTION, DINING_ROOM_TRAPDOOR_NAME, DOWN, EAST, PLAYER_DESCRIPTION, PLAYER_NAME, ROPE_DESCRIPTION, ROPE_NAME, WEST


all_name_locations = []
# bedroom
bedroom = Location(BEDROOM_NAME, BEDROOM_DESCRIPTION)
# dining room
dining_room = Location(DINING_ROOM_NAME, DINING_ROOM_DESCRIPTION)
# cellar
cellar = Location(CELLAR_NAME, CELLAR_DESCRIPTION)
# player
player = Player(PLAYER_NAME, PLAYER_DESCRIPTION, 100)
# things in bedroom
bed = Thing(BED_NAME, BED_DESCRIPTION)
bed.fixed = True
bedroom_door = Door(BEDROOM_DOOR_NAME, BEDROOM_DOOR_DESCRIPTION)
bedroom_door.connects.append(dining_room.name)
bedroom_door.locked = True
bedroom_key = Thing(BEDROOM_KEY_NAME, BEDROOM_KEY_DESCRIPTION)
bedroom_key.text = "B"
bedroom_door.key = bedroom_key.name
bedroom_hook = Thing(BEDROOM_HOOK_NAME, BEDROOM_HOOK_DESCRIPTION)
bedroom_hook.fixed = True
bedroom_hook.contents.append(bedroom_key)
bedroom_rug = Thing(BEDROOM_RUG_NAME, BEDROOM_RUG_DESCRIPTION)
bedroom_button = Activator(BEDROOM_BUTTON_NAME, BEDROOM_BUTTON_DESCRIPTION)
bedroom_button.type = "push"
bedroom_button.turn_on_method_name = "bedroom_button_on"
bedroom_button.turn_off_method_name = "bedroom_button_off"
bedroom_pile_of_dust = Thing(BEDROOM_PILE_OF_DUST_NAME, BEDROOM_PILE_OF_DUST_DESCRIPTION)
bedroom_pile_of_dust.visible = False
bedroom_rug.reveals = bedroom_pile_of_dust.name
# bedroom exits
bedroom.exits[WEST] = dining_room.name
# bedroom contents
bedroom.contents.extend([player, bed, bedroom_door, bedroom_hook,\
bedroom_rug, bedroom_button, bedroom_pile_of_dust])
# dining room exits
dining_room.exits[EAST] = bedroom.name
dining_room.exits[DOWN] = cellar.name
# things in dining room
dining_room_table = Thing(DINING_ROOM_TABLE_NAME, DINING_ROOM_TABLE_DESCRIPTION)
dining_room_table.preposition = "on"
dining_room_plate = Thing(DINING_ROOM_PLATE_NAME, DINING_ROOM_PLATE_DESCRIPTION)
dining_room_plate.preposition = "on"
dining_room_breakfast = Food(DINING_ROOM_FOOD_NAME, DINING_ROOM_FOOD_DESCRIPTION)
dining_room_breakfast.taste = DINING_ROOM_FOOD_TASTE
dining_room_trapdoor = Door(DINING_ROOM_TRAPDOOR_NAME, DINING_ROOM_TRAPDOOR_DESCRIPTION)
rope = Rope(ROPE_NAME, ROPE_DESCRIPTION)
dining_room_crate = Thing(DINING_ROOM_CRATE_NAME, DINING_ROOM_CRATE_DESCRIPTION)
dining_room_crate.fixed = True
breakfast_knife = Tool(BREAKFAST_KNIFE_NAME, BREAKFAST_KNIFE_DESCRIPTION)
dining_room_plate.when_broken_do = "break_plate"
dining_room_plate.contents.append(dining_room_breakfast)
dining_room_table.contents.append(dining_room_plate)
dining_room_table.contents.append(breakfast_knife)
# dining room contents
dining_room.contents.append(bedroom_door)
dining_room.contents.append(dining_room_table)
dining_room.contents.append(dining_room_trapdoor)
dining_room.contents.append(rope)
dining_room.contents.append(dining_room_crate)
# cellar
cellar.needs_rope = True
# dining room door connections
bedroom_door.connects.append(bedroom.name)
# add all rooms to all_name_rooms list
all_name_locations.append((bedroom.name, bedroom))
all_name_locations.append((dining_room.name, dining_room))
all_name_locations.append((cellar.name, cellar))
save_handler = SaveHandler()
save_handler.save(all_name_locations, "scenario.json")
