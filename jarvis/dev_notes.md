





### To-Do's
- [ ] Write a (cls) method in `Vision` class loc. @ jarvis/vision_sys/vision_cls.py which which implements the following:


```PYTHON
frame = vision.sensor.get_frame() # frame.shape -> (560, 783)
current_detections = vision.detector.get_current_frame_detections(frame) # apparently I had removed this line in favour of the below, on 13/11/2020
confident_boxes_norm_coords, confident_boxes_scores, confident_boxes_classes = vision.detector.confident_detections(
	current_detections)
```


