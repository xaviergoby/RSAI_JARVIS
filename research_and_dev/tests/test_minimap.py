from research_and_dev.event_driven_system.mini_map import Minimap



# minimap = Minimap((791, 591), nav_grid_side_len=15, current_world_grid_loc=None)
minimap = Minimap((791, 591), nav_grid_side_len=15)
print(minimap.current_world_grid_loc)
lmc_pxx = 715
lmc_pxy = 112
print("LMC!")
local_grid_loc = minimap.get_lmc_ds_vec(lmc_pxx, lmc_pxy)
print(f"world local_grid_loc x: {local_grid_loc[0]}  &  world grid y: {local_grid_loc[1]}")
world_grid_loc = minimap.get_lmc_world_grid_loc(lmc_pxx, lmc_pxy)
print(f"world grid x: {world_grid_loc[0]}  &  world grid y: {world_grid_loc[1]}")
print(f"Current world grid loc: {minimap.current_world_grid_loc}")
print("UPDATING mini_map current world grid loc coords....")
minimap.update_current_world_grid_loc(world_grid_loc)
print("UPDATED mini_map current world grid loc coords!")
print(f"Current world grid loc: {minimap.current_world_grid_loc}")
lmc_pxx = 715
lmc_pxy = 112
print("\nLMC!")
local_grid_loc = minimap.get_lmc_ds_vec(lmc_pxx, lmc_pxy)
print(f"world local_grid_loc x: {local_grid_loc[0]}  &  world grid y: {local_grid_loc[1]}")
world_grid_loc = minimap.get_lmc_world_grid_loc(lmc_pxx, lmc_pxy)
print(f"world grid x: {world_grid_loc[0]}  &  world grid y: {world_grid_loc[1]}")
print(f"Current world grid loc: {minimap.current_world_grid_loc}")
print("UPDATING mini_map current world grid loc coords....")
minimap.update_current_world_grid_loc(world_grid_loc)
print("UPDATED mini_map current world grid loc coords!")
print(f"Current world grid loc: {minimap.current_world_grid_loc}")

local_nav_grid_pnt_ohe_loc_label = minimap.get_ds_vec_ohe_label(local_grid_loc[0], local_grid_loc[1])
print(f"local_nav_grid_pnt_ohe_loc_label for {local_grid_loc}: {local_nav_grid_pnt_ohe_loc_label}")
ohe_loc_label_local_nav_grid_pnt = minimap.get_ohe_ds_vect(local_nav_grid_pnt_ohe_loc_label)
print(f"ohe_loc_label_local_nav_grid_pnt for {local_nav_grid_pnt_ohe_loc_label}: {ohe_loc_label_local_nav_grid_pnt}")

mm_roi_img_bbox_coords = minimap.minimap_roi_img_bbox_coords
print(f"mini_map.minimap_roi_img_bbox_coords: {minimap.minimap_roi_img_bbox_coords}")