from processes.wait import Wait
from processes.click import Click

from shapes.window import Window
from shapes.rect import Rect

from jobs.helpers.navigator import Navigator, get_npc
from utils.config import Config
from jobs.helpers.observer import Observer, observe_angle, observe_height
from jobs.helpers.handle_npc import HandleNpc
from jobs.helpers.configs import QuestMenu, AcceptQuest
from jobs.helpers.detector import Detector


config = Config()
class CircusHandler:

    def __init__(self):
        self.window = Window()

    def get_quest(self):
        obs = Observer(observe_angle, observe_height)
        obs.observe()


        Navigator.touch_npc(config.CharTitleConfig)

        HandleNpc().select_menu(config.QuestMenu)
        Wait(0.3).delay()

        HandleNpc().select_menu(config.AcceptQuest)
        Wait(0.3).delay()

        Navigator.turn_around()
        Wait(0.3).delay()


        center = Rect(config.StartPointConfig.roi).center()
        x, y = self.window.relative(center)
        Click(x, y).make_click()
        
        Wait(3).delay()
    
    def go_to_dungeon(self, party):
        if party:
            d = Detector(config.OkButton.path, Window()).detect()
            x, y, w, h = d
            x,y = Window().relative((x,y))
            Rect((x,y,w,h)).click().make_click()
            Click(x,y).make_click()

        Navigator.touch_npc(config.DungeonNpc)
        Wait(1).delay()
        HandleNpc().select_menu(config.CircusDungeonMenu)
        Wait(1).delay()
        x, y, w, h = config.StarIcon.roi
        x,y = Window().relative((x,y))
        Wait(1).delay()
        Detector(config.StarIcon.menu, Window()).detect()
        Rect((x,y,w,h)).click().make_click()
        npc = get_npc(config.CircusNpc)
        
        Navigator.click_at_npc(npc, config.CircusNpc)
        Wait(1).delay()
        
        npc_menu = HandleNpc().select_menu(config.CircusNpcMenu, quality='threshold')
        if not npc_menu:
            return None
            
        Wait(1).delay()
        npc_menu = HandleNpc().select_menu(config.FirstCircus)
        return npc_menu
