#!/usr/bin/env python
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import datetime
from numpy.random import rand
import cv2
from jarvis.vision_sys.sensor import Sensor
import numpy as np
# from GUI.GUI_experimentation.PySimpleGUI_layouts import vision_test_gui_v3_layout



class VisionTestGUIHandler:

	def __init__(self):
		self.world_map_array = np.load("world_array.npy")
		self.data_frame_size = (50, 50)

		self.col1_layout = [
			[sg.Text('OSRS_JARVIS Vision System V&V GUI', size=(30, 1), justification='center', font='Helvetica 20')],
			[sg.Image(size=(30, 10), filename='', key='screen_shot_image')],
			[sg.Text('Most Confident Detected Objects\n(ID, Centroid Coordinates)', size=(30, 3),
			         font=('Helvetica', 10), justification='center', key='obj_dect_info_key'),
			 sg.Text('Local Reference Frame Distance Vectors\n(dx, dy)', size=(30, 3), font=('Helvetica', 10),
			         justification='center', key='lrf_ds_vectors_key')],
			[sg.Listbox(values=[], size=(30, 3), key='detected_objects_info_list_key'),
			 sg.Listbox(values=[], size=(30, 3), key='lrf_ds_vectors_list_key')],
			# [sg.Text('Most Confident Detected Objects\n(ID, Centroid Coordinates)', size=(30, 3),font=('Helvetica', 10), justification='center', key='obj_dect_info_key'), sg.Listbox(values=[], size=(30, 3), key='detected_objects_info_list_key')],
			# [sg.Text('Local Reference Frame Distance Vectors\n(dx, dy)', size=(30, 3), font=('Helvetica', 10),justification='center', key='lrf_ds_vectors_key'), sg.Listbox(values=[], size=(30, 3), key='lrf_ds_vectors_list_key')],
			[sg.Text("Current Date & Time: "), sg.Text(size=(20, 1), key='-_time_-')]
		]
		self.col1 = sg.Column(self.col1_layout, justification='center')

		self.col2_layout = [[sg.Canvas(size=(40, 1), key='-CANVAS-')]]
		self.col2 = sg.Column(self.col2_layout)

		self.layout = [[self.col1, self.col2], ]

		# self.gui_window = sg.Window('OSRS_JARVIS Vision System Testing GUI', self.layout, location=(800, 400))
		self.window = sg.Window('OSRS_JARVIS Vision System Testing GUI', self.layout, location=(800, 400), finalize=True)

		self.canvas_elem = self.window['-CANVAS-']

		self.canvas = self.canvas_elem.TKCanvas
		self.fig = plt.figure(figsize=(4, 8), frameon=False)
		self.ax = plt.Axes(self.fig, [0., 0., 1., 1.])
		self.fig.add_axes(self.ax)
		self.fig_agg = self.draw_figure(self.canvas, self.fig)

		game_client_area_roi = (8, 31, 791, 591)
		screen_capture_opt = "mss"
		self.sensor = Sensor(roi=game_client_area_roi, mode=screen_capture_opt)

	def draw_figure(self, canvas, figure):
		figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
		figure_canvas_agg.draw()
		figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
		return figure_canvas_agg

	def read(self):
		# event, values = self.gui_window.read(timeout=0)
		event, values = self.window.read(timeout=0)  # WARNING! timeout=0 will chew up 100% of your CPU
		return event, values

	def update_objs_info(self, objs_info):
		self.window['detected_objects_info_list_key'].update(objs_info)

	def update_objs_lrf_ds_vectors(self, objs_lrf_ds_vectors):
		self.window['lrf_ds_vectors_list_key'].update(objs_lrf_ds_vectors)


	def main(self):
		self.read()
		bgr_frame = self.sensor.get_frame()  # frame.shape -> (560, 783)       //TODO###
		screen_shot_img = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
		current_obj_dect_rgb_img_res = screen_shot_img
		current_obj_dect_rgb_img_res_bytes_format = cv2.imencode('.png', current_obj_dect_rgb_img_res)[1].tobytes()
		self.window['screen_shot_image'].update(data=current_obj_dect_rgb_img_res_bytes_format)
		# self.window['detected_objects_info_list_key'].update(objs_info)
		# self.window['lrf_ds_vectors_list_key'].update(objs_lrf_ds_vectors)
		self.window["-_time_-"].update(str(datetime.datetime.now()))

		self.ax.cla()
		data = np.random.random(self.data_frame_size)
		self.ax.imshow(self.world_map_array, interpolation='nearest', aspect='auto')
		self.ax.set_axis_off()
		self.fig_agg.draw()

	def update_screen_cast(self, screen_shot_img):
		current_obj_dect_rgb_img_res = screen_shot_img
		current_obj_dect_rgb_img_res_bytes_format = cv2.imencode('.png', current_obj_dect_rgb_img_res)[1].tobytes()
		self.window['screen_shot_image'].update(data=current_obj_dect_rgb_img_res_bytes_format)
	# 	self.gui_window['screen_shot_image'].update(data=current_obj_dect_rgb_img_res_bytes_format)



if __name__ == "__main__":
	vis_gui_test = VisionTestGUIHandler()
	while True:
		vis_gui_test.main()


	# from jarvis.vision_sys.sensor import Sensor
	# import time
	#
	# game_client_area_roi = (8, 31, 791, 591)
	# screen_capture_opt = "mss"
	# sensor = Sensor(roi=game_client_area_roi, mode=screen_capture_opt)
	# sensor.enable_manual_recording(True)
	#
	# gui_window = VisionTestGUIHandler()

	# while True:
	# 	bgr_frame = sensor.get_frame()  # frame.shape -> (560, 783)       //TODO###
	# 	gui_window.read()
	#
	# 	rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
	# 	gui_window.update_screen_cast(screen_shot_img=rgb_frame)
	# 	time.sleep(0.6)




















