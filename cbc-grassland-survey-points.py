#!/usr/bin/env python3

from datetime import date
from polycircles import polycircles # pip3 install polycircles
import csv
import simplekml # pip3 install simplekml
import sys

UploadedIcons = set([
  "01.png",
  "02.png",
  "03.png",
  "04.png",
  "05.png",
  "06.png",
  "07.png",
  "08.png",
  "09.png",
  "10.png",
  "11.png",
  "12.png",
  "13.png",
  "14.png",
  "15.png",
  "16.png",
  "17.png",
  "18.png",
  "19.png",
  "20.png",
  "21.png",
  "22.png",
  "23.png",
  "24.png",
  "25.png",
  "26.png",
  "27.png",
  "28.png",
  "29.png",
  "30.png",
  "n01r.png",
  "n01y.png",
  "n03r.png",
  "n03y.png",
  "n05.png",
  "n15.png",
  "o01.png",
  "o01b.png",
  "o01e.png",
  "o02.png",
  "o02e.png",
  "o02s.png",
  "o05.png",
  "o06.png",
  "o26b.png",
  "r01b.png",
  "y01.png",
  "y01b.png",
  "y01e.png",
  "y02.png",
  "y02e.png",
  "y02s.png",
  "y03.png",
  "y04.png",
  "y05.png",
  "y06.png",
  "y07.png",
  "y08.png",
  "y09.png",
  "y10.png",
  "y11.png",
  "y12.png",
  "y13.png",
  "y14.png",
  "y15.png",
  "y16.png",
  "y17.png",
  "y18.png",
  "y19.png",
  "y20.png",
  "y204a.png",
  "y204c.png",
  "y204e.png",
  "y21.png",
  "y22.png",
  "y23.png",
  "y24.png",
  "y25.png",
  "y26.png",
  "y26b.png",
  "y27.png",
  "y28.png",
  "y29.png",
  "y59a.png",
  "yA.png",
  "yAA.png",
  "yAB.png",
  "yB.png",
  "yC.png",
  "yCA.png",
  "yCB.png",
  "yCC.png",
  "yCD.png",
  "yD.png",
  "yE.png",
  ])

def icon_size(png):
    if png in ("y204a.png", "y204c.png", "y204e.png"):
        return 20
    return 16
def icon_scale(png):
    return icon_size(png)/32

Area2Points = {
  "BluegrassHanshaw" : [
    ("y01", "BLUEGRASS 1", 42.4608136, -76.4474043),
    ("y02", "BLUEGRASS 2", 42.4631257, -76.4451304),
    ("y03", "BLUEGRASS 3", 42.4672536, -76.4533796),
    ("y04", "BLUEGRASS 4", 42.4655535, -76.4578572),
    ("y05", "BLUEGRASS 5", 42.463702, -76.4602889),
    ("o01", "HANSHAW 1", 42.469632, -76.445865),
    ("o02", "HANSHAW 2", 42.471553, -76.443163),
    ],
  "MtPleasant" : [
    ("y01", "MP 01", 42.46728, -76.36909),
    ("y05", "MP 05", 42.46717, -76.36647),
    ("y59a", "MP 59A", 42.468825, -76.362815),
    ("y06", "MP 06", 42.46243, -76.36573),
    ("y08", "MP 08", 42.45927, -76.3683),
    ("y12", "MP 12", 42.45996, -76.37271),
    ("y13", "MP 13", 42.46178, -76.37275),
    ("y204a", "MP 204A", 42.461611, -76.378573),
    ("y204c", "MP 204C", 42.457468, -76.38714),
    ("y204e", "MP 204E", 42.454593, -76.36125),
    ("y24", "RS 24", 42.45898, -76.36586),
    ("y25", "RS 25", 42.45893, -76.370489),
    ("y26", "RS 26", 42.45863, -76.38155),
    ("y26b", "RS 26B", 42.45856, -76.38525),
    ],
  "Stevenson" : [
    ("yB", "STEVENSON RD 338B", 42.44498, -76.436942),
    ("yD", "STEVENSON RD 338D", 42.444594, -76.433412),
    ("yC", "STEVENSON RD 338C", 42.443883, -76.429053),
    ],
  "AthleticFields" : [
    ("yA", "MCGOVERN A", 42.437179, -76.454886),
    ("yB", "MCGOVERN B", 42.438925, -76.4561),
    ("yC", "MCGOVERN C", 42.434737, -76.456659),
    ("yD", "MCGOVERN D", 42.43375, -76.451392),
    ],
  "CURuminantCenter" : [
    ("yCA", "CURC 11C A", 42.439491, -76.23384),
    ("yCC", "CURC 11C C", 42.437802, -76.231769),
    ("yCD", "CURC 11C D", 42.436103, -76.230454),
    ("yD", "CURC 11D", 42.435835, -76.265242),
    ("yAA", "CURC 11A A", 42.452442, -76.246086),
    ("yAB", "CURC 11A B", 42.456374, -76.247775),
    ],
  "EdHillRd" : [
    ("yA", "EH 363A", 42.523451, -76.335739),
    ],
  "TurkeyHillRd" : [
    ("yA", "TURKEY HILL RD 418A A", 42.434358, -76.432681),
    ("yB", "TURKEY HILL RD 418A B", 42.434336, -76.431008),
    ],
  "TownleyWildlifePreserve" : [
    ("y01", "TOWNLEY 01", 42.536598, -76.416924),
    ("y02", "TOWNLEY 02", 42.536771, -76.418692),
    ],
  "DunlopMeadow" : [
    ("y01", "DM 01", 42.38504, -76.3958),
    ("y02", "DM 02", 42.38383, -76.39714),
    ("y03", "DM 03", 42.38491, -76.39921),
    ("y04", "DM 04", 42.387204, -76.400234),
    ("o02", "RS 02", 42.385272, -76.394466),
    ],
  "Summerhill" : [
    ("y01", "SU 01", 42.3592, -76.261616),
    ("y02", "SU 02", 42.359805, -76.26415),
    ("y04", "SU 04", 42.363217, -76.266136),
    ],
  "SimsJennings" : [
    #("y01", "SJ 01", 42.560977, -76.56665), # obsolete
    ("y01b", "SJ 01B", 42.560403, -76.567387),
    ("y02", "SJ 02", 42.559326, -76.56878),
    ("y03", "SJ 03", 42.556921, -76.563909),
    ("y04", "SJ 04", 42.555896, -76.561326),
    ("y05", "SJ 05", 42.5616, -76.563253),
    ("y06", "SJ 06", 42.55544, -76.565799),
    # NOTE: SJ 07 was 42.554103, -76.564279 in <2025 fllt-locations.csv
    ("y07", "SJ 07", 42.554051, -76.564037),
    ("y08", "SJ 08", 42.554263, -76.5597),
    ],
  "LindsayParsons" : [
    ("y01", "LP-1", 42.31172, -76.51966),
    ("y02", "LP-2", 42.31268, -76.51997),
    ("y03", "LP-3", 42.3123, -76.52261),
    ("y04", "LP-4", 42.30491, -76.51937),
    ("o05", "LP-5", 42.3051, -76.51803),
    ("o06", "LP-6", 42.30733, -76.51719),
    ],
}

def gen_kml(name):
    points = Area2Points[name]
    kml = simplekml.Kml()
    for icon, pname, lat, lon in points:
        # Check png
        png = icon + ".png"
        if not png in UploadedIcons:
            print("XXX", png)
        assert png in UploadedIcons
        url = "https://suan-yong.com/icons/" + png
        # Point
        pt = kml.newpoint(name=pname)
        pt.coords = [(lon, lat)]
        pt.style.iconstyle.icon.href = url
        pt.style.iconstyle.scale = icon_scale(png)
        # 100m Circle
        pcir = polycircles.Polycircle(
                        latitude=lat, longitude=lon, radius=100,
                        number_of_vertices=36)
        ls = kml.newlinestring(name=pname + " 100m")
        ls.coords = pcir.to_kml()
        #ls.tesselate = 1
        #ls.style.linestyle.width = 1
        ls.style.linestyle.color = simplekml.Color.yellow

    outfile = "gen-" + name + ".kml"
    print("Writing", outfile)
    kml.save(outfile)

def gen_csv(outname, areas):
    r1_points = list()
    r2_lats = list()
    r3_lons = list()
    for area in areas:
        points = Area2Points[area]
        for _, pname, lat, lon in points:
            r1_points.append(pname)
            r2_lats.append(lat)
            r3_lons.append(lon)
    with open(outname, 'w', newline='') as ofp:
        writer = csv.writer(ofp)
        npoints = len(r1_points)
        assert npoints == len(r2_lats)
        assert npoints == len(r3_lons)
        writer.writerow(["", ""] + r1_points)
        writer.writerow(["Latitude", ""] + r2_lats)
        writer.writerow(["Longitude", ""] + r3_lons)
        today = date.today().strftime("%m/%d/%Y")
        writer.writerow(["Date", ""] + [today] * npoints)
        writer.writerow(["Start Time", ""] + [""] * npoints)
        writer.writerow(["State", ""] + ["NY"] * npoints)
        writer.writerow(["Country", ""] + ["US"] * npoints)
        writer.writerow(["Protocol", ""] + ["Casual"] * npoints)
        writer.writerow(["Num Observers", ""] + [1] * npoints)
        writer.writerow(["Duration (min)", ""] + [""] * npoints)
        writer.writerow(["All Obs Reported (Y/N)", ""] + ["N"] * npoints)
        writer.writerow(["Dist Traveled (Miles)", ""] + [""] * npoints)
        writer.writerow(["Area Covered (Acres)", ""] + [""] * npoints)
        writer.writerow(["Notes", ""] + ["dummy checklist"] * npoints)
    print("Wrote", outname)

#gen_kml("AthleticFields")
#gen_kml("BluegrassHanshaw")
#gen_kml("CURuminantCenter")
#gen_kml("DunlopMeadow")
#gen_kml("EdHillRd")
#gen_kml("LindsayParsons")
#gen_kml("MtPleasant")
#gen_kml("SimsJennings")
#gen_kml("Stevenson")
#gen_kml("Summerhill")
#gen_kml("TownleyWildlifePreserve")
#gen_kml("TurkeyHillRd")

gen_csv("fllt-locations.csv", ["LindsayParsons", "SimsJennings", "Summerhill"])
gen_csv("cu-locations.csv",
        ["AthleticFields",
         "BluegrassHanshaw",
         "DunlopMeadow",
         "EdHillRd",
         "MtPleasant",
         "Stevenson",
         "TownleyWildlifePreserve",
         "TurkeyHillRd",
         ])

gen_csv("cu-bluegrass.csv", ["BluegrassHanshaw"])
gen_csv("cu-dunlop.csv", ["DunlopMeadow"])
gen_csv("cu-easthill.csv", ["AthleticFields", "Stevenson", "TurkeyHillRd"])
gen_csv("cu-mtpleasant.csv", ["MtPleasant"])
gen_csv("cu-north.csv", ["EdHillRd", "TownleyWildlifePreserve"])
gen_csv("cu-ruminants.csv", ["CURuminantCenter"])

