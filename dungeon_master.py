"""dungeon master module"""
import random
from elements.chest import Chest
from elements.door import Door
from elements.location import Location
from elements.player import Player
from elements.thing import Thing
from save_handler import SaveHandler
from texts import BED_DESCRIPTION, BED_NAME, BEDROOM_DESCRIPTION, BEDROOM_DOOR_DESCRIPTION,\
    BEDROOM_DOOR_NAME, BEDROOM_HOOK_DESCRIPTION, BEDROOM_HOOK_NAME, BEDROOM_KEY_DESCRIPTION,\
    BEDROOM_KEY_NAME, BEDROOM_NAME, BEDROOM_RUG_DESCRIPTION, BEDROOM_RUG_NAME,\
    DINING_ROOM_DESCRIPTION, DINING_ROOM_NAME, EAST, ELEMENT_NOT_FOUND, GREETINGS, JUMP_RESPONSE,\
    KEY_MISSING, LOCATION_PREFIX, LOCATION_SUFFIX, SAVED_GAME_MESSAGE,\
    SWEAR_RESPONSE, door_not_locked, door_unlocked, GENERIC_LOCATAION_NAME, INVALID_DIRECTION,\
    LOCKED_DOOR, PLAYER_DESCRIPTION, PLAYER_NAME, WEST, picked_up_element, element_in_container


class DungeonMaster:
    """dungeon master class"""
    def __init__(self):
        self.player_location = None
        self.all_name_locations = []
        self.save_handler = SaveHandler()

    def generate_world(self):
        """Generates the game world"""
        # bedroom
        bedroom = Location(BEDROOM_NAME, BEDROOM_DESCRIPTION)
        # dining room
        dining_room = Location(DINING_ROOM_NAME, DINING_ROOM_DESCRIPTION)
        # things in bedroom
        player = Player(PLAYER_NAME, PLAYER_DESCRIPTION)
        bed = Thing(BED_NAME, BED_DESCRIPTION)
        bedroom_door = Door(BEDROOM_DOOR_NAME, BEDROOM_DOOR_DESCRIPTION)
        bedroom_door.connects.append(dining_room.name)
        bedroom_door.locked = True
        bedroom_key = Thing(BEDROOM_KEY_NAME, BEDROOM_KEY_DESCRIPTION)
        bedroom_door.key = bedroom_key.name
        bedroom_hook = Thing(BEDROOM_HOOK_NAME, BEDROOM_HOOK_DESCRIPTION)
        bedroom_hook.contents.append(bedroom_key)
        bedroom_rug = Thing(BEDROOM_RUG_NAME, BEDROOM_RUG_DESCRIPTION)
        # bedroom exits
        bedroom.exits[WEST] = dining_room.name
        # bedroom contents
        self.set_player_location(player, bedroom)
        bedroom.contents.append(bed)
        bedroom.contents.append(bedroom_door)
        bedroom.contents.append(bedroom_hook)
        bedroom.contents.append(bedroom_rug)
        # dining room exits
        dining_room.exits[EAST] = bedroom.name
        # dining room contents
        dining_room.contents.append(bedroom_door)
        bedroom_door.connects.append(bedroom.name)
        # add all rooms to all_name_rooms list
        self.all_name_locations.append((bedroom.name, bedroom))
        self.all_name_locations.append((dining_room.name, dining_room))

    def get_player(self):
        """Get the player object from the current location"""
        return self.get_element_container("Player", self.player_location)[0]

    def move_player(self, direction):
        """Move the player from one location to the next, which lies in the given direction"""
        if direction in self.player_location.exits:
            all_name_rooms_dict =  dict(self.all_name_locations)
            next_room = all_name_rooms_dict[self.player_location.exits[direction]]
            for element in self.player_location.contents:
                if isinstance(element, Door)\
                and next_room.name in element.connects\
                and element.locked:
                    return LOCKED_DOOR
            player = self.get_player()
            self.player_location.contents.remove(player)
            self.set_player_location(player, next_room)
            return self.player_location.name
        else:
            return INVALID_DIRECTION

    def unlock(self, door_name):
        """Unlocks and opens a door"""
        door = self.get_element_container(door_name, self.player_location)[0]
        if not door.locked:
            return door_not_locked(door_name)
        if any(element.name == door.key for element in self.get_player().contents):
            door.locked = False
            return door_unlocked(door_name)
        else:
            return KEY_MISSING

    def set_player_location(self, player, location):
        """Update the players location to a new one"""
        location.contents.append(player)
        self.player_location = location

    def describe(self, element_name):
        """Returns a desription of any kind of in-game element at the location of the player"""
        element_name = element_name.lower()
        if element_name == self.player_location.name or\
            element_name == GENERIC_LOCATAION_NAME or\
            element_name == "":
            return self.describe_location()
        else:
            return self.describe_element(element_name)

    def describe_location(self):
        """Describes the location where the player is"""
        return self.describe_container(self.player_location, (LOCATION_PREFIX, LOCATION_SUFFIX))

    def describe_element(self, element_name):
        """Get description of a single element"""
        element_container = self.get_element_container(element_name, self.player_location)
        if element_container:
            return self.describe_container(element_container[0])
        else:
            return ELEMENT_NOT_FOUND

    def describe_container(self, top_container, prefix_suffix=None):
        """Descsribe any container and its contents and all the contents contents etc."""
        if prefix_suffix:
            description = top_container.name + "\n" + prefix_suffix[0] +\
            top_container.description.lower() + prefix_suffix[1]
        else:
            description = top_container.description
        visible_elements = self.get_all_elements_container(top_container, True)
        for element_container in visible_elements:
            if element_container[1] is not self.get_player():
                if element_container[1] is not self.player_location:
                    description = description + "\n" +\
                    element_in_container(element_container[0].name, element_container[1].name)
                else:
                    if not isinstance(element_container[0], Player):
                        description = description + "\n" + element_container[0].description
        return description

    def get_element_container(self, element_name, container):
        """Get an element in the container
        by its name and the corresponding container.
        If it's not found it returns None"""
        for element_container in self.get_all_elements_container(container, True):
            element = element_container[0]
            if element.name.lower() == element_name.lower():
                return (element, element_container[1])
        return None

    def get_all_elements_container(self, container, only_visible):
        """Recursive method to get all elements in the container
        and their corresponding container. If there is nothing it returns None"""
        elements_container = []
        for element in container.contents:
            if only_visible:
                if element.visible:
                    elements_container.append((element, container))
                if isinstance(element, Chest) and not element.peekable or\
                isinstance(element, Chest) and not element.open:
                    pass
                else:
                    elements_container = elements_container +\
                    self.get_all_elements_container(element, only_visible)
            if not only_visible:
                elements_container.append((element, container))
                elements_container = elements_container +\
                self.get_all_elements_container(element, only_visible)
        return elements_container

    def take(self, element_name):
        """Take an element and put it into the players inventory"""
        element_container = self.get_element_container(element_name, self.player_location)
        if not element_container:
            return ELEMENT_NOT_FOUND
        element_container[1].contents.remove(element_container[0])
        self.get_player().contents.append(element_container[0])
        return picked_up_element(element_container[0].name)

    def get_player_inventory(self):
        """Returns the invenotry of the player as a string listing all things"""
        description = ""
        for element in self.get_player().contents:
            description = description + element.name
        return description

    def greet(self):
        """Returns the greeting"""
        return random.choice(GREETINGS)

    def swear_response(self):
        """Responds to swearing by a player"""
        return SWEAR_RESPONSE

    def jump_response(self):
        """Responds to the player jumping"""
        return JUMP_RESPONSE

    def save(self):
        """Saves the game state to file"""
        if self.save_handler.save(self.all_name_locations):
            return SAVED_GAME_MESSAGE

    def load(self):
        """Loads the game state from file"""
        load_data = self.save_handler.load(self.all_name_locations)
        self.all_name_locations = load_data[0]
        self.player_location = load_data[1]
