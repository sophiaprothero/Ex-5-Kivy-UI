import os
import pygame

# ------------------------- all imports -------------------------
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from datetime import datetime
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from kivy.animation import AnimationTransition
from kivy.graphics import Color, Rectangle
from kivy.uix.slider import Slider
from threading import Thread
from time import sleep
import os.path
from pidev.Joystick import Joystick
# -----------------------------------------------------------------

joystick_screen_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "", "JoystickGame.kv")

Builder.load_file(joystick_screen_path)

PAUSE_GAME_SCREEN = None
TRANSITION_BACK_SCREEN = 'main'

Joysticky = Joystick(0, True)

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()


class JoystickScreen(Screen):

    button_state = ObjectProperty(None)
    stick_x_val = ObjectProperty(None)
    stick_y_val = ObjectProperty(None)

    def __init__(self, **kw):
        super(JoystickScreen, self).__init__(**kw)

    def get_stick_values(self):
        while 1:
            self.stick_x_val = Joysticky.get_axis('x')
            self.stick_y_val = Joysticky.get_axis('y')
            sleep(0.01)

    def joy_button_update(self):
        while 1:
            if Joysticky.get_button_state(0) == 1:
                self.button0.text = "On"
                sleep(0.01)
            else:
                self.button0.text = "Off"

    def cursor_position(self):
        while 1:
            self.stick_cursor.pos = (self.stick_x_val * 400, self.stick_y_val * 275)
            sleep(0.01)

    def start_joy_thread(self):
        Thread(target=self.joy_button_update).start()
        Thread(target=self.get_stick_values).start()
        Thread(target=self.cursor_position).start()

    def go_pause(self):
        self.parent.current = PAUSE_GAME_SCREEN

    @staticmethod
    def set_transition_back_screen(screen):
        global TRANSITION_BACK_SCREEN
        TRANSITION_BACK_SCREEN = screen

    @staticmethod
    def set_pause_screen(screen):
        global PAUSE_GAME_SCREEN
        PAUSE_GAME_SCREEN = screen
