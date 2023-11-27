import sys
import xml.etree.ElementTree as ET

# NOTE: jump to START below to skip over data

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

## Richford_NW
#ULCOORDS = (-76.25,42.3333333377999)
## Binghamton East_CE
#LRCOORDS = (-75.8125,42.0416666715999)

## Ogdensburg East NW = Lisbon NW x Heuvelton NW
##-75.375,44.708333334
##-75.5,44.5833333342
#ULCOORDS = (-75.5,44.708333334)
## Saratoga Springs_CE
#LRCOORDS = (-73.8125,43.0416666699999)

# Syracuse West_NW
# TODO

# Webster NW / Oswego East NW
ULCOORDS = (-77.5,43.458333336)
# Gulf Summit CE
LRCOORDS = (-75.5625,42.0416666715999)

INCLIST = set([])


# START START START START

class MyException(Exception):
    pass

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
            raise MyException("Too many elements")
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

def get_urcoord(pm):
    coordtexts = get_coords(pm)
    assert len(coordtexts) == 5
    assert coordtexts[0] == coordtexts[4]
    return tuple(map(float, coordtexts[1]))

def for_each_placemark(fol):
    return fol.findall(NS + 'Placemark')

def for_each_folder(et):
    kml = et.getroot()
    ns, kmltag = kml.tag.rsplit('}', 1)
    ns += '}'
    assert ns == NS
    for doc in kml:
        for fol in doc:
            yield fol

def check_placemark_coords(pm):
    coords = get_ulcoord(pm)
    if (coords[0] >= ULCOORDS[0] and coords[0] <= LRCOORDS[0] and
        coords[1] >= LRCOORDS[1] and coords[1] <= ULCOORDS[1]
       ):
        return True
    return False

def check_placemark_inclist_remove(pm):
    """ Destructively updates INCLIST """
    block_name = get_block_name(pm)
    try:
        INCLIST.remove(block_name)
        return True
    except KeyError:
        return False

def add_name(pm):
    block_name = get_block_name(pm)
    name = ET.SubElement(pm, 'name')
    name.text = block_name
    print("Adding name", block_name)

def et_filter_placemarks(et, check_placemark):
    for fol in for_each_folder(et):
        #keepers = list()
        nkeepers = 0
        discard = list()
        ndiscard = 0
        for pm in for_each_placemark(fol):
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

def lat_lon_bname_key(lat_lon_bname):
    lat, lon, bname = lat_lon_bname
    return (-lat, -lon, bname)

def et_dump_coords(et, outfile):
    lat_lon_bname = set()
    for fol in for_each_folder(et):
        for pm in for_each_placemark(fol):
            bname = get_block_name(pm)
            ulcoords = get_ulcoord(pm)
            lat_lon_bname.add((ulcoords[1], ulcoords[0], bname))
    with open(outfile, "w") as outf:
        for lat, lon, bname in sorted(lat_lon_bname, key=lat_lon_bname_key):
            print(lat, lon, bname, file=outf)

def latlon2id(lon, lat):
    latdeg = int(lat)
    londeg = int(-lon)
    latpart = "HABCDEFG"[round((lat % 1) * 8)]
    lonpart = str(round((-lon % 1) * 8))
    assert lonpart in "01234567"
    if latpart == "H":
        latdeg -= 1
    if lonpart == "0":
        lonpart = "8"
        londeg -= 1
    return str(latdeg) + "0" + str(londeg) + latpart + lonpart

def et_dump_urls(et, outfile):
    id_name = set()
    for fol in for_each_folder(et):
        for pm in for_each_placemark(fol):
            bname = get_block_name(pm)
            if bname.endswith("_NW"):
                name = bname[:-3]
                ulcoords = get_urcoord(pm)
                blk_id = latlon2id(*ulcoords)
                id_name.add((blk_id, name))
            else:
                assert bname.endswith("_CE")
    with open(outfile, "w") as outf:
        prev = None
        for blk_id, name in sorted(id_name):
            if prev == blk_id:
                print("DUPLICATE:", blk_id, file=outf)
            prev = blk_id
            print(blk_id, name, file=outf)


USAGE = """
ARGS:
  coords: dump each block's ul coords
  urls: dump superblock urls based on NW coords
  bounds: dump kml based on hard-coded bounding box
  inclist: dump kml based on hard-coded include list
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)
    action = sys.argv[1]
    if action == "coords":
        et = ET.parse('Block_Master_Priority.kml')
        outfile = "out_coords.txt"
        et_dump_coords(et, outfile)
        print("Wrote:", outfile)
        sys.exit(0)
    elif action == "urls":
        et = ET.parse('Block_Master_Priority.kml')
        outfile = "out_urls.txt"
        et_dump_urls(et, outfile)
        print("Wrote:", outfile)
        sys.exit(0)
    elif action == "bounds":
        et = ET.parse('Block_Master_Priority.kml')
        et_filter_placemarks(et, check_placemark_coords)
        outfile = "output.kml"
        et.write(outfile)
        print("Wrote:", outfile)
        sys.exit(0)
    elif action == "inclist":
        assert INCLIST
        et = ET.parse('Block_Master_Priority.kml')
        et_filter_placemarks(et, check_placemark_inclist_remove)
        # Warn if any elements left in INCLIST
        if INCLIST:
            print("WARNING: leftovers in INCLIST:")
            for name in sorted(INCLIST):
                print("\t", name)
        outfile = "output.kml"
        et.write(outfile)
        print("Wrote:", outfile)
        sys.exit(0)
    else:
        print("ERROR: unrecognized param", action)
        print(USAGE)
        sys.exit(1)
