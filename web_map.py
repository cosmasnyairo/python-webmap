import folium
import pandas
import geocoder

g = geocoder.ip('me')

data = pandas.read_csv('data/volcanoes.csv')
lat = list(data['Latitude'])
lon = list(data['Longitude'])
name = list(data['V_Name'])
hazard = list(data['hazard'])

data2 = open('data/world_population.json', 'r', encoding='utf-8-sig')


def colordefiner(h):
    if h == 1:
        return 'green'
    elif h == 2:
        return 'orange'
    elif h == 3:
        return 'red'
    else:
        return 'white'


html = """<h4><a href="https://www.google.com/search?q=%s" target="_blank">%s</a><br></h4>"""

map1 = folium.Map(location=g.latlng, zoom_start=7, tiles="CartoDB positron")
fg = folium.FeatureGroup(name='Populations')
fg1 = folium.FeatureGroup(name='Me')
fg2 = folium.FeatureGroup(name='Volcanoes')

# polygons over all countries
fg.add_child(folium.GeoJson(data=data2.read(), style_function=lambda x: {'fillColor': 'grey' if x['properties']['POP2005'] < 10000000
                                                                         else 'blue' if 10000000 <= x['properties']['POP2005'] < 20000000
                                                                         else 'purple'
                                                                         }))

# user location
fg1.add_child(folium.Marker(g.latlng, popup='My Location',
                            icon=folium.Icon(color='black')))

# all volcanoes in all countries
for lt, ln, nm, hz in zip(lat, lon, name, hazard):
    iframe = folium.IFrame(html=html % (nm, nm), width=180, height=50)
    fg2.add_child(folium.CircleMarker([lt, ln], radius=6, popup=folium.Popup(
        iframe),
        fill_color=colordefiner(hz), color='black', fill_opacity=1))

# Feature group added
map1.add_child(fg)
map1.add_child(fg1)
map1.add_child(fg2)

# control layer added
# needs to be at the bottom of feature group as it depends on it
map1.add_child(folium.LayerControl())
map1.save('web_map.html')
