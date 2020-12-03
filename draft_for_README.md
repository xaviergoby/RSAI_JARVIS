# RuneScape - Artificial Intelligence (RSAI) Bot<a href="#rsai_proj_title_note" id="rsai_proj_title_note_ref"><sup>*</sup></a>

## Contents
1. [Goal](#goal)
2. [Old School RuneScape & RuneScape (3)](#osrs_vs_rs3)
3. [Notable Achievements & Facts](#facts_and_achievements)
4. [Autonomous Navigation Problem Potential Solutions & Key Topics](#auto_nav_prob_potential_sols)

## Goal <a name="goal"></a>
The development of an AI-based video game bot for the Massively Multiplayer Online Role-Playing Game (MMORPG) titled Old School RuneScape, the former redux version of RuneScape (AKA RuneScape 3), developed by the British video game studio, Jagex Limited.

## Old School RuneScape & RuneScape (3) <a name="osrs_vs_rs3"></a>

Old School RuneScape, originally named RuneScape, is an improved version of the backed up source code of the version of the game from August 2007. It was brought back on the 22nd of February, 2013, after having been temporally taken down so as to make way for RuneScaoe 3, the third and most recent iteration of the game, launched in July in 2013. Despite this latest HTML5-client based version of the game (RuneScape 3) possessing graphical effects and features far more advanced compared to that of Old School RuneScape, it is this earlier version of the game (OSRS) which happens hosts the largest base of players between the two versions<a href="#osrs_rs3_player_base" id="osrs_rs3_player_base_ref"><sup>1</sup></a>.


In-game screenshot, showing a player in combat with a goblin


![["In-game screenshot, showing a player in combat with a goblin"](https://en.wikipedia.org/wiki/Old_School_RuneScape)](assets/rs3_ui_img_resized_smaller.jpg "In-game screenshot")  ![["In-game screenshot, showing a player in combat with a goblin"](https://en.wikipedia.org/wiki/Old_School_RuneScape)](assets/Osrsinterface_resized_smaller.png "In-game screenshot")




### Notable Achievements & Facts <a name="facts_and_achievements+"></a>

- Guinness World Records award for the ["Most users of an MMO videogame"](https://www.guinnessworldrecords.com/world-records/105537-most-users-of-an-mmo-videogame) with a reported number of over 254,994,744 player accounts having been created since the game was first launched back in 2001.
- Guinness World Records award for the ["Most prolifically updated MMORPG videogame"](https://www.guinnessworldrecords.com/world-records/most-prolifically-updated-mmorpg) reportedly having been updated once a week on average for a total number of updates greater than 1,014 since the games initial launch.
- Guinness World Records award for the ["Greatest aggregate time playing an MMO or MMORPG videogame (all players)"](https://www.guinnessworldrecords.com/world-records/most-popular-free-mmorpg) for having a total aggregate number of minuets of player game time spent exceeding 443 billion, counting as of 27 July 2012.
- An anti-botting system, called "ClusterFlutterer", released in an update on the 25th of October, 2012, under the nickname of "Bot-Nuke", eventually 
lead to the banning of an estimated 98% of all botting accounts, equating approximately to 7.7 million million accounts being banned<a href="#bot_nuke" id="bot_nuke_ref"><sup>2</sup></a>.



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


### Current Capabilities Demonstrations

#### Environmental interaction using object detection 

 <figure class="video_container">
   <video controls="true" allowfullscreen="true" poster="path/to/poster_image.png">
     <source src="path/to/video.mp4" type="video/mvi">
     <source src="assets/RSAI_JARVIS_Media.avi" type="video/mvi">
   </video>
 </figure>




<br>
<br>
<br>
<br>
<br>
<br>
<br>


<a id="rsai_proj_title_note" href="#rsai_proj_title_note_ref"><sup>*</sup></a>More accurately, Old School RuneScape Artificial Intelligence, OSRS-AI, Bot
<br>
<a href="#osrs_rs3_player_base" id="osrs_rs3_player_base_ref"><sup>1</sup></a>[Old School RuneScape
 Official Wiki Webpage](https://oldschool.runescape.wiki/w/Old_School_RuneScape )
 <br>
<a id="bot_nuke" href="#bot_nuke_ref"><sup>2</sup></a>[Runescape bot nuking event bans 1.5 million bots in one day](https://www.pcgamer.com/runescape-bot-nuking-event-bans-1-5-million-bots-in-one-day/)
<br>



