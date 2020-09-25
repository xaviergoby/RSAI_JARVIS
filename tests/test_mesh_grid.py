from research_and_dev.end2end_nav.handlers import nav_grid_handler
import settings




if __name__ == "__main__":
	# Recall: MESH_GRID_OPTIONS = {1:{"x_grid_pnts":(150, 650, 11), "y_grid_pnts":(60, 560, 11)}}
	# lmc_x = 500
	# lmc_y = 360
	# lmc_x = 428
	# lmc_y = 326
	# lmc_x = 210
	# lmc_y = 370
	# lmc_x = 420
	lmc_x = 392
	# lmc_y = 240
	lmc_y = 212
	mgrid = nav_grid_handler.NavigationGridHandler(settings.MESH_GRID_OPTIONS[1])
	print(f"mgrid.px_x_axes_pnts: {mgrid.px_x_axes_pnts}")
	print(f"mgrid.px_y_axes_pnts: {mgrid.px_y_axes_pnts}")

	ego_cent_rf_grid_x_axes_pnts = mgrid.ego_cent_rf_grid_x_axes_pnts
	ego_cent_rf_grid_y_axes_pnts = mgrid.ego_cent_rf_grid_y_axes_pnts

	print(f"ego_cent_rf_grid_x_axes_pnts: {ego_cent_rf_grid_x_axes_pnts}")
	print(f"ego_cent_rf_grid_y_axes_pnts: {ego_cent_rf_grid_y_axes_pnts}")

	nn_scrn_px_grid_pnt_px_coords = mgrid.get_lmc_nn_grid_pnt_px_coords(lmc_x, lmc_y)
	nn_grid_pnt_x = nn_scrn_px_grid_pnt_px_coords[0]
	nn_grid_pnt_y = nn_scrn_px_grid_pnt_px_coords[1]
	get_nn_scrn_px_grid_pnt_coords = mgrid.get_lmc_nn_grid_pnt_idxs(lmc_x, lmc_y)

	print(f"nn_scrn_px_grid_pnt_px_coords(500, 360): {nn_scrn_px_grid_pnt_px_coords}")
	print(f"get_nn_scrn_px_grid_pnt_coords(500, 360): {get_nn_scrn_px_grid_pnt_coords}")

	y_label = get_nn_scrn_px_grid_pnt_coords[0]
	x_label = get_nn_scrn_px_grid_pnt_coords[1]

	print(f"x_label: {x_label}")
	print(f"y_label: {y_label}")

	print(f"ego_cent_rf_grid_x_axes_pnts[x_label]: {ego_cent_rf_grid_x_axes_pnts[x_label]}")
	print(f"ego_cent_rf_grid_y_axes_pnts[y_label]: {ego_cent_rf_grid_y_axes_pnts[y_label]}")

	print(f"mgrid.px_x_axes_pnts[x_label]: {mgrid.px_x_axes_pnts[x_label]}")
	print(f"mgrid.px_y_axes_pnts[y_label]: {mgrid.px_y_axes_pnts[y_label]}")
	
	print("Resulting nn grid pnt (x, y): {0}".format(mgrid.get_lmc_nn_grid_pnt(lmc_x, lmc_y)))


	# Plot Viz
	import matplotlib.pyplot as plt
	# mgrid.px_x_axes_pnts[len(mgrid.px_x_axes_pnts) // 2]
	
	def plot_local_grid_map():
		fig = plt.figure()
		ax = fig.add_subplot(111, label="1")
		grid_pnt_x_centre = mgrid.px_x_axes_pnts[len(mgrid.px_x_axes_pnts) // 2]
		grid_pnt_y_centre = mgrid.px_y_axes_pnts[len(mgrid.px_y_axes_pnts) // 2]
		ax.plot(grid_pnt_x_centre, grid_pnt_y_centre, marker='o', color='k', linestyle='none',
		        label="Grid centre: ({0},{1}) or ({2},{3})".format(grid_pnt_x_centre, grid_pnt_y_centre,
		                                                           ego_cent_rf_grid_x_axes_pnts[len(mgrid.ego_cent_rf_grid_x_axes_pnts) // 2],
		                                                           ego_cent_rf_grid_y_axes_pnts[len(ego_cent_rf_grid_y_axes_pnts) // 2]))
		ax.plot(mgrid.mesh_grid_px_x_pnts, mgrid.mesh_grid_px_y_pnts, marker='.', color='k', linestyle='none')
		ax.plot(lmc_x, lmc_y, "ro",
		        label="True on-screen mouse click point loc: ({0},{1})".format(lmc_x, lmc_y))
		ax.plot(nn_grid_pnt_x, nn_grid_pnt_y, "go",
		        label="Nearest-neighbour mesh grid mouse click point loc: ({0},{1})".format(nn_grid_pnt_x, nn_grid_pnt_y))
		# plt.legend()
		ax.legend(bbox_to_anchor=(0, 1.3), loc='upper left', borderaxespad=0.)
		ax.set_xticks(mgrid.px_x_axes_pnts, minor=False)
		ax.set_yticks(mgrid.px_y_axes_pnts, minor=False)
		ax.set_xlim(150, 650)
		ax.set_ylim(60, 560)
		ax2_xax, ax3_yax = ax.twiny(), ax.twinx()
		ax2_xax.set_xticks(ego_cent_rf_grid_x_axes_pnts, minor=False)
		ax3_yax.set_yticks(ego_cent_rf_grid_y_axes_pnts, minor=False)
		# ax3_yax.invert_yaxis()
		# ax2_xax.plot(0, 0)
		ax.invert_yaxis()
		ax.grid(True)
		plt.show()
		
		pass
	
	
	fig = plt.figure()
	ax = fig.add_subplot(111, label="1")
	grid_pnt_x_centre = mgrid.px_x_axes_pnts[len(mgrid.px_x_axes_pnts) // 2]
	grid_pnt_y_centre = mgrid.px_y_axes_pnts[len(mgrid.px_y_axes_pnts) // 2]
	ax.plot(grid_pnt_x_centre, grid_pnt_y_centre, marker='o', color='k', linestyle='none',
	        label="Grid centre: ({0},{1}) or ({2},{3})".format(grid_pnt_x_centre, grid_pnt_y_centre,
	                                                                 ego_cent_rf_grid_x_axes_pnts[len(mgrid.ego_cent_rf_grid_x_axes_pnts) // 2],
	                                                                 ego_cent_rf_grid_y_axes_pnts[len(ego_cent_rf_grid_y_axes_pnts) // 2]))
	ax.plot(mgrid.mesh_grid_px_x_pnts, mgrid.mesh_grid_px_y_pnts, marker='.', color='k', linestyle='none')
	ax.plot(lmc_x, lmc_y, "ro",
	        label="True on-screen mouse click point loc: ({0},{1})".format(lmc_x, lmc_y))
	ax.plot(nn_grid_pnt_x, nn_grid_pnt_y, "go",
	         label="Nearest-neighbour mesh grid mouse click point loc: ({0},{1})".format(nn_grid_pnt_x, nn_grid_pnt_y))
	# plt.legend()
	ax.legend(bbox_to_anchor=(0, 1.3), loc='upper left', borderaxespad=0.)
	ax.set_xticks(mgrid.px_x_axes_pnts, minor=False)
	ax.set_yticks(mgrid.px_y_axes_pnts, minor=False)
	ax.set_xlim(150, 650)
	ax.set_ylim(60, 560)
	ax2_xax, ax3_yax = ax.twiny(), ax.twinx()
	ax2_xax.set_xticks(ego_cent_rf_grid_x_axes_pnts, minor=False)
	ax3_yax.set_yticks(ego_cent_rf_grid_y_axes_pnts, minor=False)
	# ax3_yax.invert_yaxis()
	# ax2_xax.plot(0, 0)
	ax.invert_yaxis()
	ax.grid(True)
	plt.show()



