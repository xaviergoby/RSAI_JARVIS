# NOTE:
# THIS SCRIPT IS THE EXACT SAME ONE AS LOCATED AT:
# src\ui_automation_tools\mouse_events_monitoring.py

import win32api
import win32api as wapi
import pyautogui
from settings import *

chars = "ABCDEFGHIJKLMNOPQRSTWXYZ 123456789,.'£$/\\"
keyList = ["\b"]
for char in "ABDPQSTW123 ":
    keyList.append(char)


def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys


def get_mouse_state():
    coords = pyautogui.position()
    state_left = win32api.GetKeyState(0x01)
    state = [coords, state_left]

    return state


def get_init_mouse_states(nVirtKey_dict, set_key_states=None):
    """
    This function is responsible for getting/setting the initial key state for
    each hexedecimal value in mouse_nVirtKey_dict
    :param nVirtKey_dict: i.e. mouse_nVirtKey_dict = {"LMB":0x01, "RMB":0x02}
    :return: {"LMB":win32api.GetKeyState(0x01), "RMB":win32api.GetKeyState(0x02)}
    """
    init_states_nVirtKey_dict = {}
    for key_state, hex in nVirtKey_dict.items():
        init_states_nVirtKey_dict[key_state] = win32api.GetKeyState(hex)
    return init_states_nVirtKey_dict


def get_mouse_click_event(init_mouse_state, nVirtKey):
    """
    NOTE: This function disregards both the pressed and unpressed states,
    (-128, -127), of both the LMB and RMB. This involves ignoring the
    pressed/unpressed state change values of -128 and -127.

    This function solely checks to see if a click(ed) (state) event has occured
    for either the LMB or RMB. This involves determining when the state of either
    the LMB or RMB change from having a state value of either 0 or 1 to instead having
    a state value of either 1 or 0.
    :param init_mouse_state: the initial key state of LMB or RMB. Can only either be 1 or 0
    :param nVirtKey: the hexedecimal of the virtual key code. lmb:0x01 and RMB:0x02
    :return:
    """
    # coords = pyautogui.position()
    current_mouse_state = win32api.GetKeyState(nVirtKey)
    if init_mouse_state != current_mouse_state:
        if current_mouse_state not in [-128, -127]:
            new_init_mouse_state = current_mouse_state
            return new_init_mouse_state
        elif current_mouse_state in [-128, -127]:
            return False
    elif init_mouse_state == current_mouse_state:
        return False


def get_mouse_click_events(init_states_nVirtKey_dict, nVirtKey_dict):
    """
    :param init_states_nVirtKey_dict:
    :return: e.g. {"LMB":False, "RMB":0}
    """
    mouse_click_events_dict = {}
    for key_state, init_key_state in init_states_nVirtKey_dict.items():
        nVirtKey = nVirtKey_dict[key_state]
        click_event = get_mouse_click_event(init_key_state, nVirtKey)
        mouse_click_events_dict[key_state] = click_event
    return mouse_click_events_dict


def mouse_button_clicked(mouse_click_events, mouse_btns=None):
    """
    :param mouse_click_events: a dict contaning key-value pairs of
    mouse button name - True or False.
    This function is only capable of checking if one mouse button was
    clicked.
    :param mouse_btns: a list containing the names of the mouse buttons
    which are the only be checked
    :return: a True or False statement
    """
    clicked = False
    if mouse_btns is not None:
        for mouse_btn_name in mouse_btns:
            if mouse_click_events[mouse_btn_name] is not False:
                clicked = True
                return clicked
            else:
                pass
        return clicked
    elif mouse_btns is None:
        for mouse_btn_name in list(mouse_nVirtKey_dict.keys()):
            if mouse_click_events[mouse_btn_name] is not False:
                clicked = True
                return clicked
            else:
                pass
        return clicked


def update_mouse_states(init_key_states, mouse_click_events):
    updated_init_key_states = init_key_states
    for key_state, changed_state in mouse_click_events.items():
        if changed_state is not False:
            updated_init_key_states[key_state] = changed_state
        else:
            pass
    return updated_init_key_states


def get_mouse_button_clicked_str(mouse_click_events):
    for mouse_btn_name in list(mouse_nVirtKey_dict.keys()):
        if mouse_click_events[mouse_btn_name] is not False:
            return mouse_btn_name
        else:
            pass
