from lets_plot import *
from lets_plot.geo_data import *

# Set 'dark' theme for interactive map.
#
LetsPlot.set(maptiles_lets_plot(theme='dark'))

# %%

# Data

# List of major JetBrains offices.
# Note: the offices capacity is just my guess.
offices = [
	["Prague", "CZ", "Headquarters", 100],
	["Petersburg", "Russia", "R&D Center", 1000],
	["Moscow", "Russia", "R&D Center", 100],
	["Novosibirsk", "Russia", "R&D Center", 50],
	["München", "Germany", "R&D Center", 200],
	["Amsterdam", "Netherlands", "R&D Center", 100],
	["Boston", "US", "R&D Center", 10],
	["Marlton", "US", "Sales", 10],
	["Foster City", "US", "Sales", 10],
]

dat = dict(
		city=[o[0] for o in offices],
		country=[o[1] for o in offices],
		kind=[o[2] for o in offices],
		size=[o[3] for o in offices],
)

# %%

# Geocoding

# Obtain coordinates of cities where the offices are located.
city_geocoder = geocode_cities(dat['city']).countries(dat['country'])

# %%

# An interactive map showing JetBrains major offices worldwide.

p = (ggplot(dat) +
     geom_livemap() +
     geom_point(
		     aes(color='kind', shape='kind', size='size'),
		     map_join=['city', 'city'],
		     map=city_geocoder.get_centroids(),
		     tooltips=layer_tooltips()
			     .line('@kind')
			     .line('@city (@country)')
			     .line("Capacity|@size")
			     .format('size', ".0f")
			     .min_width(100)
			     .color('black')) +
     scale_size(range=[5, 30]) +
     guides(size='none'))

p.show()