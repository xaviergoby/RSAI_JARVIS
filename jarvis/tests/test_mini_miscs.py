import win32gui
from collections import namedtuple
import time


wndw_name = "Old School RuneScape"
print(f"Finding window titled '{wndw_name}'")
wndw_handle = win32gui.FindWindow(None, "Old School RuneScape")
print(f"Found window titled '{wndw_name}'")

# The RECT structure defines a rectangle by the coordinates of its upper-left and lower-right corners.
# left: Specifies the x-coordinate of the upper-left corner of the rectangle.
# top: Specifies the y-coordinate of the upper-left corner of the rectangle.
# right: Specifies the x-coordinate of the lower-right corner of the rectangle.
# bottom: Specifies the y-coordinate of the lower-right corner of the rectangle.
Rect = namedtuple('Rect', ('left', 'top', 'right', 'bottom'))
Size = namedtuple('Size', ('width', 'height'))

init_sleep_time = 5
loop_sleep_time = 3
print(f"\nStarting {init_sleep_time} seconds...")
while True:
	wndw_rect = win32gui.GetWindowRect(wndw_handle)
	cliet_rect = win32gui.GetClientRect(wndw_handle)
	print(f"Window")
	break



