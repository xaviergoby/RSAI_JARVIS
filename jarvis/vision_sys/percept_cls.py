





class Perept:

	def __init__(self, frame: "np array w/ shape (h, w, c)"=None, dects=None, __confident_dects=None):
		"""
		:param frame: np array w/ shape (h, w, c)
		:param dects: a dict with the 5 keys ("norm_boxes", "obj_scores", "classes", "num_detections", "inf_res_img") where:
		type(norm_boxes) -> array & norm_boxes.shape -> (max_detections, 4)
		type(obj_scores) -> array & obj_scores.shape -> (max_detections, )
		type(classes) -> array & classes.shape -> (max_detections, )
		num_detections??
		type(inf_res_img) -> array & inf_res_img.shape -> (560, 783, 3) when wndw set using def (0, 0, 800, 600) opt
		:param __confident_dects: a 3-tuple (confident boxes normed coords, confident boxes scores, confident boxes classes)
		having types (<class 'numpy.ndarray'>, <class 'numpy.ndarray'>, <class 'numpy.ndarray'>)
		"""
		self.__frame = frame # vision.sensor.get_frame()
		self.__dects = dects # vision.detector.get_current_frame_detections(frame)
		self.__confident_dects = __confident_dects


