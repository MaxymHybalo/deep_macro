import os
import sys
import time

from win32 import win32gui as api
from win32.lib import win32con as con
from win32api import GetSystemMetrics

import pyautogui as ui

from processes.wait import Wait
from driver import send
from utils.deep_utils import get_active_windows, get_window_coord, _foreground_window
from processes.click import Click
import config

path = 'D:\Games\RappelzSpace'
launcher = 'Launcher.exe'
credentials = 'credentials.yml'
launcher_name = 'Launcher'
game = 'Rappelz'

# login vars
login_point = (615, 535)
pasword_point = (615, 565)
submit_point = (700, 600)
desktop = (GetSystemMetrics(0), GetSystemMetrics(1))
server_point = (970, 610)

print('Desktop:', desktop)

def _to_absolute(pt, coords):
    x, y, _, _ = coords
    x1, y1 = pt
    return x + x1, y + y1

def run_clients(count=3):
    os.chdir(path)
    for _ in range(count):
        os.popen(launcher_name)
    time.sleep(1)
    wnd = get_active_windows(launcher_name)

    for i, handle in enumerate(wnd):
        l, t, w, h = get_window_coord(handle)
        api.SetWindowPos(handle, con.HWND_TOP, int(desktop[0] / 2 - w / 2), 100*(i + 1) + h*i,w, h, 0)

    for handle in wnd:
        l, t, w, h = get_window_coord(handle)
        time.sleep(1)
        api.SetActiveWindow(handle)
        time.sleep(1)
        Click(l + w - 50, t + h - 25).make_click()

def one():
    run_clients(1)

# print(os.getcwd())
def fill_games_grid(coord):
    desktop_x, desktop_y = desktop
    _, _, w, h = coord
    return {
        0: (0, 0),
        1: (desktop_x - w, 0),
        2: (int(desktop_x / 2 - w / 2), desktop_y - h - 50)
    }

def justify_games():
    games = get_active_windows(game)

    for i, g in enumerate(games):
        # set active window
        _foreground_window(g)
        coord = get_window_coord(g)
        grid = fill_games_grid(coord)
        x, y = grid[i]
        _, _, w, h = coord
        api.SetWindowPos(g, con.HWND_TOP, x, y, w, h, 0)

def _set_field(coord, pt, cred): 
    lx, ly = _to_absolute(pt, coord)
    Click(lx, ly).make_click()
    Wait(0.2).delay()
    ui.write(cred, interval=0.01)

def login():
    games = get_active_windows(game)
    logins = config.load_config('{0}/{1}'.format(path, credentials))
    for i, g in enumerate(games):
        # set active window
        _foreground_window(g)
        Wait(0.2).delay()

        cr = logins['credentials'][i]
        login, password = cr['login'], cr['password']
        print(login, password)
        coord = get_window_coord(g)

        Wait(0.1).delay()
        _set_field(coord, login_point, login)
        Wait(0.1).delay()
        _set_field(coord, pasword_point, password)

        submit = _to_absolute(submit_point, coord)
        sx, sy = submit
        Click(sx, sy, submit).make_click()

    for i, g in enumerate(games):
        Wait(2).delay()
        x, y = _to_absolute(server_point, get_window_coord(g))
        Click(x, y).make_click()


launch_map = {
    'run': run_clients,
    'justify': justify_games,
    'login': login,
    'one': one
}

# print(sys.argv)
# command = sys.argv[1]

# launch_map[command]()
# run_clients()
# justify_games()
