import json
import settings
import os


def get_bot_current_loc():
	"""

	:return: list containing the bots x and y grid location w.r.t globak/world grid map (Explsv OSRS Map coordnates)
	e.g. [3216, 3219]
	"""
	json_path = os.path.join(settings.EVENT_DRIVEN_SYS_DATA_DIR, "init_world_coords.json")
	with open(json_path, 'r') as bot_memory_data_json:
		bot_memory_data = json.load(bot_memory_data_json)
		return bot_memory_data
		# return bot_memory_data["current_location"]


def update_bot_current_loc(bot_current_loc):
	json_path = os.path.join(settings.EVENT_DRIVEN_SYS_DATA_DIR, "init_world_coords.json")
	with open(json_path, 'w') as bot_memory_data_json:
		json.dump(bot_current_loc, bot_memory_data_json)


if __name__ == "__main__":
	# [3216, 3219]
	update_bot_current_loc([3216, 3219])
	current_loc = get_bot_current_loc()
	print(f"current_loc: {current_loc}")
	new_current_loc = [3218, 3222]
	update_bot_current_loc(new_current_loc)
	update_current_loc = get_bot_current_loc()
	print(type(update_current_loc))
	print(f"update_current_loc: {update_current_loc}")
	print(f"update_current_loc: {type(update_current_loc)}")
	print(type(update_current_loc))
	print(len(update_current_loc))
	print(type(update_current_loc[0]))
	print(type(update_current_loc[1]))
