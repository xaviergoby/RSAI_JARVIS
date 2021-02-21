import PySimpleGUI as sg
import cv2



class VisionTestGUIHandler:

	def __init__(self):
		self.layout = [[sg.Text('OSRS_JARVIS Vision System V&V GUI', size=(40, 1), justification='center', font='Helvetica 20')],
			[sg.Image(filename='', key='screen_shot_image')],
			[sg.Text('Most Confident Detected Objects\n(ID, Centroid Coordinates)', size=(30, 3),
			         font=('Helvetica', 10), justification='center', key='obj_dect_info_key'),
			 sg.Listbox(values=[], size=(30, 3), key='detected_objects_info_list_key')],
			[sg.Text('Local Reference Frame Distance Vectors\n(dx, dy)', size=(30, 3), font=('Helvetica', 10),
			         justification='center', key='lrf_ds_vectors_key'),
			 sg.Listbox(values=[], size=(30, 3), key='lrf_ds_vectors_list_key')]]
		self.gui_window = sg.Window('OSRS_JARVIS Vision System Testing GUI', self.layout, location=(800, 400))

	def read(self):
		event, values = self.gui_window.read(timeout=0)
		return event, values

	def update_screen_cast(self, screen_shot_img):
		current_obj_dect_rgb_img_res = screen_shot_img
		current_obj_dect_rgb_img_res_bytes_format = cv2.imencode('.png', current_obj_dect_rgb_img_res)[1].tobytes()
		self.gui_window['screen_shot_image'].update(data=current_obj_dect_rgb_img_res_bytes_format)

	def update_objs_info(self, objs_info):
		self.gui_window['detected_objects_info_list_key'].update(objs_info)

	def update_objs_lrf_ds_vectors(self, objs_lrf_ds_vectors):
		self.gui_window['lrf_ds_vectors_list_key'].update(objs_lrf_ds_vectors)
