from jarvis.hobbes_bot.inventory import InventoryHandler








class Hobbes:

	def __init__(self, task_name, roi, confidence_threshold=0.1, max_detections=None):
		self.task_name = task_name
		self.roi = roi
		self.confidence_threshold = confidence_threshold
		self.max_detections = max_detections
		self.detections = None
		# self.tracker = CentroidTracker()
		self.mining = False
		self.currently_mining_mine_unique_id = None
		self.mines_mined = 0
		self.inv = InventoryHandler()
		# self.stop_watch = StopWatchTimer()
		self.tot_mined_mined = 0
		# self.sensor = ObjDectSensorSubSystem(self.roi)
		self.current_frame_detections_dict = None
		self.current_detections = None
		self.current_confident_detections = None
