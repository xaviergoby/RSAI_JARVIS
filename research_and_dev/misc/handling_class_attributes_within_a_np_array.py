import numpy as np


class CellClass:
    def __init__(self, unit_cell_x_distance):
        self.unit_cell_x_distance_2_origin = unit_cell_x_distance
        self.leftmost_x_px = 708
        self.rightmost_x_px = 711
        self.cell_x_id = unit_cell_x_distance


    def update_leftmost_x_px(self):
        if self.cell_x_id != 0:
            self.leftmost_x_px = self.leftmost_x_px + self.unit_cell_x_distance_2_origin * 4
            self.rightmost_x_px = self.rightmost_x_px + self.unit_cell_x_distance_2_origin * 4
        else:
            pass
        return self


    def __str__(self):

        return "\nLeft most x pixel: {0}" \
               "\nRight most x pixel: {1}"\
               "\nCell xID: {2}".format(self.leftmost_x_px, self.rightmost_x_px, self.cell_x_id)


vecfunc = np.vectorize(CellClass.update_leftmost_x_px, otypes=[object])
myarray2 = np.array([CellClass(i) for i in range(-10, 10 + 1)])
vecfunc(myarray2)

for obj_i in myarray2:
    print(obj_i)






# initial_left_px = 708
# final_left_px = 748
#
#
# class CellClass:
#     def __init__(self):
#         self.left_border_x_px = None
#         self.right_border_x_px = None
#     def modifyvar(self):
#         self.left_border_x_px += 4
#         return self
#
# vecfunc = np.vectorize(CellClass.modifyvar, otypes=[object])
# myarray2 = np.array([CellClass() for px_x_i in range()])
# vecfunc(myarray2)