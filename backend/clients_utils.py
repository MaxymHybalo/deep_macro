import os
import sys
import time

from win32 import win32gui as api
from win32.lib import win32con as con
from win32api import GetSystemMetrics

from utils.deep_utils import get_active_windows, get_window_coord
from processes.click import Click

path = 'D:\Games\RappelzSpace'
launcher = 'Launcher.exe'
launcher_name = 'Launcher'
game = 'Rappelz'

desktop = (GetSystemMetrics(0), GetSystemMetrics(1))
print('Desktop:', desktop)

def run_clients():
    os.chdir(path)
    for _ in range(3):
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
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        api.SetForegroundWindow(g)
        time.sleep(0.1)
        coord = get_window_coord(g)
        grid = fill_games_grid(coord)
        x, y = grid[i]
        _, _, w, h = coord
        api.SetWindowPos(g, con.HWND_TOP, x, y, w, h, 0)
        
launch_map = {
    'run': run_clients,
    'justify': justify_games
}

print(sys.argv)
command = sys.argv[1]

launch_map[command]()
# run_clients()
# justify_games()
