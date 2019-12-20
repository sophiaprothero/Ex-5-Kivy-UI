import os
import pygame

os.environ['KIVY_GL_BACKEND'] = 'sdl2'

from kivy.core.window import Window

os.environ['DISPLAY'] = ":0.0"
os.environ['KIVY_WINDOW'] = 'egl_rpi'

# ------------------------- all imports -------------------------
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from JoystickGame import JoystickScreen
from datetime import datetime
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from kivy.animation import AnimationTransition
from kivy.graphics import Color, Rectangle
from kivy.uix.slider import Slider
from threading import Thread
from time import sleep
# -----------------------------------------------------------------

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
IMAGE_SCREEN_NAME = 'image'
PAUSE_SCREEN_NAME = 'pauseGame'


class ProjectNameGUI(App):

    def build(self):
        return SCREEN_MANAGER
# Launches Window Manager


Window.clearcolor = (0.7, 0.7, 0.7, 1)
# Initial Window Color


class MainScreen(Screen):
    counter = ObjectProperty(None)
    button_state = ObjectProperty(None)

    global motor_val
    motor_val = "Motor Off"

    global x_value
    x_value = 0

    global sec_num
    sec_num = 1

    def motor_control_switch(self):
        if self.motor_text() == 'Off':
            self.motorToggle.text = "Motor On"

        elif self.motor_text() == 'On':
            self.motorToggle.text = "Motor Off"

    def motor_text(self):
        if self.motorToggle.text == "Motor Off":
            return 'Off'

        elif self.motorToggle.text == "Motor On":
            return 'On'

    def counter_button(self):
        global x_value
        x_value = x_value + 1
        self.counter.text = "%d" % x_value

    def image_transition_anim(self):
        Clock.schedule_once(self.image_transition, 1)

        anim = Animation(pos=(-9500, -9000), size=(20000, 20000), duration=1) + Animation(pos=(140, 300),
                                                                                          size=(250, 250), duration=0.1)
        anim.start(self.ids.screenButton)

    @staticmethod
    def image_transition(self):
        SCREEN_MANAGER.current = IMAGE_SCREEN_NAME

    @staticmethod
    def admin_action():
        SCREEN_MANAGER.current = 'passCode'

    @staticmethod
    def stick_go():
        SCREEN_MANAGER.current = 'stick'

    def color_animate(self):
        global sec_num

        anim = Animation(color=(1, 0.5, 0, 1), duration=sec_num) + Animation(color=(1, 1, 0, 1),
                                                                             duration=sec_num) + Animation(
            color=(0.5, 1, 0, 1), duration=sec_num) + Animation(color=(0, 1, 0, 1), duration=sec_num) + Animation(
            color=(0, 1, 0.5, 1), duration=sec_num) + Animation(color=(0, 1, 1, 1), duration=sec_num) + Animation(
            color=(0, 0.5, 1, 1), duration=sec_num) + Animation(color=(0, 0, 1, 1), duration=sec_num) + Animation(
            color=(0.5, 0, 1, 1), duration=sec_num) + Animation(color=(1, 0, 1, 1), duration=sec_num) + Animation(
            color=(1, 0, 0.5, 1), duration=sec_num) + Animation(color=(1, 0, 0, 1), duration=sec_num)

        anim.start(self.ids.colorButton)
# Main Screen Setup


class ImageScreen(Screen):

    def __init__(self, **kwargs):
        Builder.load_file('ImageScreen.kv')

        super(ImageScreen, self).__init__(**kwargs)

    def image_transition_anim_back(self):
        Clock.schedule_once(self.image_transition_back, 1)

        anim = Animation(pos=(-9500, -9000), size=(20000, 20000), duration=1) + Animation(pos=(500, 375),
                                                                                          size=(200, 200), duration=0.1)
        anim.start(self.ids.animatedImage)

    @staticmethod
    def image_transition_back(self):
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME
# Color Slider Screen Setup


class PauseGameScreen(Screen):

    def __init__(self, **kwargs):
        Builder.load_file('PauseGameScreen.kv')

        JoystickScreen.set_pause_screen(PAUSE_SCREEN_NAME)
        JoystickScreen.set_transition_back_screen(MAIN_SCREEN_NAME)

        super(PauseGameScreen, self).__init__(**kwargs)

    @staticmethod
    def go_unpause():
        SCREEN_MANAGER.current = 'stick'

    @staticmethod
    def transition_back():
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME
# Pause Screen Setup


class AdminScreen(Screen):

    def __init__(self, **kwargs):
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        quit()
# Screen For Admin Actions


# ----------------- Screen Declarations -----------------------
Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseGameScreen(name=PAUSE_SCREEN_NAME))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(ImageScreen(name=IMAGE_SCREEN_NAME))
SCREEN_MANAGER.add_widget(JoystickScreen(name='stick'))
# -------------------------------------------------------------


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()
# MixPanel Events


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
# Execute GUI
