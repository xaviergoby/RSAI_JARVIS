# RuneScape - Artificial Intelligence (RSAI) Bot<a href="#rsai_proj_title_note" id="rsai_proj_title_note_ref"><sup>*</sup></a>

## Contents
1. [Goal](#goal)<br>
2. [Old School RuneScape & RuneScape (3)](#osrs_vs_rs3)<br>
3. [Notable Achievements & Facts](#facts_and_achievements)<br>
4. [Current Capabilities Demonstrations](#current_capabilities)<br>
    4.1) [Environmental Interaction Using Object Detection](#env_interaction)<br>
    4.2) [Simulation Environment GUI Software](#sim_env_gui_sw)<br>
4. [Autonomous Navigation Problem Potential Solutions & Key Topics](#auto_nav_prob_potential_sols)<br>

## Goal <a name="goal"></a>

The development of an AI-based video game bot for the Massively Multiplayer Online Role-Playing Game (MMORPG) titled Old School RuneScape, the former redux version of RuneScape (AKA RuneScape 3), developed by the British video game studio, Jagex Limited.

<br>

## Old School RuneScape & RuneScape (3) <a name="osrs_vs_rs3"></a>

Old School RuneScape, originally named RuneScape, is an improved version of the backed up source code of the version of the game from August 2007. It was brought back on the 22nd of February, 2013, after having been temporally taken down so as to make way for RuneScaoe 3, the third and most recent iteration of the game, launched in July in 2013. Despite this latest HTML5-client based version of the game (RuneScape 3) possessing graphical effects and features far more advanced compared to that of Old School RuneScape, it is this earlier version of the game (OSRS) which happens hosts the largest base of players between the two versions<a href="#osrs_rs3_player_base" id="osrs_rs3_player_base_ref"><sup>1</sup></a>.

<br>

![RuneScape 3 vs Old School RuneScape comparison](assets/rs3_vs_osrs_comparison_images_combined.jpg "Hello World")*<br>In-game screenshot comparison of both games. RuneScape3 (left), showing a player carrying a longsword and standing amongst a bunch of NPC wizards, a typical scenario for an experienced player. Old School RuneScape (right), showing a new player in combat with a goblin, a standard activity every newly joined player goes through.*

<br>

### Notable Achievements & Facts <a name="facts_and_achievements+"></a>


- Guinness World Records award for the ["Most users of an MMO videogame"](https://www.guinnessworldrecords.com/world-records/105537-most-users-of-an-mmo-videogame) with a reported number of over 254,994,744 player accounts having been created since the game was first launched back in 2001.
- Guinness World Records award for the ["Most prolifically updated MMORPG videogame"](https://www.guinnessworldrecords.com/world-records/most-prolifically-updated-mmorpg) reportedly having been updated once a week on average for a total number of updates greater than 1,014 since the games initial launch.
- Guinness World Records award for the ["Greatest aggregate time playing an MMO or MMORPG videogame (all players)"](https://www.guinnessworldrecords.com/world-records/most-popular-free-mmorpg) for having a total aggregate number of minuets of player game time spent exceeding 443 billion, counting as of 27 July 2012.
- An anti-botting system, called "ClusterFlutterer", released in an update on the 25th of October, 2012, under the nickname of "Bot-Nuke", eventually 
lead to the banning of an estimated 98% of all botting accounts, equating approximately to 7.7 million million accounts being banned<a href="#bot_nuke" id="bot_nuke_ref"><sup>2</sup></a>.

<br>

### Current Capabilities Demonstrations <a name="current_capabilities"></a>

#### Environmental Interaction Using Object Detection <a name="env_interaction"></a>

Autonomous slaying of cows by the bot with the help of object detection. The TensorFlow pre-trained model which was used was ssd_mobilenet_v1_coco and it was trained on a dataset of images and PASCAL VOC format annotations, created using [LabelImg](https://github.com/tzutalin/labelImg).

<br>

![slaying_cows_using_obj_dect](assets/RSAI_JARVIS_Media.gif)*<br>Object detection based autonomous NPC slaying at the cow pen near the in-game city/town called Lumbridge*

<br>

#### Simulation Environment GUI Software <a name="sim_env_gui_sw"></a>

An extensive still-in-development simulation GUI program developed for various purposes. Some of these are:

- Use of as a controllable & deterministic simulation environment.
- Implementation & testing of reinforcement learning algorithms.
- Assistive experimentation tool for autonomous navigation.
- Investigation of various planning & decision making algorithms.
- Validation & verification of implementations prior to integration with the system. 

A great and invaluable piece of contribution to project by [Victor Guillet](https://github.com/vguillet).

<br>

![slaying_cows_using_obj_dect](assets/RSAI_JARVIS_RL_GUI.gif)*<br>An extensive still-in-development simulation GUI program developped for various purposes. Is currently mainly being used for implementing and testing reinforcement learning algorithms as streamlined and conveniently as possible, in addition to being used as a helpful tool in the quest of solving the problem of autonomous navigation. Credits to [Victor Guillet](https://github.com/vguillet) for his invaluable contribution*

<br>

### Autonomous Navigation Problem Potential Solutions & Key Topics<a name="auto_nav_prob_potential_sols"></a>

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







<br>
<br>
<br>
<br>
<br>
<br>
<br>

---

<a id="rsai_proj_title_note" href="#rsai_proj_title_note_ref"><sup>*</sup></a>More accurately, Old School RuneScape Artificial Intelligence, OSRS-AI, Bot
<br>
<a href="#osrs_rs3_player_base" id="osrs_rs3_player_base_ref"><sup>1</sup></a>[Old School RuneScape
 Official Wiki Webpage](https://oldschool.runescape.wiki/w/Old_School_RuneScape )
 <br>
<a id="bot_nuke" href="#bot_nuke_ref"><sup>2</sup></a>[Runescape bot nuking event bans 1.5 million bots in one day](https://www.pcgamer.com/runescape-bot-nuking-event-bans-1-5-million-bots-in-one-day/)
<br>



