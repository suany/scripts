import sys
import xml.etree.ElementTree as ET

# NOTE: coordinates are lon/lat instead of conventional lat/lon!

NS = '{http://www.opengis.net/kml/2.2}'

## Geneva North_NW
#ULCOORDS = (-77.0, 42.9583333367999)
## Newark Valley_CE
#LRCOORDS = (-76.1875,42.1666666713999)


## Dansville_NW
#ULCOORDS = (-77.75,42.5833333373999)
## Big Flats_CE
#LRCOORDS = (-76.9375,42.1666666713999)

# Richford_NW
ULCOORDS = (-76.25,42.3333333377999)
#Binghamton East_CE
LRCOORDS = (-75.8125,42.0416666715999)

# Syracuse West_NW
# TODO

"""
Get the one element from iterator.
Odd behavior if iterator contains None.
"""
def one(iterator):
    single = set()
    for x in iterator:
        if not single:
            single.add(x)
        else:
            raise ValueError # Too many elements
    return single.pop()

def get_block_name(pm):
    sd = one(pm.iter(NS + 'SimpleData'))
    return sd.text

def get_coords(pm):
    coordelt = one(pm.iter(NS + 'coordinates'))
    coordtexts = [coord.split(',', 1) for coord in coordelt.text.split()]
    return coordtexts

def get_ulcoord(pm):
    coordtexts = get_coords(pm)
    assert len(coordtexts) == 5
    assert coordtexts[0] == coordtexts[4]
    return tuple(map(float, coordtexts[0]))

def check_placemark(pm):
    coords = get_ulcoord(pm)
    if (coords[0] >= ULCOORDS[0] and coords[0] <= LRCOORDS[0] and
        coords[1] >= LRCOORDS[1] and coords[1] <= ULCOORDS[1]
       ):
        return True
    return False

def add_name(pm):
    block_name = get_block_name(pm)
    name = ET.SubElement(pm, 'name')
    name.text = block_name
    print("Adding name", block_name)

def process_folder(fol):
    #keepers = list()
    nkeepers = 0
    discard = list()
    ndiscard = 0
    for pm in fol.findall(NS + 'Placemark'):
        if check_placemark(pm):
            #keepers.append(pm)
            add_name(pm)
            nkeepers += 1
        else:
            discard.append(pm)
            ndiscard += 1
    print("Keepers:", nkeepers, "Discards:", ndiscard)
    for pm in discard:
        fol.remove(pm)

def process_elt_tree(et):
    kml = et.getroot()
    ns, kmltag = kml.tag.rsplit('}', 1)
    ns += '}'
    assert ns == NS
    for doc in kml:
        for fol in doc:
            process_folder(fol)

if __name__ == "__main__":
    et = ET.parse('Block_Master_Priority.kml')
    process_elt_tree(et)
    et.write('test_output.kml')
