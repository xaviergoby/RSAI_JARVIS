import PySimpleGUI as sg
import cv2
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import rand


np.random.seed(19680801)



class VisionTestGUIHandler:

	def __init__(self):
		# self.NUM_DATAPOINTS = 500
		# self.NUM_DATAPOINTS_TO_PLOT = 9
		self.data_frame_size = (50, 50)

		self.layout = [
			[sg.Text('OSRS_JARVIS Vision System V&V GUI', size=(40, 1), justification='center', font='Helvetica 20')],
			[sg.Image(filename='', key='screen_shot_image'), sg.Canvas(size=(640, 480), key='-CANVAS-')],
			[sg.Text('Most Confident Detected Objects\n(ID, Centroid Coordinates)', size=(30, 3), font=('Helvetica', 10), justification='center', key='obj_dect_info_key'),sg.Text('Local Reference Frame Distance Vectors\n(dx, dy)', size=(30, 3), font=('Helvetica', 10),justification='center', key='lrf_ds_vectors_key')],
			[sg.Listbox(values=[], size=(30, 3), key='detected_objects_info_list_key'), sg.Listbox(values=[], size=(30, 3), key='lrf_ds_vectors_list_key')],
			# [sg.Text('Most Confident Detected Objects\n(ID, Centroid Coordinates)', size=(30, 3),font=('Helvetica', 10), justification='center', key='obj_dect_info_key'), sg.Listbox(values=[], size=(30, 3), key='detected_objects_info_list_key')],
			# [sg.Text('Local Reference Frame Distance Vectors\n(dx, dy)', size=(30, 3), font=('Helvetica', 10),justification='center', key='lrf_ds_vectors_key'), sg.Listbox(values=[], size=(30, 3), key='lrf_ds_vectors_list_key')],
			[sg.Text("Current Date & Time: "), sg.Text(size=(20, 1), key='-_time_-')]
		]

		self.window = sg.Window('OSRS_JARVIS Vision System Testing GUI', self.layout, location=(800, 400), finalize=True)

		self.canvas_elem = self.window['-CANVAS-']
		self.canvas = self.canvas_elem.TKCanvas
		self.fig, self.ax = plt.subplots()
		self.ax.grid(True)
		self.fig_agg = self.draw_figure(self.canvas, self.fig)

	def draw_figure(self, canvas, figure):
		figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
		figure_canvas_agg.draw()
		figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
		return figure_canvas_agg


	def read(self):
		event, values = self.window.read(timeout=0)  # WARNING! timeout=0 will chew up 100% of your CPU
		return event, values

	def update_screen_cast(self, screen_shot_img):
		current_obj_dect_rgb_img_res = screen_shot_img
		current_obj_dect_rgb_img_res_bytes_format = cv2.imencode('.png', current_obj_dect_rgb_img_res)[1].tobytes()
		self.window['screen_shot_image'].update(data=current_obj_dect_rgb_img_res_bytes_format)
		# self.gui_window['screen_shot_image2'].update(data=current_obj_dect_rgb_img_res_bytes_format)

	def update_objs_info(self, objs_info):
		self.window['detected_objects_info_list_key'].update(objs_info)

	def update_objs_lrf_ds_vectors(self, objs_lrf_ds_vectors):
		self.window['lrf_ds_vectors_list_key'].update(objs_lrf_ds_vectors)

	def update_current_time(self):
		self.window["-_time_-"].update(str(datetime.datetime.now()))

	def draw_plot_animation(self):
		self.ax.cla()
		self.ax.grid(True)
		for color in ['red', 'green', 'blue']:
			n = 750
			x, y = rand(2, n)
			scale = 200.0 * rand(n)
			self.ax.scatter(x, y, c=color, s=scale, label=color, alpha=0.3, edgecolors='none')
		self.ax.legend()
		# self.fig_agg.draw()
		self.fig_agg.draw_idle()

	# # matplotlib.use('TkAgg')
	# def draw_figure(self, loc=(0, 0)):
	# 	# figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
	# 	self.figure_canvas_agg.draw()
	# 	self.figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
	# 	# return self.figure_canvas_agg
	#
	# def show_img_fig(self):
	# 	data = np.random.random(self.data_frame_size)
	# 	# self.ax.cla() # clear the subplot
	# 	# self.ax.imshow(data) # draw the grid
	# 	self.ax.imshow(data)
	#
	# # def get_draw_figure(self):
	# 	# canvas_elem = self.gui_window.FindElement('-CANVAS-')
	# 	# canvas = canvas_elem.TKCanvas
	# 	# fig_agg = self.draw_figure(self.canvas, self.fig)
	#
	# def _clear(self):
	# 	for item in self.figure_canvas_agg.get_tk_widget().find_all():
	# 		self.figure_canvas_agg.get_tk_widget().delete(item)

	# def main(self):


if __name__ == "__main__":
	from jarvis.vision_sys.sensor import Sensor
	import time

	game_client_area_roi = (8, 31, 791, 591)
	screen_capture_opt = "mss"
	sensor = Sensor(roi=game_client_area_roi, mode=screen_capture_opt)
	# sensor.enable_manual_recording(True)

	gui_window = VisionTestGUIHandler()

	while True:
		bgr_frame = sensor.get_frame()  # frame.shape -> (560, 783)       //TODO###
		gui_window.read()

		rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
		gui_window.update_screen_cast(screen_shot_img=rgb_frame)
		gui_window.update_current_time()

		gui_window.draw_plot_animation()


# time.sleep(0.6)





















