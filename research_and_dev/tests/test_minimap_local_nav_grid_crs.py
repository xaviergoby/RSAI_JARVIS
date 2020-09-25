from research_and_dev.event_driven_system.mini_map.minimap_nav_grid_crs import MinimapNavGridCoordRefSys



mm_local_nav_grid_crs = MinimapNavGridCoordRefSys((791, 591))
lmc_pxx = 715
# lmc_pxx = 652
# lmc_pxx = 764
lmc_pxy = 112
gx, gy = mm_local_nav_grid_crs.convert_px_coords_2_ds_vec(lmc_pxx, lmc_pxy)
print(f"lmc_pxx: {lmc_pxx}  &  gx: {gx}\nlmc_pxy: {lmc_pxy}  &  gy: {gy}")