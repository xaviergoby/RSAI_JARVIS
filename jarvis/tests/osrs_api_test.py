from jarvis.osrs_api.item import Item
from jarvis.osrs_api.grandexchange import GrandExchange
import urllib.request
from PIL import Image
import matplotlib.pyplot as plt
from jarvis.osrs_api.hiscore import Hiscores

copper_ore_item_name = "Copper ore"
copper_ore_item_id = Item.get_ids(copper_ore_item_name)

ge_copper_ore = GrandExchange.item(copper_ore_item_id)

ge_copper_ore_small_icon_url = ge_copper_ore.icon
ge_copper_ore_large_icon_url = ge_copper_ore.large_icon

small_image = Image.open(urllib.request.urlopen(ge_copper_ore_small_icon_url))
large_image = Image.open(urllib.request.urlopen(ge_copper_ore_large_icon_url))

small_width, small_height = small_image.size
large_width, large_height = large_image.size

print(f"(small_width, small_height): {small_width, small_height}")
print(f"(large_width, large_height): {large_width, large_height}")


# plt.imshow(small_image, cmap='gray')
# plt.title("small_image")

plt.imshow(large_image, cmap='gray')
plt.title("large_image")
plt.show()

print(f"copper ore price: {ge_copper_ore.price()}")

bot_info = Hiscores("xaviergoby")
print(f"bot skills info: {bot_info.skills}")