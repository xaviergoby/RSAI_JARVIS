
import PySimpleGUI as sg





# vision_test_gui.py layout 02/04/2021
vision_test_gui_layout = [
	[sg.Text('OSRS_JARVIS Vision System V&V GUI', size=(40, 1), justification='center', font='Helvetica 20')],
	[sg.Image(filename='', key='screen_shot_image')],
	[sg.Text('Most Confident Detected Objects\n(ID, Centroid Coordinates)', size=(30, 3), font=('Helvetica', 10), justification='center', key='obj_dect_info_key'),
	 sg.Listbox(values=[], size=(30, 3), key='detected_objects_info_list_key')],
	[sg.Text('Local Reference Frame Distance Vectors\n(dx, dy)', size=(30, 3), font=('Helvetica', 10), justification='center', key='lrf_ds_vectors_key'),
	 sg.Listbox(values=[], size=(30, 3), key='lrf_ds_vectors_list_key')]]


# vision_test_gui_v3.py 02/04/2021
col1_layout = \
	[
	[sg.Text('OSRS_JARVIS Vision System V&V GUI', size=(30, 1), justification='center', font='Helvetica 20')],
    [sg.Image(size=(30, 10), filename='', key='screen_shot_image')],
    [sg.Text('Most Confident Detected Objects\n(ID, Centroid Coordinates)', size=(30, 3), font=('Helvetica', 10), justification='center', key='obj_dect_info_key'),
    sg.Text('Local Reference Frame Distance Vectors\n(dx, dy)', size=(30, 3), font=('Helvetica', 10), justification='center', key='lrf_ds_vectors_key')],
    [sg.Listbox(values=[], size=(30, 3), key='detected_objects_info_list_key'),
    sg.Listbox(values=[], size=(30, 3), key='lrf_ds_vectors_list_key')],
	# [sg.Text('Most Confident Detected Objects\n(ID, Centroid Coordinates)', size=(30, 3),font=('Helvetica', 10), justification='center', key='obj_dect_info_key'), sg.Listbox(values=[], size=(30, 3), key='detected_objects_info_list_key')],
	# [sg.Text('Local Reference Frame Distance Vectors\n(dx, dy)', size=(30, 3), font=('Helvetica', 10),justification='center', key='lrf_ds_vectors_key'), sg.Listbox(values=[], size=(30, 3), key='lrf_ds_vectors_list_key')],
    [sg.Text("Current Date & Time: "), sg.Text(size=(20, 1), key='-_time_-')]
	]
col1 = sg.Column(col1_layout, justification='center')
col2_layout = [[sg.Canvas(size=(40, 1), key='-CANVAS-')]]
col2 = sg.Column(col2_layout)
vision_test_gui_v3_layout = [[col1, col2], ]
