from csv import writer


def append_list_as_row(file_name, list_of_elem):
	# Open file in append mode
	with open(file_name, 'a+', newline='') as write_obj:
		# Create a writer object from csv module
		csv_writer = writer(write_obj, delimiter=",")
		# Add contents of list as last row in the csv file
		for row in [list_of_elem]:
			csv_writer.writerow(row)