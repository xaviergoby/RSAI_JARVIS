import cv2


class VisionSysHelperUtil:

    def __init__(self, show=True, show_overlayed_info=True, print_state_info=True,
                 show_all_overlaid_text_info=True, show_obj_tracking_id=True,
                 show_obj_centroid_coords=True, show_overlaid_dect_obj_markers=True,
                 vertical_offset = 15, text_font_size = 0.5, text_font_thickness = 2,
                 text_colour=(0,0,0), bbox_c_pnt_colour = (0, 0, 0)):
        self.show = show
        self.show_overlayed_info = show_overlayed_info
        self.show_all_text_info = show_all_overlaid_text_info
        self.show_obj_tracking_id = show_obj_tracking_id
        self.show_obj_centroid_coords = show_obj_centroid_coords
        self.show_obj_marker = show_overlaid_dect_obj_markers
        self.vertical_offset = vertical_offset
        self.text_font_size = text_font_size
        self.text_font_thickness = text_font_thickness
        self.text_colour = text_colour
        self.bbox_c_pnt_colour = bbox_c_pnt_colour

    ########################## Obj Dect Output Frame Info Overlaying ##########################
    def set_dect_obj_info(self, img, tracking_id_i, centroid_i):
        """
        :param img:
        :param tracking_id_i:
        :param centroid_i:
        :return:
        """
        if self.show_all_text_info is True:
            if self.show_obj_tracking_id is True:
                obj_id_info = "Mine ID:{0}".format(tracking_id_i)
                cv2.putText(img, obj_id_info,
                            (centroid_i[0], centroid_i[1] + 0 * self.vertical_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, self.text_font_size, self.text_colour, self.text_font_thickness)

            if self.show_obj_centroid_coords is True:
                obj_frame_centroid_pos_info = "Obj Centroid:({0},{1})".format(centroid_i[0], centroid_i[1])
                cv2.putText(img, obj_frame_centroid_pos_info,
                            (centroid_i[0], centroid_i[1] + 1 * self.vertical_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, self.text_font_size, self.text_colour, self.text_font_thickness)

    def set_dect_obj_markers(self, img, centroid_i):
        """
        :param img:
        :param centroid_i:
        :return:
        """
        if self.show_obj_marker is True:
                cv2.circle(img, (centroid_i[0], centroid_i[1] + 0 * self.vertical_offset),
                           4, self.bbox_c_pnt_colour, -1)

    def overlay_obj_dect_state_info(self, img, objects_tracked_dict):
        """
        :param img:
        :param objects_tracked_dict:
        :return:
        """
        if self.show is True:
            for (tracking_id_i, centroid_i) in objects_tracked_dict.items():
                self.set_dect_obj_info(img, tracking_id_i, centroid_i)
                self.set_dect_obj_markers(img, centroid_i)

    ########################## Obj Dect State Info Printing ##########################
    def print_obj_dect_input_frame_info(self, obj_dect_input_frame):
        print("\n" + "⨂", "Object Detection Sys Input Frame Information:")
        frame_ic = int(obj_dect_input_frame.shape[0] // 2)
        frame_jc = int(obj_dect_input_frame.shape[1] // 2)
        print(f"Shape: {obj_dect_input_frame.shape}")
        print(f"Centroid coordinates (pxy, pxx)↔(row i, col j): {(frame_ic, frame_jc)}")
        # print("~" * 5)

    def print_obj_dect_output_frame_info(self, obj_dect_output_frame):
        print("\n" + "⨂", "Object Detection Sys Output Frame Information:")
        frame_ic = int(obj_dect_output_frame.shape[0] // 2)
        frame_jc = int(obj_dect_output_frame.shape[1] // 2)
        print(f"Shape: {obj_dect_output_frame.shape}\n")
        print(f"Centroid centroid (pxy, pxx)↔(row i, col j): {(frame_ic, frame_jc)}")
        # print("~" * 5)

    def print_tracked_lrf_centroid_ds_vectors(self, lrf_centroid_ds_vectors):
        print("\n" + "⨂", "Detected Objects Local Ref Frame Distance (or displacement?) Vectors:")
        print(f"{lrf_centroid_ds_vectors}")
        # print("~" * 5)

    def print_inline_dect_objs_tracked_info(self, objs_tracked_dict):
        tracker_ids, centroid_coords = objs_tracked_dict.items()
        print("\n" + "⨂", "Detected Objects Information:")
        print(f"- Tracker IDs: {tracker_ids}")
        print(f"- Screen Relative Centroid Pos. Coords (pxy, pxx)↔(row i, col j): {centroid_coords}")
        # print("~" * 5)

    def print_multiline_dect_objs_tracked_info(self, objs_tracked_dict):
        # def print_dect_objs_tracked_info(self, tracking_id_i, centroid_i):
        print("\n" + "⨂", "Detected Objects Tracker ID & Screen Relative Centroid Pos. Coords (pxy, pxx)↔(row i, col j):")
        for (tracking_id_i, centroid_i) in objs_tracked_dict.items():
            # obj_id_info = "Mine Tracker ID: {0}".format(tracking_id_i)
            # obj_frame_centroid_pos_info = "Mine Frame Relative Centroid Pos. Coords (pxx, pxy)↔(col j, row i): ({0}, {1})".format(centroid_i[0], centroid_i[1])
            # print(obj_id_info)
            # print(obj_frame_centroid_pos_info)
            obj_tracker_id_frame_centroid_coords_info = f"- ID: {tracking_id_i} \t&\tScreen Relative Centroid Coords: {(centroid_i[1], centroid_i[0])}"
            print(obj_tracker_id_frame_centroid_coords_info)
