import numpy as np
import itertools
from research_and_dev.event_driven_system.utils.data_storage_tools import get_bot_current_loc
from sklearn.preprocessing import OneHotEncoder



class MinimapNavGrid:
    """
    The argument provided to the parameter nav_grid_side_len squared is equal to the total
    number of points on the grid of the minimap which there will be.
    Then naturally the total number of one-hot encoded class labels there will be will equal the total number of
    minimap grid points.
    """

    def __init__(self, nav_grid_side_len):
        self.nav_grid_side_len = nav_grid_side_len
        self.ego_cent_rf_grid_rad = (self.nav_grid_side_len - 1) / 2
        self.ego_cent_rf_grid_x_axes_pnts = np.arange(-self.ego_cent_rf_grid_rad, self.ego_cent_rf_grid_rad+1)
        self.ego_cent_rf_grid_y_axes_pnts = np.arange(self.ego_cent_rf_grid_rad, -self.ego_cent_rf_grid_rad-1, -1)
        self.grid_x_pnts, self.grid_y_pnts = np.meshgrid(self.ego_cent_rf_grid_x_axes_pnts,
                                                         self.ego_cent_rf_grid_y_axes_pnts)
        self._init_grid()

    def _init_grid(self):
        """
        What this function does is simply generate all the grid points and corresponding ohe-hot
        encodied class labels  at one.
        :return: None
        """
        self.grid_pnts = self._gen_grid_pnts()
        self.grid_pnts_ohe_cls_labels = self._gen_grid_pnts_ohe_labels()

    def _gen_grid_pnts(self):
        """
        What this function does is that it generates all the necessary grid points for the
        specified size of the sides of the square grid.
        :return: None
        """
        valid_grid_pnt_coords_permutations_nested_list = list(itertools.product(self.ego_cent_rf_grid_x_axes_pnts,
                                                                                self.ego_cent_rf_grid_y_axes_pnts))
        valid_grid_pnt_coords_permutations_nested_list = list(map(list, valid_grid_pnt_coords_permutations_nested_list))
        return valid_grid_pnt_coords_permutations_nested_list

    def _gen_grid_pnts_ohe_labels(self):
        """
        What this function does is that it generates all the one-hott encoded class labels corresponding with
        the grid points which were (needed to be) generated right before this function being called.
        :return: None
        """
        onehotencoder = OneHotEncoder()
        one_hot_encoded_grid_pnt_coord_labels = onehotencoder.fit_transform(self.grid_pnts).toarray()
        return one_hot_encoded_grid_pnt_coord_labels

    def get_ds_vec_ohe_label(self, ds_x, ds_y):
        """
        What this function does is that it converts the x and y components of the displacement into its
        corresponding one-hot encoded label
        :param ds_x: int
        :param ds_y: int
        :return: array type of the ohe cls label associated with the ds vect (ds_x, ds_y)
        """
        ds_x_float = float(ds_x)
        ds_y_float = float(ds_y)
        ds_vect_floats = [ds_x_float, ds_y_float]
        for grid_pnt_i_coords in self.grid_pnts:
            if ds_vect_floats == grid_pnt_i_coords:
                grid_pnt_coord_idx = self.grid_pnts.index(grid_pnt_i_coords)
                grid_pnt_i_ohe_cls_label = self.grid_pnts_ohe_cls_labels[grid_pnt_coord_idx]
                ds_vect_i_ohe_cls_label = grid_pnt_i_ohe_cls_label
                return ds_vect_i_ohe_cls_label

    def get_ohe_ds_vect(self, ohe_label):
        """
        What this function does is that it takes a ohe cls label and converts this into the
        ds vect it is associated with.
        :param ohe_label: array
        :return: a tuple of 2 ints (ds_x, ds_y)
        """
        for ohe_cls_label_i_idx in range(len(self.grid_pnts_ohe_cls_labels)):
            ohe_cls_label_i = self.grid_pnts_ohe_cls_labels[ohe_cls_label_i_idx]
            if ohe_cls_label_i.tolist() == ohe_label.tolist():
                ohe_label_ds_vect = self.grid_pnts[ohe_cls_label_i_idx]
                ds_x, ds_y = ohe_label_ds_vect
                return ds_x, ds_y

