# RuneScape - Artificial Intelligence (RSAI) Bot<a href="#rsai_proj_title_note" id="rsai_proj_title_note_ref"><sup>*</sup></a>

[comment]: <> (![slaying_cows_using_obj_dect]&#40;assets/RSAI_JARVIS_Media.gif&#41;)
## Contents

1. [Goal](#goal)<br>

2. [Old School RuneScape & RuneScape (3)](#osrs_vs_rs3)<br>

3. [Notable Achievements & Facts](#facts_and_achievements)<br>

4. [Current Capabilities Demonstrations](#current_capabilities)<br>

    4.1 [Environmental Interaction Using Object Detection](#env_interaction)<br>

    4.2 [Simulation Environment GUI Software](#sim_env_gui_sw)<br>

4. [Autonomous Navigation Problem Potential Solutions & Key Topics](#auto_nav_prob_potential_sols)<br>

## Goal <a name="goal"></a>

The development of an AI-based video game bot for the Massively Multiplayer Online Role-Playing Game (MMORPG) titled Old School RuneScape, the former redux version of RuneScape (AKA RuneScape 3), developed by the British video game studio, Jagex Limited.


## Old School RuneScape & RuneScape (3) <a name="osrs_vs_rs3"></a>

Old School RuneScape, originally named RuneScape, is an improved version of the backed up source code of the version of the game from August 2007. It was brought back on the 22nd of February, 2013, after having been temporally taken down so as to make way for RuneScaoe 3, the third and most recent iteration of the game, launched in July in 2013. Despite this latest HTML5-client based version of the game (RuneScape 3) possessing graphical effects and features far more advanced compared to that of Old School RuneScape, it is this earlier version of the game (OSRS) which happens hosts the largest base of players between the two versions<a href="#osrs_rs3_player_base" id="osrs_rs3_player_base_ref"><sup>1</sup></a>.


![RuneScape 3 vs Old School RuneScape comparison](assets/rs3_vs_osrs_comparison_images_combined.jpg "Hello World")*<br>In-game screenshot comparison of both games. RuneScape3 (left), showing a player carrying a longsword and standing amongst a bunch of NPC wizards, a typical scenario for an experienced player. Old School RuneScape (right), showing a new player in combat with a goblin, a standard activity every newly joined player goes through.*


### Notable Achievements & Facts <a name="facts_and_achievements+"></a>


- Guinness World Records award for the ["Most users of an MMO videogame"](https://www.guinnessworldrecords.com/world-records/105537-most-users-of-an-mmo-videogame) with a reported number of over 254,994,744 player accounts having been created since the game was first launched back in 2001.

- Guinness World Records award for the ["Most prolifically updated MMORPG videogame"](https://www.guinnessworldrecords.com/world-records/most-prolifically-updated-mmorpg) reportedly having been updated once a week on average for a total number of updates greater than 1,014 since the games initial launch.

- Guinness World Records award for the ["Greatest aggregate time playing an MMO or MMORPG videogame (all players)"](https://www.guinnessworldrecords.com/world-records/most-popular-free-mmorpg) for having a total aggregate number of minuets of player game time spent exceeding 443 billion, counting as of 27 July 2012.

- An anti-botting system, called "ClusterFlutterer", released in an update on the 25th of October, 2012, under the nickname of "Bot-Nuke", eventually 

lead to the banning of an estimated 98% of all botting accounts, equating approximately to 7.7 million million accounts being banned<a href="#bot_nuke" id="bot_nuke_ref"><sup>2</sup></a>.

---

### Current Capabilities Demonstrations <a name="current_capabilities"></a>

#### Environmental Interaction Using Object Detection <a name="env_interaction"></a>

Autonomous slaying of cows by the bot with the help of object detection. The TensorFlow pre-trained model which was used was ssd_mobilenet_v1_coco and it was trained on a dataset of images and PASCAL VOC format annotations, created using [LabelImg](https://github.com/tzutalin/labelImg).


![slaying_cows_using_obj_dect](assets/RSAI_JARVIS_Media.gif)*<br>Object detection based autonomous NPC slaying at the cow pen near the in-game city/town called Lumbridge*

<br>

![osrs_game_client_window_and_ui_components](assets/Edited_RSAI_Jarvis_Hobbes_Mining_Copy.gif)*<br>Object detection based autonomous resource gathering at the mines south of Lumbridge*

<br>

#### Simulation Environment GUI Software <a name="sim_env_gui_sw"></a>

An extensive still-in-development simulation GUI program developed for various purposes. Some of these are:

- Use of as a controllable & deterministic simulation environment.

- Implementation & testing of reinforcement learning algorithms.

- Assistive experimentation tool for autonomous navigation.

- Investigation of various planning & decision making algorithms.

- Validation & verification of implementations prior to integration with the system. 

A great and invaluable piece of contribution to project by [Victor Guillet](https://github.com/vguillet).


![slaying_cows_using_obj_dect](assets/RSAI_JARVIS_RL_GUI.gif)*<br>An extensive still-in-development simulation GUI program developped for various purposes. Is currently mainly being used for implementing and testing reinforcement learning algorithms as streamlined and conveniently as possible, in addition to being used as a helpful tool in the quest of solving the problem of autonomous navigation. Credits to [Victor Guillet](https://github.com/vguillet) for his invaluable contribution*

### OSRS Game Client Window & User-Interface Components


![osrs_game_client_window_and_ui_components](assets/OSRS_Game_Client_Window_and_User_Interface_Components.png)*<br>Object detection based autonomous NPC slaying at the cow pen near the in-game city/town called Lumbridge*

---

__## Autonomous Navigation Problem Potential Solutions & Key Topics<a name="auto_nav_prob_potential_sols"></a>

- Iterative Closest Point (ICP) algorithm

- End-to-end (E2E) Deep Learning (DL)

    - CNN2-LSTM Network

    - [SuperPoint](https://github.com/rpautrat/SuperPoint) network

    - Hierarchical Scene Coordinate network [(hscnet)](https://github.com/AaltoVision/hscnet) for coordinate classification (& regression?) for visual localisation

    - [Hierarchical Localisation](https://github.com/cvg/Hierarchical-Localization) network

- Extended Kalman Filter (EKF)

- Dead Reckoning

- Topological (visual) graphs & maps

- View graphs (& maps)

- Optical flow

- Key points

- Global & local feature descriptors

- Simultaneous Localisation And Mapping (SLAM)

    - Occupancy Grid SLAM

    - GraphSLAM

    - RGB-D SLAM



## Navigation & Simultaneous Localization And Mapping (SLAM)

### Place to Place Navigation (P2PNav)

Flow of steps:

- **Starting Place**: Set starting place (global) Main Map loc coordinates 

- **Along Path/Trajectory**: 

  - 1st) Convert A* generated (global) Main Map displacements to mini map (mm) screen pixel pos coords.

  - 2nd) Use generated mm screen pixel pos coords for Left Mouse Button actuator clicks. 

---

## Current Issues & Potential Solution Approaches

|        Modules       |                                                       Issues                                                       |                         Potential Solutions                        |
|:--------------------:|:------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------:|
| `Inventory` `Hobbes` | Determining the total number of items present in the inventory, regardless of whether items are known or unknown. | First start by counting all the items which are known and then.... |
|                      |                                                                                                                    |                                                                    |
|                      |                                                                                                                    |                                                                    |
|                      |                                                                                                                    |                                                                    |
<br>
<br>

---

## Testing, `jarvis/tests`, Scripts Explained

- `jarvis/tests/osrs_api_test.py`: This script is used for testing the Old School Runescape API which allows you to fetch
  real-time market prices of items from the Grand Exchange.
- `jarvis/tests/test_game_client_wndw.py`: This script is used for testing the game client handler. The primary purpose of
  the `GameClient` class is to "take control" of the game client window in order to resize & reposition the game client
  window.
- `jarvis/tests/test_slam.py`: Does not seem to be working.
- `jarvis/tests/test_vision_sys.py`: 
- `jarvis/tests/test_vision_sys_GUI_version.py`: This script is for testing the integration of following modules:
  - Object Detection & Tracking: `Vision`
  - Game Client Handler, `GameClient`
  - GUI: `VisionTestGUIHandler` & `VisionSysHelperUtil`
  - Actuators (Mouse & Keyboard Clicks): `Mouse` & `HardwareEventsListener`
  - The actual agent/bot: `Hobbes`

## Util, `jarvis/utils`, Scripts Explained
- `jarvis/utils/vision_sys_helper_util.py`: The `VisionSysHelperUtil` class in this script is a helpful 
utility for the `Vision` & `VisionTestGUIHandler`  modules. Its utilisation purpose is the annotation of infomartion and drawing of "symbols" on the captured screen shots which are displayed in the GUI. All "settings" of this class are `True` by default!
  ![](assets/vision_sys_helper_util_VisionSysHelperUtil_demo_with_and without_all_annots.jpg)*<br>`VisionTestGUIHandler` class with (left) all default/True settings and (right) with every thing "switched" off. Note that the script in use (being annotated in the bottom right) is `jarvis/tests/test_vision_sys_GUI_version.py` script.*
  

---
  
## "Mundane" TO-DO Dev Notes

<ins>Script Documentation  **TO BE ADDED**</ins>

- [ ] `jarvis/tests/test_vision_sys_GUI_version.py`

<ins>Files  **TO BE DELETED**</ins>

- [X]  README_backup.adoc
- [X]  test_vision_sys_GUI_version.spec
- [X]  draft_for_README.md
- [X]  Handbook of Computer Vision Algorithms in Image Algebra.pdf

**INCOMPLETE**

<ins>Folders **TO BE DELETED**</ins>

- [X] bot_sys_components
- [X] build
- [X] dist

**INCOMPLETE**

<ins>JARVIS Folders & Files In Use [X] & Not In Use [_]</ins>

- [ ] jarvis/actuator_sys/actuator.py
- [X] jarvis/actuator_sys/mouse.py
- [X] jarvis/game_client/game_client.py
- [ ] jarvis/hobbes_bot/basic_self_contained_bot_cls.py
- [X] jarvis/hobbes_bot/hobbes.py
- [X] jarvis/hobbes_bot/inventory.py
- [ ] jarvis/hobbes_bot/navigation.py
- [ ] jarvis/hobbes_bot/skills.py
- [ ] jarvis/jarvis_core/agent.py
- [ ] jarvis/jarvis_core/environment.py

**INCOMPLETE**

---

## Acronyms, Abreviations & Terms Used

- "def": "default"
- "w/": "with"
- "w/o": "without"
- "b/c": "because"
- "args": "arguments"
- "params": "parameters"
- "OSRS": "Old School RuneScape"
- "RS3": "RuneScape 3"
- "vis" or "viz: "Vision"
- "h/w": "hardware"
- "pos": "position"
- "coords": "coordinates"
- "dim(s)": "dimension(s)"
- "obj": "object"
- "dect" (yes, dect): "detection"
- "wndw": "window"
- "num": "number"
- "req": "required"
- "V&V" or "VV": "Verification & Validation"



**INCOMPLETE**


---

<a id="rsai_proj_title_note" href="#rsai_proj_title_note_ref"><sup>*</sup></a>More accurately, Old School RuneScape Artificial Intelligence, OSRS-AI, Bot

<a href="#osrs_rs3_player_base" id="osrs_rs3_player_base_ref"><sup>1</sup></a>[Old School RuneScape Official Wiki Webpage](https://oldschool.runescape.wiki/w/Old_School_RuneScape )


<a id="bot_nuke" href="#bot_nuke_ref"><sup>2</sup></a>[Runescape bot nuking event bans 1.5 million bots in one day](https://www.pcgamer.com/runescape-bot-nuking-event-bans-1-5-million-bots-in-one-day/)

<br>



