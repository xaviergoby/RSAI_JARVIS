#!/usr/bin/env python
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from numpy.random import rand


class AnimatedPlot:

	def __init__(self):

		self.layout = [[sg.Text('Animated Matplotlib', size=(40, 1), justification='center', font='Helvetica 20')],
		          [sg.Canvas(size=(640, 480), key='-CANVAS-')],
		          [sg.Button('Exit', size=(10, 2), pad=((280, 0), 3), font='Helvetica 14')]]

		self.window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', self.layout, finalize=True)

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

# def draw_figure(canvas, figure):
# 	figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
# 	figure_canvas_agg.draw()
# 	figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
# 	return figure_canvas_agg


	def main(self):
		# define the form layout
		# layout = [[sg.Text('Animated Matplotlib', size=(40, 1), justification='center', font='Helvetica 20')],
		#           [sg.Canvas(size=(640, 480), key='-CANVAS-')],
		#           [sg.Button('Exit', size=(10, 2), pad=((280, 0), 3), font='Helvetica 14')]]

		# create the form and show it without the plot
		# window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', layout, finalize=True)

		# canvas_elem = window['-CANVAS-']
		# canvas = canvas_elem.TKCanvas
		# # draw the intitial scatter plot
		# fig, ax = plt.subplots()
		# ax.grid(True)
		# fig_agg = draw_figure(canvas, fig)

		# animated_plot_window = AnimatedPlot()

		while True:
			event, values = self.window.read(timeout=10)
			if event in ('Exit', None):
				exit(69)

			self.ax.cla()
			self.ax.grid(True)
			for color in ['red', 'green', 'blue']:
				n = 750
				x, y = rand(2, n)
				scale = 200.0 * rand(n)
				self.ax.scatter(x, y, c=color, s=scale, label=color, alpha=0.3, edgecolors='none')
			self.ax.legend()
			self.fig_agg.draw()
		self.window.close()


if __name__ == '__main__':
	animated_plot_window = AnimatedPlot()
	animated_plot_window.main()
