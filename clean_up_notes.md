<ins>Testing Scripts Explained</ins>
- jarvis/tests/osrs_api_test.py: This script is used for testing the Old School Runescape API which allows you to fetch real-time market prices of items from the Grand Exchange.
- jarvis/tests/test_game_client_wndw.py: This script is used for testing the game client handler. The primary purpose of the `GameClient` class is to "take control" of the game client window in order to resize & reposition the game client window.
- jarvis/tests/test_slam.py: Does not seem to be working.  
- jarvis/tests/test_vision_sys.py:  
- jarvis/tests/test_vision_sys_GUI_version.py: This script is for testing the integration of following modules:
  - Object Detection & Tracking: `Vision` 
  - Game Client Handler, `GameClient`
  - GUI: `VisionTestGUIHandler` & `VisionSysHelperUtil`
  - Actuators (Mouse & Keyboard Clicks): `Mouse` & `HardwareEventsListener`
  - The actual agent/bot: `Hobbes`

---

## "Mundane" TO-DO Dev Notes

<ins>Files  **TO BE DELETED**</ins>

- [ ] README_backup.adoc
- [ ]  test_vision_sys_GUI_version.spec
- [ ]  draft_for_README.md
- [ ]  Handbook of Computer Vision Algorithms in Image Algebra.pdf

**INCOMPLETE**

<ins>Folders **TO BE DELETED**</ins>

- [ ] bot_sys_components
- [ ] build
- [ ] dist

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

