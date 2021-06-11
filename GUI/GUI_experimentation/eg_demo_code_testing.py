import PySimpleGUI as sg
import datetime

sg.theme('Dark Blue 3')  # please make your windows colorful

layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(12, 1), key='-OUTPUT-')],
          [sg.Input(key='-IN-')],
          [sg.Button('Show'), sg.Button('Exit'), sg.Text(size=(20, 1), key='-_time_-')]]

window = sg.Window('Window Title', layout)


def getTime():
	return datetime.datetime.now().strftime('%H:%M:%S')

while True:  # Event Loop
	# event, values = window.read()
	event, values = window.read(timeout=0)
	# print(event, values)
	# window['-_time_-'].update(str(datetime.datetime.now()))
	if event == sg.WIN_CLOSED or event == 'Exit':
		break
	if event == 'Show':
		# change the "output" element to be the value of "input" element
		window['-OUTPUT-'].update(values['-IN-'])


	window["-_time_-"].update(str(datetime.datetime.now()))
	# window.FindElement('-_time_-').update(str(datetime.datetime.now()))

	# window.FindElement('-_time_-').Update(getTime())

window.close()
