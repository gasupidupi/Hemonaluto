"""test save handler module"""
import unittest
from elements.activator import Activator
from elements.animate import Animate
from elements.chest import Chest
from elements.door import Door
from elements.element import Element
from elements.food import Food
from elements.location import Location
from elements.player import Player
from elements.rope import Rope
from elements.thing import Thing
from elements.tool import Tool
from enums.activator_type import ActivatorType
from save_handler import SaveHandler


class TestSaveHandler(unittest.TestCase):
    """Test SaveHandler class"""

    def setUp(self):
        """Set up environment required for tests"""
        self.save_handler = SaveHandler()
        self.names_locations, self.player_location = self.save_handler.load("tests/test_world.json")

    def test_load_names_locations(self):
        """Test if it loads names_locations correctly"""
        name = self.names_locations[0][0]
        location: Location = self.names_locations[0][1]
        self.assertEqual("test", name)
        self.assertEqual("test", location.name)
        self.assertEqual("test", location.description)
        self.assertEqual("Location", location.class_name)
        self.assertEqual("test", location.brief)
        self.assertEqual(True, location.has_light)
        self.assertEqual(True, location.needs_rope)
        self.assertEqual(11, len(location.contents))
        self.assertEqual("test", location.exits["test"])

    def test_load_contents(self):
        """Test if all elements get loaded correctly"""
        location: Location = self.names_locations[0][1]
        for element in location.contents:
            if isinstance(element, Activator) or issubclass(element.__class__, Activator):
                self.assertEqual(element.type, ActivatorType.PRESS)
                self.assertEqual(element.is_on, True)
                self.assertEqual(element.turn_on_method_name, "test_turn_on_method")
                self.assertEqual(element.turn_off_method_name, "test_turn_off_method")
            if isinstance(element, Animate) or issubclass(element.__class__, Animate):
                self.assertEqual(element.clothes, ["test"])
                self.assertEqual(element.health, "test")
            if isinstance(element, Chest) or issubclass(element.__class__, Chest):
                self.assertEqual(element.open, True)
                self.assertEqual(element.locked, True)
                self.assertEqual(element.key, "test")
                self.assertEqual(element.peekable, True)
            if isinstance(element, Door) or issubclass(element.__class__, Door):
                self.assertEqual(element.open, True)
                self.assertEqual(element.lockable, True)
                self.assertEqual(element.locked, True)
                self.assertEqual(element.key, "test")
                self.assertEqual(element.connects, ["test"])
            if isinstance(element, Element) or issubclass(element.__class__, Element):
                self.assertEqual(element.visible, True)
                self.assertEqual(element.contents[0].name, "test")
                #self.assertEqual(element.preposition, "test")
                self.assertEqual(element.sound, "test")
                self.assertEqual(element.smell, "test")
            if isinstance(element, Food) or issubclass(element.__class__, Food):
                self.assertEqual(element.regen, 50)
                self.assertEqual(element.taste, "test")
            if isinstance(element, Player) or issubclass(element.__class__, Player):
                self.assertEqual(element.clothes, ["test"])
                self.assertEqual(element.hiding, True)
            if isinstance(element, Rope) or issubclass(element.__class__, Rope):
                self.assertEqual(element.tied_to, "test")
            if isinstance(element, Thing) or issubclass(element.__class__, Thing):
                self.assertEqual(element.when_broken_do, "test_broken_method")
                self.assertEqual(element.reveals, "test")
                self.assertEqual(element.moved, True)
                self.assertEqual(element.fixed, True)
                self.assertEqual(element.visible, True)
                self.assertEqual(element.enterable, True)
                self.assertEqual(element.wearable, True)
                self.assertEqual(element.text, "test")
            if isinstance(element, Tool) or issubclass(element.__class__, Tool):
                self.assertEqual(element.damage, 50)
                self.assertEqual(element.durability, 50)