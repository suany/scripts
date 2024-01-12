import os, sys
import xml.etree.ElementTree as ET
import requests # pip3 install requests

DO_DOWNLOAD = True # If False, use cached html files, fail if does not exist
USE_CACHE = True   # Use cached html file if exists

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

### Column west of above, to include all of Steuben County
## Hilton NW
#ULCOORDS = (-77.875,43.3333333361999)
## Troupsburg CE
#LRCOORDS = (-77.5625,42.0416666715999)

# Syracuse West_NW
# TODO

### GREATER CNY BOUNDS, incl Oswego County ###
## Hilton NW / Ellisburg NW
#ULCOORDS = (-77.875,43.7083333356)
## Gulf Summit CE
#LRCOORDS = (-75.5625,42.0416666715999)

### WNY west of Hilton above ###
## South Ripley NW / Newfane NW
#ULCOORDS = (-79.75,43.3333333361999)
## Wellsville South CE
#LRCOORDS = (-77.9375,42.0416666715999)

### Column east of above, to include Oneida County
## Glenfield NW
#ULCOORDS = (-75.5,43.7083333356)
## Readburn CE
##LRCOORDS = (-75.1875,42.0416666715999)

### WNY and CNY ###
## South Ripley NW / Copper Lake NW
ULCOORDS = (-79.75,43.7083333356)
# Readburn CE
LRCOORDS = (-75.1875,42.0416666715999)

INCLIST = set([
    "Mecklenburg_NW",
    "Mecklenburg_CE",
    "Ithaca West_NW",
])

COUNTIES1 = set([
    "Ontario",
    "Oswego",
    "Wayne",
    "Seneca",
    "Cayuga",
    "Onondaga",
    "Steuben",
    "Schuyler",
    "Yates",
])

COUNTIES = set([
    "Monroe",
    "Livingston",
    "Alleghany",
    "Chemung",
    "Tompkins",
    "Tioga",
    "Cortland",
    "Madison",
    "Oneida",
    "Jefferson",
])

USGSBLOCK_TO_URLID = {
  "Pattersquash Island"    : "40072F7",
  "Shinnecock Inlet"       : "40072G4",
  "Quogue"                 : "40072G5",
  "Eastport"               : "40072G6",
  "Moriches"               : "40072G7",
  "Bellport"               : "40072G8",
  "Napeague Beach"         : "40072H1",
  "East Hampton"           : "40072H2",
  "Sag Harbor"             : "40072H3",
  "Southampton"            : "40072H4",
  "Mattituck"              : "40072H5",
  "Riverhead"              : "40072H6",
  "Wading River"           : "40072H7",
  "Middle Island"          : "40072H8",
  "West Gilgo Beach"       : "40073E4",
  "Jones Inlet"            : "40073E5",
  "Lawrence"               : "40073E6",
  "Far Rockaway"           : "40073E7",
  "Coney Island"           : "40073E8",
  "Sayville"               : "40073F1",
  "Bay Shore East"         : "40073F2",
  "Bay Shore West"         : "40073F3",
  "Amityville"             : "40073F4",
  "Freeport"               : "40073F5",
  "Lynbrook"               : "40073F6",
  "Jamaica"                : "40073F7",
  "Brooklyn"               : "40073F8",
  "Patchogue"              : "40073G1",
  "Central Islip"          : "40073G2",
  "Greenlawn"              : "40073G3",
  "Huntington"             : "40073G4",
  "Hicksville"             : "40073G5",
  "Sea Cliff"              : "40073G6",
  "Flushing"               : "40073G7",
  "Central Park"           : "40073G8",
  "Port Jefferson"         : "40073H1",
  "Saint James"            : "40073H2",
  "Lloyd Harbor"           : "40073H4",
  "Mamaroneck"             : "40073H6",
  "Mount Vernon"           : "40073H7",
  "Yonkers"                : "40073H8",
  "The Narrows"            : "40074E1",
  "Arthur Kill"            : "40074E2",
  "Jersey City"            : "40074F1",
  "Montauk Point"          : "41071A8",
  "Gardiners Island East"  : "41072A1",
  "Greenport"              : "41072A3",
  "Southold"               : "41072A4",
  "Glenville"              : "41073A6",
  "White Plains"           : "41073A7",
  "Nyack"                  : "41073A8",
  "Pound Ridge"            : "41073B5",
  "Mount Kisco"            : "41073B6",
  "Ossining"               : "41073B7",
  "Haverstraw"             : "41073B8",
  "Peach Lake"             : "41073C5",
  "Croton Falls"           : "41073C6",
  "Mohegan Lake"           : "41073C7",
  "Peekskill"              : "41073C8",
  "Brewster"               : "41073D5",
  "Lake Carmel"            : "41073D6",
  "Oscawana Lake"          : "41073D7",
  "West Point"             : "41073D8",
  "Pawling"                : "41073E5",
  "Poughquag"              : "41073E6",
  "Hopewell Junction"      : "41073E7",
  "Wappingers Falls"       : "41073E8",
  "Dover Plains"           : "41073F5",
  "Verbank"                : "41073F6",
  "Pleasant Valley"        : "41073F7",
  "Poughkeepsie"           : "41073F8",
  "Amenia"                 : "41073G5",
  "Millbrook"              : "41073G6",
  "Salt Point"             : "41073G7",
  "Hyde Park"              : "41073G8",
  "Sharon"                 : "41073H4",
  "Millerton"              : "41073H5",
  "Pine Plains"            : "41073H6",
  "Rock City"              : "41073H7",
  "Kingston East"          : "41073H8",
  "Park Ridge"             : "41074A1",
  "Thiells"                : "41074B1",
  "Sloatsburg"             : "41074B2",
  "Greenwood Lake"         : "41074B3",
  "Popolopen Lake"         : "41074C1",
  "Monroe"                 : "41074C2",
  "Warwick"                : "41074C3",
  "Pine Island"            : "41074C4",
  "Unionville"             : "41074C5",
  "Cornwall-on-Hudson"     : "41074D1",
  "Maybrook"               : "41074D2",
  "Goshen"                 : "41074D3",
  "Middletown"             : "41074D4",
  "Otisville"              : "41074D5",
  "Port Jervis North"      : "41074D6",
  "Pond Eddy"              : "41074D7",
  "Shohola"                : "41074D8",
  "Newburgh"               : "41074E1",
  "Walden"                 : "41074E2",
  "Pine Bush"              : "41074E3",
  "Wurtsboro"              : "41074E4",
  "Yankee Lake"            : "41074E5",
  "Hartwood"               : "41074E6",
  "Highland Lake"          : "41074E7",
  "Eldred"                 : "41074E8",
  "Clintondale"            : "41074F1",
  "Gardiner"               : "41074F2",
  "Napanoch"               : "41074F3",
  "Ellenville"             : "41074F4",
  "Woodridge"              : "41074F5",
  "Monticello"             : "41074F6",
  "White Lake"             : "41074F7",
  "Lake Huntington"        : "41074F8",
  "Rosendale"              : "41074G1",
  "Mohonk Lake"            : "41074G2",
  "Kerhonkson"             : "41074G3",
  "Rondout Reservoir"      : "41074G4",
  "Grahamsville"           : "41074G5",
  "Liberty East"           : "41074G6",
  "Liberty West"           : "41074G7",
  "Jeffersonville"         : "41074G8",
  "Kingston West"          : "41074H1",
  "Ashokan"                : "41074H2",
  "West Shokan"            : "41074H3",
  "Peekamoose Mountain"    : "41074H4",
  "Claryville"             : "41074H5",
  "Willowemoc"             : "41074H6",
  "Livingston Manor"       : "41074H7",
  "Roscoe"                 : "41074H8",
  "Narrowsburg"            : "41075E1",
  "Damascus"               : "41075F1",
  "Callicoon"              : "41075G1",
  "Long Eddy"              : "41075G2",
  "Horton"                 : "41075H1",
  "Fishs Eddy"             : "41075H2",
  "Hancock"                : "41075H3",
  "Copake"                 : "42073A5",
  "Ancram"                 : "42073A6",
  "Clermont"               : "42073A7",
  "Saugerties"             : "42073A8",
  "Egremont"               : "42073B4",
  "Hillsdale"              : "42073B5",
  "Claverack"              : "42073B6",
  "Hudson South"           : "42073B7",
  "Cementon"               : "42073B8",
  "State Line"             : "42073C4",
  "Chatham"                : "42073C5",
  "Stottville"             : "42073C6",
  "Hudson North"           : "42073C7",
  "Leeds"                  : "42073C8",
  "Canaan"                 : "42073D4",
  "East Chatham"           : "42073D5",
  "Kinderhook"             : "42073D6",
  "Ravena"                 : "42073D7",
  "Alcove"                 : "42073D8",
  "Hancock MA"             : "42073E3",
  "Stephentown Center"     : "42073E4",
  "Nassau"                 : "42073E5",
  "East Greenbush"         : "42073E6",
  "Delmar"                 : "42073E7",
  "Clarksville"            : "42073E8",
  "Berlin"                 : "42073F3",
  "Taborton"               : "42073F4",
  "Averill Park"           : "42073F5",
  "Troy South"             : "42073F6",
  "Albany"                 : "42073F7",
  "Voorheesville"          : "42073F8",
  "North Pownal"           : "42073G3",
  "Grafton"                : "42073G4",
  "Tomhannock"             : "42073G5",
  "Troy North"             : "42073G6",
  "Niskayuna"              : "42073G7",
  "Schenectady"            : "42073G8",
  "Hoosick Falls"          : "42073H3",
  "Eagle Bridge"           : "42073H4",
  "Schaghticoke"           : "42073H5",
  "Mechanicville"          : "42073H6",
  "Round Lake"             : "42073H7",
  "Burnt Hills"            : "42073H8",
  "Woodstock"              : "42074A1",
  "Bearsville"             : "42074A2",
  "Phoenicia"              : "42074A3",
  "Shandaken"              : "42074A4",
  "Seager"                 : "42074A5",
  "Arena"                  : "42074A6",
  "Lewbeach"               : "42074A7",
  "Downsville"             : "42074A8",
  "Kaaterskill Clove"      : "42074B1",
  "Hunter"                 : "42074B2",
  "Lexington"              : "42074B3",
  "West Kill"              : "42074B4",
  "Fleischmanns"           : "42074B5",
  "Margaretville"          : "42074B6",
  "Andes"                  : "42074B7",
  "Hamden"                 : "42074B8",
  "Freehold"               : "42074C1",
  "Hensonville"            : "42074C2",
  "Ashland"                : "42074C3",
  "Prattsville"            : "42074C4",
  "Roxbury"                : "42074C5",
  "Hobart"                 : "42074C6",
  "Bloomville"             : "42074C7",
  "Delhi"                  : "42074C8",
  "Greenville"             : "42074D1",
  "Durham"                 : "42074D2",
  "Livingstonville"        : "42074D3",
  "Gilboa"                 : "42074D4",
  "Stamford"               : "42074D5",
  "Harpersfield"           : "42074D6",
  "Davenport"              : "42074D7",
  "West Davenport"         : "42074D8",
  "Westerlo"               : "42074E1",
  "Rensselaerville"        : "42074E2",
  "Middleburgh"            : "42074E3",
  "Breakabeen"             : "42074E4",
  "Summit"                 : "42074E5",
  "Charlotteville"         : "42074E6",
  "Schenevus"              : "42074E7",
  "Milford"                : "42074E8",
  "Altamont"               : "42074F1",
  "Gallupville"            : "42074F2",
  "Schoharie"              : "42074F3",
  "Cobleskill"             : "42074F4",
  "Richmondville"          : "42074F5",
  "South Valley"           : "42074F6",
  "Westford"               : "42074F7",
  "Cooperstown"            : "42074F8",
  "Rotterdam Junction"     : "42074G1",
  "Duanesburg"             : "42074G2",
  "Esperance"              : "42074G3",
  "Carlisle"               : "42074G4",
  "Sharon Springs"         : "42074G5",
  "Sprout Brook"           : "42074G6",
  "East Springfield"       : "42074G7",
  "Richfield Springs"      : "42074G8",
  "Pattersonville"         : "42074H1",
  "Amsterdam"              : "42074H2",
  "Tribes Hill"            : "42074H3",
  "Randall"                : "42074H4",
  "Canajoharie"            : "42074H5",
  "Fort Plain"             : "42074H6",
  "Van Hornesville"        : "42074H7",
  "Jordanville"            : "42074H8",
  "Corbett"                : "42075A1",
  "Readburn"               : "42075A2",
  "Cannonsville Reservoir" : "42075A3",
  "Deposit"                : "42075A4",
  "Gulf Summit"            : "42075A5",
  "Windsor"                : "42075A6",
  "Binghamton East"        : "42075A7",
  "Binghamton West"        : "42075A8",
  "Walton East"            : "42075B1",
  "Walton West"            : "42075B2",
  "Trout Creek"            : "42075B3",
  "North Sanford"          : "42075B4",
  "Afton"                  : "42075B5",
  "Belden"                 : "42075B6",
  "Chenango Forks"         : "42075B7",
  "Castle Creek"           : "42075B8",
  "Treadwell"              : "42075C1",
  "Franklin"               : "42075C2",
  "Unadilla"               : "42075C3",
  "Sidney"                 : "42075C4",
  "West Bainbridge"        : "42075C5",
  "Brisben"                : "42075C6",
  "Greene"                 : "42075C7",
  "Whitney Point"          : "42075C8",
  "Oneonta"                : "42075D1",
  "Otego"                  : "42075D2",
  "Gilbertsville"          : "42075D3",
  "Guilford"               : "42075D4",
  "Oxford"                 : "42075D5",
  "Tyner"                  : "42075D6",
  "Smithville Flats"       : "42075D7",
  "Willet"                 : "42075D8",
  "Mount Vision"           : "42075E1",
  "Morris"                 : "42075E2",
  "New Berlin South"       : "42075E3",
  "Holmesville"            : "42075E4",
  "Norwich"                : "42075E5",
  "East Pharsalia"         : "42075E6",
  "Pitcher"                : "42075E7",
  "Cincinnatus"            : "42075E8",
  "Hartwick"               : "42075F1",
  "Edmeston"               : "42075F2",
  "New Berlin North"       : "42075F3",
  "Sherburne"              : "42075F4",
  "Earlville"              : "42075F5",
  "Otselic"                : "42075F6",
  "South Otselic"          : "42075F7",
  "Cuyler"                 : "42075F8",
  "Schuyler Lake"          : "42075G1",
  "Unadilla Forks"         : "42075G2",
  "Brookfield"             : "42075G3",
  "Hubbardsville"          : "42075G4",
  "Hamilton"               : "42075G5",
  "West Eaton"             : "42075G6",
  "Erieville"              : "42075G7",
  "DeRuyter"               : "42075G8",
  "Millers Mills"          : "42075H1",
  "West Winfield"          : "42075H2",
  "Cassville"              : "42075H3",
  "Oriskany Falls"         : "42075H4",
  "Munnsville"             : "42075H5",
  "Morrisville"            : "42075H6",
  "Cazenovia"              : "42075H7",
  "Oran"                   : "42075H8",
  "Endicott"               : "42076A1",
  "Apalachin"              : "42076A2",
  "Owego"                  : "42076A3",
  "Barton"                 : "42076A4",
  "Waverly"                : "42076A5",
  "Wellsburg"              : "42076A6",
  "Elmira"                 : "42076A7",
  "Seeley Creek"           : "42076A8",
  "Maine"                  : "42076B1",
  "Newark Valley"          : "42076B2",
  "Candor"                 : "42076B3",
  "Spencer"                : "42076B4",
  "Van Etten"              : "42076B5",
  "Erin"                   : "42076B6",
  "Horseheads"             : "42076B7",
  "Big Flats"              : "42076B8",
  "Lisle"                  : "42076C1",
  "Richford"               : "42076C2",
  "Speedsville"            : "42076C3",
  "Willseyville"           : "42076C4",
  "West Danby"             : "42076C5",
  "Alpine"                 : "42076C6",
  "Montour Falls"          : "42076C7",
  "Beaver Dams"            : "42076C8",
  "Marathon"               : "42076D1",
  "Harford"                : "42076D2",
  "Dryden"                 : "42076D3",
  "Ithaca East"            : "42076D4",
  "Ithaca West"            : "42076D5",
  "Mecklenburg"            : "42076D6",
  "Burdett"                : "42076D7",
  "Reading Center"         : "42076D8",
  "McGraw"                 : "42076E1",
  "Cortland"               : "42076E2",
  "Groton"                 : "42076E3",
  "West Groton"            : "42076E4",
  "Ludlowville"            : "42076E5",
  "Trumansburg"            : "42076E6",
  "Lodi"                   : "42076E7",
  "Dundee"                 : "42076E8",
  "Truxton"                : "42076F1",
  "Homer"                  : "42076F2",
  "Sempronius"             : "42076F3",
  "Moravia"                : "42076F4",
  "Genoa"                  : "42076F5",
  "Sheldrake"              : "42076F6",
  "Ovid"                   : "42076F7",
  "Dresden"                : "42076F8",
  "Tully"                  : "42076G1",
  "Otisco Valley"          : "42076G2",
  "Spafford"               : "42076G3",
  "Owasco"                 : "42076G4",
  "Scipio Center"          : "42076G5",
  "Union Springs"          : "42076G6",
  "Romulus"                : "42076G7",
  "Geneva South"           : "42076G8",
  "Jamesville"             : "42076H1",
  "South Onondaga"         : "42076H2",
  "Marcellus"              : "42076H3",
  "Skaneateles"            : "42076H4",
  "Auburn"                 : "42076H5",
  "Cayuga"                 : "42076H6",
  "Seneca Falls"           : "42076H7",
  "Geneva North"           : "42076H8",
  "Caton"                  : "42077A1",
  "Addison"                : "42077A2",
  "Borden"                 : "42077A3",
  "Woodhull"               : "42077A4",
  "Troupsburg"             : "42077A5",
  "Rexville"               : "42077A6",
  "Whitesville"            : "42077A7",
  "Wellsville South"       : "42077A8",
  "Corning"                : "42077B1",
  "Campbell"               : "42077B2",
  "Rathbone"               : "42077B3",
  "Cameron"                : "42077B4",
  "South Canisteo"         : "42077B5",
  "Greenwood"              : "42077B6",
  "Andover"                : "42077B7",
  "Wellsville North"       : "42077B8",
  "Bradford"               : "42077C1",
  "Savona"                 : "42077C2",
  "Bath"                   : "42077C3",
  "Towlesville"            : "42077C4",
  "Canisteo"               : "42077C5",
  "Hornell"                : "42077C6",
  "Alfred"                 : "42077C7",
  "West Almond"            : "42077C8",
  "Wayne"                  : "42077D1",
  "Hammondsport"           : "42077D2",
  "Rheims"                 : "42077D3",
  "Avoca"                  : "42077D4",
  "Haskinville"            : "42077D5",
  "Arkport"                : "42077D6",
  "Canaseraga"             : "42077D7",
  "Birdsall"               : "42077D8",
  "Keuka Park"             : "42077E1",
  "Pulteney"               : "42077E2",
  "Prattsburg"             : "42077E3",
  "Naples"                 : "42077E4",
  "Wayland"                : "42077E5",
  "Dansville"              : "42077E6",
  "Ossian"                 : "42077E7",
  "Nunda"                  : "42077E8",
  "Penn Yan"               : "42077F1",
  "Potter"                 : "42077F2",
  "Middlesex"              : "42077F3",
  "Bristol Springs"        : "42077F4",
  "Springwater"            : "42077F5",
  "Conesus"                : "42077F6",
  "Sonyea"                 : "42077F7",
  "Mount Morris"           : "42077F8",
  "Stanley"                : "42077G1",
  "Rushville"              : "42077G2",
  "Canandaigua Lake"       : "42077G3",
  "Bristol Center"         : "42077G4",
  "Honeoye"                : "42077G5",
  "Livonia"                : "42077G6",
  "Geneseo"                : "42077G7",
  "Leicester"              : "42077G8",
  "Phelps"                 : "42077H1",
  "Clifton Springs"        : "42077H2",
  "Canandaigua"            : "42077H3",
  "Victor"                 : "42077H4",
  "Honeoye Falls"          : "42077H5",
  "Rush"                   : "42077H6",
  "Caledonia"              : "42077H7",
  "Le Roy"                 : "42077H8",
  "Allentown"              : "42078A1",
  "Bolivar"                : "42078A2",
  "Portville"              : "42078A3",
  "Olean"                  : "42078A4",
  "Knapp Creek"            : "42078A5",
  "Limestone"              : "42078A6",
  "Red House"              : "42078A7",
  "Steamburg"              : "42078A8",
  "Belmont"                : "42078B1",
  "Friendship"             : "42078B2",
  "Cuba"                   : "42078B3",
  "Hinsdale"               : "42078B4",
  "Humphrey"               : "42078B5",
  "Salamanca"              : "42078B6",
  "Little Valley"          : "42078B7",
  "Randolph"               : "42078B8",
  "Angelica"               : "42078C1",
  "Black Creek"            : "42078C2",
  "Rawson"                 : "42078C3",
  "Franklinville"          : "42078C4",
  "Ashford"                : "42078C5",
  "Ellicottville"          : "42078C6",
  "Cattaraugus"            : "42078C7",
  "New Albion"             : "42078C8",
  "Fillmore"               : "42078D1",
  "Houghton"               : "42078D2",
  "Freedom"                : "42078D3",
  "Delevan"                : "42078D4",
  "West Valley"            : "42078D5",
  "Ashford Hollow"         : "42078D6",
  "Collins Center"         : "42078D7",
  "Gowanda"                : "42078D8",
  "Portageville"           : "42078E1",
  "Pike"                   : "42078E2",
  "Bliss"                  : "42078E3",
  "Arcade"                 : "42078E4",
  "Sardinia"               : "42078E5",
  "Springville"            : "42078E6",
  "Langford"               : "42078E7",
  "North Collins"          : "42078E8",
  "Castile"                : "42078F1",
  "Warsaw"                 : "42078F2",
  "Johnsonburg"            : "42078F3",
  "Strykersville"          : "42078F4",
  "Holland"                : "42078F5",
  "Colden"                 : "42078F6",
  "Hamburg"                : "42078F7",
  "Eden"                   : "42078F8",
  "Wyoming"                : "42078G1",
  "Dale"                   : "42078G2",
  "Attica"                 : "42078G3",
  "Cowlesville"            : "42078G4",
  "East Aurora"            : "42078G5",
  "Orchard Park"           : "42078G6",
  "Buffalo SE"             : "42078G7",
  "Stafford"               : "42078H1",
  "Batavia South"          : "42078H2",
  "Alexander"              : "42078H3",
  "Corfu"                  : "42078H4",
  "Clarence"               : "42078H5",
  "Lancaster"              : "42078H6",
  "Buffalo NE"             : "42078H7",
  "Buffalo NW"             : "42078H8",
  "Ivory"                  : "42079A1",
  "Jamestown"              : "42079A2",
  "Lakewood"               : "42079A3",
  "Panama"                 : "42079A4",
  "North Clymer"           : "42079A5",
  "Clymer"                 : "42079A6",
  "Kennedy"                : "42079B1",
  "Gerry"                  : "42079B2",
  "Ellery Center"          : "42079B3",
  "Chautauqua"             : "42079B4",
  "Sherman"                : "42079B5",
  "South Ripley"           : "42079B6",
  "Cherry Creek"           : "42079C1",
  "Hamlet"                 : "42079C2",
  "Cassadaga"              : "42079C3",
  "Hartfield"              : "42079C4",
  "Westfield"              : "42079C5",
  "Ripley"                 : "42079C6",
  "Perrysburg"             : "42079D1",
  "Forestville"            : "42079D2",
  "Dunkirk"                : "42079D3",
  "Brocton"                : "42079D4",
  "Farnham"                : "42079E1",
  "Silver Creek"           : "42079E2",
  "Angola"                 : "42079F1",
  "Shushan"                : "43073A3",
  "Cambridge"              : "43073A4",
  "Schuylerville"          : "43073A5",
  "Quaker Springs"         : "43073A6",
  "Saratoga Springs"       : "43073A7",
  "Middle Grove"           : "43073A8",
  "Salem"                  : "43073B3",
  "Cossayuna"              : "43073B4",
  "Fort Miller"            : "43073B5",
  "Gansevoort"             : "43073B6",
  "Corinth"                : "43073B7",
  "Porter Corners"         : "43073B8",
  "West Pawlet"            : "43073C3",
  "Hartford"               : "43073C4",
  "Hudson Falls"           : "43073C5",
  "Glens Falls"            : "43073C6",
  "Lake Luzerne"           : "43073C7",
  "Conklingville"          : "43073C8",
  "Granville"              : "43073D3",
  "Fort Ann"               : "43073D4",
  "Putnam Mountain"        : "43073D5",
  "Lake George"            : "43073D6",
  "Warrensburg"            : "43073D7",
  "Stony Creek"            : "43073D8",
  "Thorn Hill"             : "43073E3",
  "Whitehall"              : "43073E4",
  "Shelving Rock"          : "43073E5",
  "Bolton Landing"         : "43073E6",
  "The Glen"               : "43073E7",
  "Johnsburg"              : "43073E8",
  "Putnam"                 : "43073F4",
  "Silver Bay"             : "43073F5",
  "Brant Lake"             : "43073F6",
  "Chestertown"            : "43073F7",
  "North Creek"            : "43073F8",
  "Ticonderoga"            : "43073G4",
  "Graphite"               : "43073G5",
  "Pharaoh Mountain"       : "43073G6",
  "Schroon Lake"           : "43073G7",
  "Minerva"                : "43073G8",
  "Crown Point"            : "43073H4",
  "Eagle Lake"             : "43073H5",
  "Paradox Lake"           : "43073H6",
  "Blue Ridge"             : "43073H7",
  "Cheney Pond"            : "43073H8",
  "Galway"                 : "43074A1",
  "Broadalbin"             : "43074A2",
  "Gloversville"           : "43074A3",
  "Peck Lake"              : "43074A4",
  "Lassellsville"          : "43074A5",
  "Oppenheim"              : "43074A6",
  "Little Falls"           : "43074A7",
  "Herkimer"               : "43074A8",
  "Edinburg"               : "43074B1",
  "Northville"             : "43074B2",
  "Jackson Summit"         : "43074B3",
  "Caroga Lake"            : "43074B4",
  "Canada Lake"            : "43074B5",
  "Stratford"              : "43074B6",
  "Salisbury"              : "43074B7",
  "Middleville"            : "43074B8",
  "Ohmer Mountain"         : "43074C1",
  "Hope Falls"             : "43074C2",
  "Cathead Mountain"       : "43074C3",
  "Whitehouse"             : "43074C4",
  "Tomany Mountain"        : "43074C5",
  "Morehouse Lake"         : "43074C6",
  "Jerseyfield Lake"       : "43074C7",
  "Ohio"                   : "43074C8",
  "Harrisburg"             : "43074D1",
  "Griffin"                : "43074D2",
  "Wells"                  : "43074D3",
  "Lake Pleasant"          : "43074D4",
  "Piseco Lake"            : "43074D5",
  "Hoffmeister"            : "43074D6",
  "Morehouseville"         : "43074D7",
  "Black Creek Lake"       : "43074D8",
  "Bakers Mills"           : "43074E1",
  "South Pond Mountain"    : "43074E2",
  "Kunjamuk River"         : "43074E3",
  "Page Mountain"          : "43074E4",
  "Spruce Lake"            : "43074E5",
  "Spruce Lake Mountain"   : "43074E6",
  "Honnedaga Lake"         : "43074E7",
  "Bisby Lakes"            : "43074E8",
  "Gore Mountain"          : "43074F1",
  "Bullhead Mountain"      : "43074F2",
  "Indian Lake"            : "43074F3",
  "Snowy Mountain"         : "43074F4",
  "Wakely Mountain"        : "43074F5",
  "Mount Tom"              : "43074F6",
  "Limekiln Lake"          : "43074F7",
  "Old Forge"              : "43074F8",
  "Dutton Mountain"        : "43074G1",
  "Bad Luck Mountain"      : "43074G2",
  "Rock Lake"              : "43074G3",
  "Blue Mountain Lake"     : "43074G4",
  "Sargent Ponds"          : "43074G5",
  "Raquette Lake"          : "43074G6",
  "Eagle Bay"              : "43074G7",
  "Big Moose"              : "43074G8",
  "Vanderwhacker Mountain" : "43074H1",
  "Newcomb"                : "43074H2",
  "Dun Brook Mountain"     : "43074H3",
  "Deerland"               : "43074H4",
  "Forked Lake"            : "43074H5",
  "Brandreth Lake"         : "43074H6",
  "Nehasane Lake"          : "43074H7",
  "Beaver River"           : "43074H8",
  "Ilion"                  : "43075A1",
  "Utica East"             : "43075A2",
  "Utica West"             : "43075A3",
  "Clinton"                : "43075A4",
  "Vernon"                 : "43075A5",
  "Oneida"                 : "43075A6",
  "Canastota"              : "43075A7",
  "Manlius"                : "43075A8",
  "Newport"                : "43075B1",
  "South Trenton"          : "43075B2",
  "Oriskany"               : "43075B3",
  "Rome"                   : "43075B4",
  "Verona"                 : "43075B5",
  "Sylvan Beach"           : "43075B6",
  "Jewell"                 : "43075B7",
  "Cleveland"              : "43075B8",
  "Hinckley"               : "43075C1",
  "Remsen"                 : "43075C2",
  "North Western"          : "43075C3",
  "Westernville"           : "43075C4",
  "Lee Center"             : "43075C5",
  "Camden East"            : "43075C6",
  "Camden West"            : "43075C7",
  "Panther Lake"           : "43075C8",
  "North Wilmurt"          : "43075D1",
  "Forestport"             : "43075D2",
  "Boonville"              : "43075D3",
  "West Leyden"            : "43075D4",
  "Point Rock"             : "43075D5",
  "Florence"               : "43075D6",
  "Westdale"               : "43075D7",
  "Williamstown"           : "43075D8",
  "McKeever"               : "43075E1",
  "Woodgate"               : "43075E2",
  "Port Leyden"            : "43075E3",
  "Constableville"         : "43075E4",
  "High Market"            : "43075E5",
  "North Osceola"          : "43075E6",
  "Redfield"               : "43075E7",
  "Orwell"                 : "43075E8",
  "Thendara"               : "43075F1",
  "Copper Lake"            : "43075F2",
  "Brantingham"            : "43075F3",
  "Glenfield"              : "43075F4",
  "Page"                   : "43075F5",
  "Sears Pond"             : "43075F6",
  "Worth Center"           : "43075F7",
  "Boylston Center"        : "43075F8",
  "Stillwater Mountain"    : "43075G1",
  "Number Four"            : "43075G2",
  "Crystal Dale"           : "43075G3",
  "Lowville"               : "43075G4",
  "West Lowville"          : "43075G5",
  "New Boston"             : "43075G6",
  "Barnes Corners"         : "43075G7",
  "Rodman"                 : "43075G8",
  "Stillwater"             : "43075H1",
  "Soft Maple Reservoir"   : "43075H2",
  "Belfort"                : "43075H3",
  "Croghan"                : "43075H4",
  "Carthage"               : "43075H5",
  "Copenhagen"             : "43075H6",
  "Rutland Center"         : "43075H7",
  "Watertown"              : "43075H8",
  "Syracuse East"          : "43076A1",
  "Syracuse West"          : "43076A2",
  "Camillus"               : "43076A3",
  "Jordan"                 : "43076A4",
  "Weedsport"              : "43076A5",
  "Montezuma"              : "43076A6",
  "Savannah"               : "43076A7",
  "Lyons"                  : "43076A8",
  "Cicero"                 : "43076B1",
  "Brewerton"              : "43076B2",
  "Baldwinsville"          : "43076B3",
  "Lysander"               : "43076B4",
  "Cato"                   : "43076B5",
  "Victory"                : "43076B6",
  "Wolcott"                : "43076B7",
  "Rose"                   : "43076B8",
  "Mallory"                : "43076C1",
  "Central Square"         : "43076C2",
  "Pennellville"           : "43076C3",
  "Fulton"                 : "43076C4",
  "Hannibal"               : "43076C5",
  "Fair Haven"             : "43076C6",
  "North Wolcott"          : "43076C7",
  "Dugway"                 : "43076D1",
  "Mexico"                 : "43076D2",
  "New Haven"              : "43076D3",
  "Oswego East"            : "43076D4",
  "Oswego West"            : "43076D5",
  "Richland"               : "43076E1",
  "Pulaski"                : "43076E2",
  "Sandy Creek"            : "43076F1",
  "Ellisburg"              : "43076F2",
  "Adams"                  : "43076G1",
  "Henderson"              : "43076G2",
  "Sackets Harbor"         : "43076H1",
  "Henderson Bay"          : "43076H2",
  "Newark"                 : "43077A1",
  "Palmyra"                : "43077A2",
  "Macedon"                : "43077A3",
  "Fairport"               : "43077A4",
  "Pittsford"              : "43077A5",
  "West Henrietta"         : "43077A6",
  "Clifton"                : "43077A7",
  "Churchville"            : "43077A8",
  "Sodus"                  : "43077B1",
  "Williamson"             : "43077B2",
  "Ontario"                : "43077B3",
  "Webster"                : "43077B4",
  "Rochester East"         : "43077B5",
  "Rochester West"         : "43077B6",
  "Spencerport"            : "43077B7",
  "Brockport"              : "43077B8",
  "Hilton"                 : "43077C7",
  "Hamlin"                 : "43077C8",
  "Byron"                  : "43078A1",
  "Batavia North"          : "43078A2",
  "Oakfield"               : "43078A3",
  "Akron"                  : "43078A4",
  "Wolcottsville"          : "43078A5",
  "Clarence Center"        : "43078A6",
  "Tonawanda East"         : "43078A7",
  "Tonawanda West"         : "43078A8",
  "Holley"                 : "43078B1",
  "Albion"                 : "43078B2",
  "Knowlesville"           : "43078B3",
  "Medina"                 : "43078B4",
  "Gasport"                : "43078B5",
  "Lockport"               : "43078B6",
  "Cambria"                : "43078B7",
  "Ransomville"            : "43078B8",
  "Kendall"                : "43078C1",
  "Kent"                   : "43078C2",
  "Ashwood"                : "43078C3",
  "Lyndonville"            : "43078C4",
  "Barker"                 : "43078C5",
  "Newfane"                : "43078C6",
  "Wilson"                 : "43078C7",
  "Lewiston"               : "43079B1",
  "Port Henry"             : "44073A4",
  "Witherbee"              : "44073A5",
  "Underwood"              : "44073A6",
  "Dix Mountain"           : "44073A7",
  "Mount Marcy"            : "44073A8",
  "Vergennes West"         : "44073B3",
  "Westport"               : "44073B4",
  "Elizabethtown"          : "44073B5",
  "Rocky Peak Ridge"       : "44073B6",
  "Keene Valley"           : "44073B7",
  "North Elba"             : "44073B8",
  "Charlotte"              : "44073C3",
  "Willsboro"              : "44073C4",
  "Lewis"                  : "44073C5",
  "Jay Mountain"           : "44073C6",
  "Keene"                  : "44073C7",
  "Lake Placid"            : "44073C8",
  "Port Douglass"          : "44073D4",
  "Clintonville"           : "44073D5",
  "Au Sable Forks"         : "44073D6",
  "Wilmington"             : "44073D7",
  "Franklin Falls"         : "44073D8",
  "Keeseville"             : "44073E4",
  "Peru"                   : "44073E5",
  "Peasleeville"           : "44073E6",
  "Redford"                : "44073E7",
  "Alder Brook"            : "44073E8",
  "Plattsburgh"            : "44073F4",
  "Morrisonville"          : "44073F5",
  "Dannemora"              : "44073F6",
  "Moffitsville"           : "44073F7",
  "Lyon Mountain"          : "44073F8",
  "Beekmantown"            : "44073G4",
  "West Chazy"             : "44073G5",
  "Jericho"                : "44073G6",
  "Ellenburg Mountain"     : "44073G7",
  "Ellenburg Center"       : "44073G8",
  "Rouses Point"           : "44073H3",
  "Champlain"              : "44073H4",
  "Mooers"                 : "44073H5",
  "Altona"                 : "44073H6",
  "Ellenburg Depot"        : "44073H7",
  "Churubusco"             : "44073H8",
  "Mount Adams"            : "44074A1",
  "Santanoni Peak"         : "44074A2",
  "Kempshall Mountain"     : "44074A3",
  "Grampus Lake"           : "44074A4",
  "Little Tupper Lake"     : "44074A5",
  "Sabattis"               : "44074A6",
  "Wolf Mountain"          : "44074A7",
  "Five Ponds"             : "44074A8",
  "Street Mountain"        : "44074B1",
  "Ampersand Lake"         : "44074B2",
  "Stony Creek Mountain"   : "44074B3",
  "Tupper Lake"            : "44074B4",
  "Piercefield"            : "44074B5",
  "Long Tom Mountain"      : "44074B6",
  "Cranberry Lake"         : "44074B7",
  "Newton Falls"           : "44074B8",
  "McKenzie Mountain"      : "44074C1",
  "Saranac Lake"           : "44074C2",
  "Upper Saranac Lake"     : "44074C3",
  "Derrick"                : "44074C4",
  "Mount Matumbla"         : "44074C5",
  "Childwold"              : "44074C6",
  "Brother Ponds"          : "44074C7",
  "Tooley Pond"            : "44074C8",
  "Bloomingdale"           : "44074D1",
  "Gabriels"               : "44074D2",
  "Saint Regis Mountain"   : "44074D3",
  "Bay Pond"               : "44074D4",
  "Augerhole Falls"        : "44074D5",
  "Carry Falls Reservoir"  : "44074D6",
  "Stark"                  : "44074D7",
  "Albert Marsh"           : "44074D8",
  "Loon Lake"              : "44074E1",
  "Debar Mountain"         : "44074E2",
  "Meacham Lake"           : "44074E3",
  "Meno"                   : "44074E4",
  "Lake Ozonia"            : "44074E5",
  "Sylvan Falls"           : "44074E6",
  "Rainbow Falls"          : "44074E7",
  "Colton"                 : "44074E8",
  "Ragged Lake"            : "44074F1",
  "Owls Head"              : "44074F2",
  "Lake Titus"             : "44074F3",
  "Santa Clara"            : "44074F4",
  "Saint Regis Falls"      : "44074F5",
  "Nicholville"            : "44074F6",
  "Parishville"            : "44074F7",
  "Potsdam"                : "44074F8",
  "Brainardsville"         : "44074G1",
  "Chasm Falls"            : "44074G2",
  "Malone"                 : "44074G3",
  "Bangor"                 : "44074G4",
  "Brushton"               : "44074G5",
  "North Lawrence"         : "44074G6",
  "Brasher Falls"          : "44074G7",
  "Norfolk"                : "44074G8",
  "Chateaugay"             : "44074H1",
  "Burke"                  : "44074H2",
  "Constable"              : "44074H3",
  "Fort Covington"         : "44074H4",
  "Bombay"                 : "44074H5",
  "Hogansburg"             : "44074H6",
  "Raquette River"         : "44074H7",
  "Massena"                : "44074H8",
  "Oswegatchie SE"         : "44075A1",
  "Oswegatchie SW"         : "44075A2",
  "Remington Corners"      : "44075A3",
  "Natural Bridge"         : "44075A4",
  "North Wilna"            : "44075A5",
  "Deferiet"               : "44075A6",
  "Black River"            : "44075A7",
  "Brownville"             : "44075A8",
  "Oswegatchie"            : "44075B1",
  "Fine"                   : "44075B2",
  "Harrisville"            : "44075B3",
  "Lake Bonaparte"         : "44075B4",
  "Antwerp"                : "44075B5",
  "Philadelphia"           : "44075B6",
  "Theresa"                : "44075B7",
  "La Fargeville"          : "44075B8",
  "Degrasse"               : "44075C1",
  "South Edwards"          : "44075C2",
  "Edwards"                : "44075C3",
  "Gouverneur"             : "44075C4",
  "Natural Dam"            : "44075C5",
  "Muskellunge Lake"       : "44075C6",
  "Redwood"                : "44075C7",
  "Alexandria Bay"         : "44075C8",
  "West Pierrepont"        : "44075D1",
  "Hermon"                 : "44075D2",
  "Bigelow"                : "44075D3",
  "Richville"              : "44075D4",
  "Pope Mills"             : "44075D5",
  "Hammond"                : "44075D6",
  "Chippewa Bay"           : "44075D7",
  "Pierrepont"             : "44075E1",
  "Canton"                 : "44075E2",
  "Rensselaer Falls"       : "44075E3",
  "Heuvelton"              : "44075E4",
  "Edwardsville"           : "44075E5",
  "Morristown"             : "44075E6",
  "West Potsdam"           : "44075F1",
  "Morley"                 : "44075F2",
  "Lisbon"                 : "44075F3",
  "Ogdensburg East"        : "44075F4",
  "Ogdensburg West"        : "44075F5",
  "Chase Mills"            : "44075G1",
  "Waddington"             : "44075G2",
  "Sparrowhawk Point"      : "44075G3",
  "Louisville"             : "44075H1",
  "Dexter"                 : "44076A1",
  "Chaumont"               : "44076A2",
  "Cape Vincent South"     : "44076A3",
  "Clayton"                : "44076B1",
  "Saint Lawrence"         : "44076B2",
  "Cape Vincent North"     : "44076B3",
  "Thousand Island Park"   : "44076C1",
}

# WNY/CNY NE to Copper Lake and SE to Readburn
# (incl Oswego County down to Broome County, most of Oneida County)
#
#  Honeoye_NW: Livingston/Ontario (5:1)
#
#  Geneva North_NW: Ontario/Seneca (60-40)
#  Geneva South_NW: Ontario/Seneca (33/66), most of Seneca is on lake
#
#  Manlius_NW: Onondaga/Madison (50-50)
#  Manlius_CE: Onondaga/Madison (33/66)
#  Oran_CE: Onondaga/Madison (45/55)
#  Camden West_NW: Oswego/Oneida (5%/95%)
#
#  Ellisburg_CE: Jefferson/Oswego (3:1)
#  Sandy Creek_CE: Jefferson/Oswego (70/30)
WNYCNY_URLID_TO_MAINCOUNTY = {
  "42075A2CE": "Delaware",
  "42075A2NW": "Delaware",
  "42075A3CE": "Delaware",
  "42075A3NW": "Delaware",
  "42075A4CE": "Delaware",
  "42075A4NW": "Broome",
  "42075A5CE": "Broome",
  "42075A5NW": "Broome",
  "42075A6CE": "Broome",
  "42075A6NW": "Broome",
  "42075A7CE": "Broome",
  "42075A7NW": "Broome",
  "42075A8CE": "Broome",
  "42075A8NW": "Broome",
  "42075B2CE": "Delaware",
  "42075B2NW": "Delaware",
  "42075B3CE": "Delaware",
  "42075B3NW": "Delaware",
  "42075B4CE": "Delaware",
  "42075B4NW": "Chenango",
  "42075B5CE": "Broome",
  "42075B5NW": "Chenango",
  "42075B6CE": "Broome",
  "42075B6NW": "Broome",
  "42075B7CE": "Broome",
  "42075B7NW": "Broome",
  "42075B8CE": "Broome",
  "42075B8NW": "Broome",
  "42075C2CE": "Delaware",
  "42075C2NW": "Delaware",
  "42075C3CE": "Delaware",
  "42075C3NW": "Otsego",
  "42075C4CE": "Delaware",
  "42075C4NW": "Chenango",
  "42075C5CE": "Chenango",
  "42075C5NW": "Chenango",
  "42075C6CE": "Chenango",
  "42075C6NW": "Chenango",
  "42075C7CE": "Chenango",
  "42075C7NW": "Chenango",
  "42075C8CE": "Broome",
  "42075C8NW": "Broome",
  "42075D2CE": "Otsego",
  "42075D2NW": "Otsego",
  "42075D3CE": "Otsego",
  "42075D3NW": "Otsego",
  "42075D4CE": "Chenango",
  "42075D4NW": "Chenango",
  "42075D5CE": "Chenango",
  "42075D5NW": "Chenango",
  "42075D6CE": "Chenango",
  "42075D6NW": "Chenango",
  "42075D7CE": "Chenango",
  "42075D7NW": "Chenango",
  "42075D8CE": "Cortland",
  "42075D8NW": "Cortland",
  "42075E2CE": "Otsego",
  "42075E2NW": "Otsego",
  "42075E3CE": "Otsego",
  "42075E3NW": "Chenango",
  "42075E4CE": "Chenango",
  "42075E4NW": "Chenango",
  "42075E5CE": "Chenango",
  "42075E5NW": "Chenango",
  "42075E6CE": "Chenango",
  "42075E6NW": "Chenango",
  "42075E7CE": "Chenango",
  "42075E7NW": "Chenango",
  "42075E8CE": "Cortland",
  "42075E8NW": "Cortland",
  "42075F2CE": "Otsego",
  "42075F2NW": "Otsego",
  "42075F3CE": "Otsego",
  "42075F3NW": "Chenango",
  "42075F4CE": "Chenango",
  "42075F4NW": "Chenango",
  "42075F5CE": "Chenango",
  "42075F5NW": "Chenango",
  "42075F6CE": "Chenango",
  "42075F6NW": "Chenango",
  "42075F7CE": "Chenango",
  "42075F7NW": "Madison",
  "42075F8CE": "Cortland",
  "42075F8NW": "Cortland",
  "42075G2CE": "Otsego",
  "42075G2NW": "Otsego",
  "42075G3CE": "Madison",
  "42075G3NW": "Madison",
  "42075G4CE": "Madison",
  "42075G4NW": "Madison",
  "42075G5CE": "Madison",
  "42075G5NW": "Madison",
  "42075G6CE": "Madison",
  "42075G6NW": "Madison",
  "42075G7CE": "Madison",
  "42075G7NW": "Madison",
  "42075G8CE": "Onondaga",
  "42075G8NW": "Onondaga",
  "42075H2CE": "Herkimer",
  "42075H2NW": "Oneida",
  "42075H3CE": "Oneida",
  "42075H3NW": "Oneida",
  "42075H4CE": "Oneida",
  "42075H4NW": "Oneida",
  "42075H5CE": "Oneida",
  "42075H5NW": "Madison",
  "42075H6CE": "Madison",
  "42075H6NW": "Madison",
  "42075H7CE": "Madison",
  "42075H7NW": "Madison",
  "42075H8CE": "Madison",
  "42075H8NW": "Onondaga",
  "42076A1CE": "Broome",
  "42076A1NW": "Broome",
  "42076A2CE": "Tioga",
  "42076A2NW": "Tioga",
  "42076A3CE": "Tioga",
  "42076A3NW": "Tioga",
  "42076A4CE": "Tioga",
  "42076A4NW": "Tioga",
  "42076A5CE": "Tioga",
  "42076A5NW": "Chemung",
  "42076A6CE": "Chemung",
  "42076A6NW": "Chemung",
  "42076A7CE": "Chemung",
  "42076A7NW": "Chemung",
  "42076A8CE": "Chemung",
  "42076A8NW": "Steuben",
  "42076B1CE": "Broome",
  "42076B1NW": "Tioga",
  "42076B2CE": "Tioga",
  "42076B2NW": "Tioga",
  "42076B3CE": "Tioga",
  "42076B3NW": "Tioga",
  "42076B4CE": "Tioga",
  "42076B4NW": "Tioga",
  "42076B5CE": "Tioga",
  "42076B5NW": "Chemung",
  "42076B6CE": "Chemung",
  "42076B6NW": "Chemung",
  "42076B7CE": "Chemung",
  "42076B7NW": "Chemung",
  "42076B8CE": "Chemung",
  "42076B8NW": "Steuben",
  "42076C1CE": "Broome",
  "42076C1NW": "Broome",
  "42076C2CE": "Tioga",
  "42076C2NW": "Tioga",
  "42076C3CE": "Tompkins",
  "42076C3NW": "Tompkins",
  "42076C4CE": "Tioga",
  "42076C4NW": "Tompkins",
  "42076C5CE": "Tompkins",
  "42076C5NW": "Tompkins",
  "42076C6CE": "Tompkins",
  "42076C6NW": "Schuyler",
  "42076C7CE": "Schuyler",
  "42076C7NW": "Schuyler",
  "42076C8CE": "Schuyler",
  "42076C8NW": "Schuyler",
  "42076D1CE": "Cortland",
  "42076D1NW": "Cortland",
  "42076D2CE": "Cortland",
  "42076D2NW": "Cortland",
  "42076D3CE": "Tompkins",
  "42076D3NW": "Tompkins",
  "42076D4CE": "Tompkins",
  "42076D4NW": "Tompkins",
  "42076D5CE": "Tompkins",
  "42076D5NW": "Tompkins",
  "42076D6CE": "Tompkins",
  "42076D6NW": "Schuyler",
  "42076D7CE": "Schuyler",
  "42076D7NW": "Schuyler",
  "42076D8CE": "Schuyler",
  "42076D8NW": "Yates",
  "42076E1CE": "Cortland",
  "42076E1NW": "Cortland",
  "42076E2CE": "Cortland",
  "42076E2NW": "Cortland",
  "42076E3CE": "Tompkins",
  "42076E3NW": "Tompkins",
  "42076E4CE": "Tompkins",
  "42076E4NW": "Tompkins",
  "42076E5CE": "Tompkins",
  "42076E5NW": "Tompkins",
  "42076E6CE": "Seneca",
  "42076E6NW": "Seneca",
  "42076E7CE": "Seneca",
  "42076E7NW": "Seneca",
  "42076E8CE": "Yates",
  "42076E8NW": "Yates",
  "42076F1CE": "Cortland",
  "42076F1NW": "Cortland",
  "42076F2CE": "Cortland",
  "42076F2NW": "Cortland",
  "42076F3CE": "Cayuga",
  "42076F3NW": "Cayuga",
  "42076F4CE": "Cayuga",
  "42076F4NW": "Cayuga",
  "42076F5CE": "Cayuga",
  "42076F5NW": "Cayuga",
  "42076F6CE": "Cayuga",
  "42076F6NW": "Cayuga",
  "42076F7CE": "Seneca",
  "42076F7NW": "Seneca",
  "42076F8CE": "Seneca",
  "42076F8NW": "Yates",
  "42076G1CE": "Onondaga",
  "42076G1NW": "Onondaga",
  "42076G2CE": "Onondaga",
  "42076G2NW": "Onondaga",
  "42076G3CE": "Onondaga",
  "42076G3NW": "Onondaga",
  "42076G4CE": "Cayuga",
  "42076G4NW": "Cayuga",
  "42076G5CE": "Cayuga",
  "42076G5NW": "Cayuga",
  "42076G6CE": "Cayuga",
  "42076G6NW": "Cayuga",
  "42076G7CE": "Seneca",
  "42076G7NW": "Seneca",
  "42076G8CE": "Seneca",
  "42076G8NW": "Seneca",
  "42076H1CE": "Onondaga",
  "42076H1NW": "Onondaga",
  "42076H2CE": "Onondaga",
  "42076H2NW": "Onondaga",
  "42076H3CE": "Onondaga",
  "42076H3NW": "Onondaga",
  "42076H4CE": "Onondaga",
  "42076H4NW": "Cayuga",
  "42076H5CE": "Cayuga",
  "42076H5NW": "Cayuga",
  "42076H6CE": "Cayuga",
  "42076H6NW": "Cayuga",
  "42076H7CE": "Seneca",
  "42076H7NW": "Seneca",
  "42076H8CE": "Seneca",
  "42076H8NW": "Ontario",
  "42077A1CE": "Steuben",
  "42077A1NW": "Steuben",
  "42077A2CE": "Steuben",
  "42077A2NW": "Steuben",
  "42077A3CE": "Steuben",
  "42077A3NW": "Steuben",
  "42077A4CE": "Steuben",
  "42077A4NW": "Steuben",
  "42077A5CE": "Steuben",
  "42077A5NW": "Steuben",
  "42077A6CE": "Steuben",
  "42077A6NW": "Steuben",
  "42077A7CE": "Allegany",
  "42077A7NW": "Allegany",
  "42077A8CE": "Allegany",
  "42077A8NW": "Allegany",
  "42077B1CE": "Steuben",
  "42077B1NW": "Steuben",
  "42077B2CE": "Steuben",
  "42077B2NW": "Steuben",
  "42077B3CE": "Steuben",
  "42077B3NW": "Steuben",
  "42077B4CE": "Steuben",
  "42077B4NW": "Steuben",
  "42077B5CE": "Steuben",
  "42077B5NW": "Steuben",
  "42077B6CE": "Steuben",
  "42077B6NW": "Steuben",
  "42077B7CE": "Allegany",
  "42077B7NW": "Allegany",
  "42077B8CE": "Allegany",
  "42077B8NW": "Allegany",
  "42077C1CE": "Schuyler",
  "42077C1NW": "Schuyler",
  "42077C2CE": "Steuben",
  "42077C2NW": "Steuben",
  "42077C3CE": "Steuben",
  "42077C3NW": "Steuben",
  "42077C4CE": "Steuben",
  "42077C4NW": "Steuben",
  "42077C5CE": "Steuben",
  "42077C5NW": "Steuben",
  "42077C6CE": "Steuben",
  "42077C6NW": "Steuben",
  "42077C7CE": "Allegany",
  "42077C7NW": "Allegany",
  "42077C8CE": "Allegany",
  "42077C8NW": "Allegany",
  "42077D1CE": "Schuyler",
  "42077D1NW": "Schuyler",
  "42077D2CE": "Steuben",
  "42077D2NW": "Steuben",
  "42077D3CE": "Steuben",
  "42077D3NW": "Steuben",
  "42077D4CE": "Steuben",
  "42077D4NW": "Steuben",
  "42077D5CE": "Steuben",
  "42077D5NW": "Steuben",
  "42077D6CE": "Steuben",
  "42077D6NW": "Steuben",
  "42077D7CE": "Allegany",
  "42077D7NW": "Allegany",
  "42077D8CE": "Allegany",
  "42077D8NW": "Allegany",
  "42077E1CE": "Yates",
  "42077E1NW": "Yates",
  "42077E2CE": "Steuben",
  "42077E2NW": "Yates",
  "42077E3CE": "Steuben",
  "42077E3NW": "Yates",
  "42077E4CE": "Steuben",
  "42077E4NW": "Ontario",
  "42077E5CE": "Steuben",
  "42077E5NW": "Livingston",
  "42077E6CE": "Steuben",
  "42077E6NW": "Livingston",
  "42077E7CE": "Livingston",
  "42077E7NW": "Livingston",
  "42077E8CE": "Livingston",
  "42077E8NW": "Livingston",
  "42077F1CE": "Yates",
  "42077F1NW": "Yates",
  "42077F2CE": "Yates",
  "42077F2NW": "Yates",
  "42077F3CE": "Yates",
  "42077F3NW": "Ontario",
  "42077F4CE": "Ontario",
  "42077F4NW": "Ontario",
  "42077F5CE": "Ontario",
  "42077F5NW": "Ontario",
  "42077F6CE": "Livingston",
  "42077F6NW": "Livingston",
  "42077F7CE": "Livingston",
  "42077F7NW": "Livingston",
  "42077F8CE": "Livingston",
  "42077F8NW": "Wyoming",
  "42077G1CE": "Ontario",
  "42077G1NW": "Ontario",
  "42077G2CE": "Ontario",
  "42077G2NW": "Ontario",
  "42077G3CE": "Ontario",
  "42077G3NW": "Ontario",
  "42077G4CE": "Ontario",
  "42077G4NW": "Ontario",
  "42077G5CE": "Ontario",
  "42077G5NW": "Livingston",
  "42077G6CE": "Livingston",
  "42077G6NW": "Livingston",
  "42077G7CE": "Livingston",
  "42077G7NW": "Livingston",
  "42077G8CE": "Livingston",
  "42077G8NW": "Wyoming",
  "42077H1CE": "Ontario",
  "42077H1NW": "Ontario",
  "42077H2CE": "Ontario",
  "42077H2NW": "Ontario",
  "42077H3CE": "Ontario",
  "42077H3NW": "Ontario",
  "42077H4CE": "Ontario",
  "42077H4NW": "Ontario",
  "42077H5CE": "Ontario",
  "42077H5NW": "Monroe",
  "42077H6CE": "Livingston",
  "42077H6NW": "Monroe",
  "42077H7CE": "Livingston",
  "42077H7NW": "Livingston",
  "42077H8CE": "Livingston",
  "42077H8NW": "Genesee",
  "42078A1CE": "Allegany",
  "42078A1NW": "Allegany",
  "42078A2CE": "Allegany",
  "42078A2NW": "Allegany",
  "42078A3CE": "Allegany",
  "42078A3NW": "Cattaraugus",
  "42078A4CE": "Cattaraugus",
  "42078A4NW": "Cattaraugus",
  "42078A5CE": "Cattaraugus",
  "42078A5NW": "Cattaraugus",
  "42078A6CE": "Cattaraugus",
  "42078A6NW": "Cattaraugus",
  "42078A7CE": "Cattaraugus",
  "42078A7NW": "Cattaraugus",
  "42078A8CE": "Cattaraugus",
  "42078A8NW": "Cattaraugus",
  "42078B1CE": "Allegany",
  "42078B1NW": "Allegany",
  "42078B2CE": "Allegany",
  "42078B2NW": "Allegany",
  "42078B3CE": "Allegany",
  "42078B3NW": "Cattaraugus",
  "42078B4CE": "Cattaraugus",
  "42078B4NW": "Cattaraugus",
  "42078B5CE": "Cattaraugus",
  "42078B5NW": "Cattaraugus",
  "42078B6CE": "Cattaraugus",
  "42078B6NW": "Cattaraugus",
  "42078B7CE": "Cattaraugus",
  "42078B7NW": "Cattaraugus",
  "42078B8CE": "Cattaraugus",
  "42078B8NW": "Cattaraugus",
  "42078C1CE": "Allegany",
  "42078C1NW": "Allegany",
  "42078C2CE": "Allegany",
  "42078C2NW": "Allegany",
  "42078C3CE": "Allegany",
  "42078C3NW": "Cattaraugus",
  "42078C4CE": "Cattaraugus",
  "42078C4NW": "Cattaraugus",
  "42078C5CE": "Cattaraugus",
  "42078C5NW": "Cattaraugus",
  "42078C6CE": "Cattaraugus",
  "42078C6NW": "Cattaraugus",
  "42078C7CE": "Cattaraugus",
  "42078C7NW": "Cattaraugus",
  "42078C8CE": "Cattaraugus",
  "42078C8NW": "Cattaraugus",
  "42078D1CE": "Allegany",
  "42078D1NW": "Allegany",
  "42078D2CE": "Allegany",
  "42078D2NW": "Allegany",
  "42078D3CE": "Allegany",
  "42078D3NW": "Cattaraugus",
  "42078D4CE": "Cattaraugus",
  "42078D4NW": "Cattaraugus",
  "42078D5CE": "Cattaraugus",
  "42078D5NW": "Cattaraugus",
  "42078D6CE": "Cattaraugus",
  "42078D6NW": "Cattaraugus",
  "42078D7CE": "Cattaraugus",
  "42078D7NW": "Erie",
  "42078D8CE": "Cattaraugus",
  "42078D8NW": "Cattaraugus",
  "42078E1CE": "Livingston",
  "42078E1NW": "Wyoming",
  "42078E2CE": "Wyoming",
  "42078E2NW": "Wyoming",
  "42078E3CE": "Wyoming",
  "42078E3NW": "Wyoming",
  "42078E4CE": "Wyoming",
  "42078E4NW": "Erie",
  "42078E5CE": "Erie",
  "42078E5NW": "Erie",
  "42078E6CE": "Erie",
  "42078E6NW": "Erie",
  "42078E7CE": "Erie",
  "42078E7NW": "Erie",
  "42078E8CE": "Erie",
  "42078E8NW": "Erie",
  "42078F1CE": "Wyoming",
  "42078F1NW": "Wyoming",
  "42078F2CE": "Wyoming",
  "42078F2NW": "Wyoming",
  "42078F3CE": "Wyoming",
  "42078F3NW": "Wyoming",
  "42078F4CE": "Wyoming",
  "42078F4NW": "Erie",
  "42078F5CE": "Erie",
  "42078F5NW": "Erie",
  "42078F6CE": "Erie",
  "42078F6NW": "Erie",
  "42078F7CE": "Erie",
  "42078F7NW": "Erie",
  "42078F8CE": "Erie",
  "42078F8NW": "Erie",
  "42078G1CE": "Wyoming",
  "42078G1NW": "Wyoming",
  "42078G2CE": "Wyoming",
  "42078G2NW": "Wyoming",
  "42078G3CE": "Wyoming",
  "42078G3NW": "Wyoming",
  "42078G4CE": "Wyoming",
  "42078G4NW": "Wyoming",
  "42078G5CE": "Erie",
  "42078G5NW": "Erie",
  "42078G6CE": "Erie",
  "42078G6NW": "Erie",
  "42078G7CE": "Erie",
  "42078G7NW": "Erie",
  "42078H1CE": "Genesee",
  "42078H1NW": "Genesee",
  "42078H2CE": "Genesee",
  "42078H2NW": "Genesee",
  "42078H3CE": "Genesee",
  "42078H3NW": "Genesee",
  "42078H4CE": "Genesee",
  "42078H4NW": "Erie",
  "42078H5CE": "Erie",
  "42078H5NW": "Erie",
  "42078H6CE": "Erie",
  "42078H6NW": "Erie",
  "42078H7CE": "Erie",
  "42078H7NW": "Erie",
  "42078H8CE": "Erie",
  "42078H8NW": "Erie",
  "42079A1CE": "Cattaraugus",
  "42079A1NW": "Chautauqua",
  "42079A2CE": "Chautauqua",
  "42079A2NW": "Chautauqua",
  "42079A3CE": "Chautauqua",
  "42079A3NW": "Chautauqua",
  "42079A4CE": "Chautauqua",
  "42079A4NW": "Chautauqua",
  "42079A5CE": "Chautauqua",
  "42079A5NW": "Chautauqua",
  "42079A6CE": "Chautauqua",
  "42079A6NW": "Chautauqua",
  "42079B1CE": "Cattaraugus",
  "42079B1NW": "Chautauqua",
  "42079B2CE": "Chautauqua",
  "42079B2NW": "Chautauqua",
  "42079B3CE": "Chautauqua",
  "42079B3NW": "Chautauqua",
  "42079B4CE": "Chautauqua",
  "42079B4NW": "Chautauqua",
  "42079B5CE": "Chautauqua",
  "42079B5NW": "Chautauqua",
  "42079B6CE": "Chautauqua",
  "42079B6NW": "Chautauqua",
  "42079C1CE": "Cattaraugus",
  "42079C1NW": "Chautauqua",
  "42079C2CE": "Chautauqua",
  "42079C2NW": "Chautauqua",
  "42079C3CE": "Chautauqua",
  "42079C3NW": "Chautauqua",
  "42079C4CE": "Chautauqua",
  "42079C4NW": "Chautauqua",
  "42079C5CE": "Chautauqua",
  "42079C6CE": "Chautauqua",
  "42079D1CE": "Cattaraugus",
  "42079D1NW": "Chautauqua",
  "42079D2CE": "Chautauqua",
  "42079D2NW": "Chautauqua",
  "42079D3CE": "Chautauqua",
  "42079D3NW": "Chautauqua",
  "42079D4CE": "Chautauqua",
  "42079E1CE": "Erie",
  "42079E1NW": "Erie",
  "42079E2CE": "Chautauqua",
  "42079F1CE": "Erie",
  "43075A2CE": "Herkimer",
  "43075A2NW": "Oneida",
  "43075A3CE": "Oneida",
  "43075A3NW": "Oneida",
  "43075A4CE": "Oneida",
  "43075A4NW": "Oneida",
  "43075A5CE": "Oneida",
  "43075A5NW": "Oneida",
  "43075A6CE": "Madison",
  "43075A6NW": "Madison",
  "43075A7CE": "Madison",
  "43075A7NW": "Madison",
  "43075A8CE": "Madison",
  "43075A8NW": "Madison",
  "43075B2CE": "Oneida",
  "43075B2NW": "Oneida",
  "43075B3CE": "Oneida",
  "43075B3NW": "Oneida",
  "43075B4CE": "Oneida",
  "43075B4NW": "Oneida",
  "43075B5CE": "Oneida",
  "43075B5NW": "Oneida",
  "43075B6CE": "Oneida",
  "43075B6NW": "Oneida",
  "43075B7CE": "Oneida",
  "43075B7NW": "Oneida",
  "43075B8CE": "Oswego",
  "43075B8NW": "Oswego",
  "43075C2CE": "Oneida",
  "43075C2NW": "Oneida",
  "43075C3CE": "Oneida",
  "43075C3NW": "Oneida",
  "43075C4CE": "Oneida",
  "43075C4NW": "Oneida",
  "43075C5CE": "Oneida",
  "43075C5NW": "Oneida",
  "43075C6CE": "Oneida",
  "43075C6NW": "Oneida",
  "43075C7CE": "Oneida",
  "43075C7NW": "Oneida",
  "43075C8CE": "Oswego",
  "43075C8NW": "Oswego",
  "43075D2CE": "Oneida",
  "43075D2NW": "Oneida",
  "43075D3CE": "Oneida",
  "43075D3NW": "Oneida",
  "43075D4CE": "Oneida",
  "43075D4NW": "Lewis",
  "43075D5CE": "Lewis",
  "43075D5NW": "Lewis",
  "43075D6CE": "Oneida",
  "43075D6NW": "Lewis",
  "43075D7CE": "Oneida",
  "43075D7NW": "Oswego",
  "43075D8CE": "Oswego",
  "43075D8NW": "Oswego",
  "43075E2CE": "Oneida",
  "43075E2NW": "Lewis",
  "43075E3CE": "Lewis",
  "43075E3NW": "Lewis",
  "43075E4CE": "Lewis",
  "43075E4NW": "Lewis",
  "43075E5CE": "Lewis",
  "43075E5NW": "Lewis",
  "43075E6CE": "Lewis",
  "43075E6NW": "Lewis",
  "43075E7CE": "Oswego",
  "43075E7NW": "Oswego",
  "43075E8CE": "Oswego",
  "43075E8NW": "Oswego",
  "43075F2CE": "Lewis",
  "43075F2NW": "Lewis",
  "43075F3CE": "Lewis",
  "43075F3NW": "Lewis",
  "43075F4CE": "Lewis",
  "43075F4NW": "Lewis",
  "43075F5CE": "Lewis",
  "43075F5NW": "Lewis",
  "43075F6CE": "Lewis",
  "43075F6NW": "Lewis",
  "43075F7CE": "Oswego",
  "43075F7NW": "Jefferson",
  "43075F8CE": "Oswego",
  "43075F8NW": "Jefferson",
  "43076A1CE": "Onondaga",
  "43076A1NW": "Onondaga",
  "43076A2CE": "Onondaga",
  "43076A2NW": "Onondaga",
  "43076A3CE": "Onondaga",
  "43076A3NW": "Onondaga",
  "43076A4CE": "Onondaga",
  "43076A4NW": "Onondaga",
  "43076A5CE": "Cayuga",
  "43076A5NW": "Cayuga",
  "43076A6CE": "Cayuga",
  "43076A6NW": "Wayne",
  "43076A7CE": "Wayne",
  "43076A7NW": "Wayne",
  "43076A8CE": "Wayne",
  "43076A8NW": "Wayne",
  "43076B1CE": "Onondaga",
  "43076B1NW": "Oswego",
  "43076B2CE": "Onondaga",
  "43076B2NW": "Oswego",
  "43076B3CE": "Onondaga",
  "43076B3NW": "Onondaga",
  "43076B4CE": "Onondaga",
  "43076B4NW": "Oswego",
  "43076B5CE": "Cayuga",
  "43076B5NW": "Cayuga",
  "43076B6CE": "Cayuga",
  "43076B6NW": "Wayne",
  "43076B7CE": "Wayne",
  "43076B7NW": "Wayne",
  "43076B8CE": "Wayne",
  "43076B8NW": "Wayne",
  "43076C1CE": "Oswego",
  "43076C1NW": "Oswego",
  "43076C2CE": "Oswego",
  "43076C2NW": "Oswego",
  "43076C3CE": "Oswego",
  "43076C3NW": "Oswego",
  "43076C4CE": "Oswego",
  "43076C4NW": "Oswego",
  "43076C5CE": "Oswego",
  "43076C5NW": "Oswego",
  "43076C6CE": "Cayuga",
  "43076C6NW": "Cayuga",
  "43076C7CE": "Wayne",
  "43076D1CE": "Oswego",
  "43076D1NW": "Oswego",
  "43076D2CE": "Oswego",
  "43076D2NW": "Oswego",
  "43076D3CE": "Oswego",
  "43076D3NW": "Oswego",
  "43076D4CE": "Oswego",
  "43076D4NW": "Oswego",
  "43076D5CE": "Oswego",
  "43076E1CE": "Oswego",
  "43076E1NW": "Oswego",
  "43076E2CE": "Oswego",
  "43076E2NW": "Oswego",
  "43076F1CE": "Jefferson",
  "43076F1NW": "Jefferson",
  "43076F2CE": "Jefferson",
  "43076F2NW": "Jefferson",
  "43077A1CE": "Wayne",
  "43077A1NW": "Wayne",
  "43077A2CE": "Wayne",
  "43077A2NW": "Wayne",
  "43077A3CE": "Wayne",
  "43077A3NW": "Wayne",
  "43077A4CE": "Monroe",
  "43077A4NW": "Monroe",
  "43077A5CE": "Monroe",
  "43077A5NW": "Monroe",
  "43077A6CE": "Monroe",
  "43077A6NW": "Monroe",
  "43077A7CE": "Monroe",
  "43077A7NW": "Monroe",
  "43077A8CE": "Monroe",
  "43077A8NW": "Genesee",
  "43077B1CE": "Wayne",
  "43077B1NW": "Wayne",
  "43077B2CE": "Wayne",
  "43077B2NW": "Wayne",
  "43077B3CE": "Wayne",
  "43077B3NW": "Wayne",
  "43077B4CE": "Monroe",
  "43077B4NW": "Monroe",
  "43077B5CE": "Monroe",
  "43077B5NW": "Monroe",
  "43077B6CE": "Monroe",
  "43077B6NW": "Monroe",
  "43077B7CE": "Monroe",
  "43077B7NW": "Monroe",
  "43077B8CE": "Monroe",
  "43077B8NW": "Monroe",
  "43077C7CE": "Monroe",
  "43077C7NW": "Monroe",
  "43077C8CE": "Monroe",
  "43077C8NW": "Monroe",
  "43078A1CE": "Genesee",
  "43078A1NW": "Genesee",
  "43078A2CE": "Genesee",
  "43078A2NW": "Genesee",
  "43078A3CE": "Genesee",
  "43078A3NW": "Genesee",
  "43078A4CE": "Genesee",
  "43078A4NW": "Niagara",
  "43078A5CE": "Erie",
  "43078A5NW": "Niagara",
  "43078A6CE": "Erie",
  "43078A6NW": "Niagara",
  "43078A7CE": "Erie",
  "43078A7NW": "Niagara",
  "43078A8CE": "Niagara",
  "43078A8NW": "Niagara",
  "43078B1CE": "Orleans",
  "43078B1NW": "Orleans",
  "43078B2CE": "Orleans",
  "43078B2NW": "Orleans",
  "43078B3CE": "Orleans",
  "43078B3NW": "Orleans",
  "43078B4CE": "Orleans",
  "43078B4NW": "Niagara",
  "43078B5CE": "Niagara",
  "43078B5NW": "Niagara",
  "43078B6CE": "Niagara",
  "43078B6NW": "Niagara",
  "43078B7CE": "Niagara",
  "43078B7NW": "Niagara",
  "43078B8CE": "Niagara",
  "43078B8NW": "Niagara",
  "43078C1CE": "Orleans",
  "43078C1NW": "Orleans",
  "43078C2CE": "Orleans",
  "43078C2NW": "Orleans",
  "43078C3CE": "Orleans",
  "43078C3NW": "Orleans",
  "43078C4CE": "Orleans",
  "43078C4NW": "Niagara",
  "43078C5CE": "Niagara",
  "43078C5NW": "Niagara",
  "43078C6CE": "Niagara",
  "43078C6NW": "Niagara",
  "43078C7CE": "Niagara",
  "43079B1CE": "Niagara",
}

# As of 2024-01-12
WNYCNY_COMPLETE_URLID = {
  "42075A2NW",
  "42075A4CE",
  "42075A8NW",
  "42075B2NW",
  "42075B3CE",
  "42075B3NW",
  "42075B4CE",
  "42075B4NW",
  "42075B5NW",
  "42075B6NW",
  "42075B7NW",
  "42075C2CE",
  "42075C2NW",
  "42075C3CE",
  "42075C3NW",
  "42075C4NW",
  "42075C5CE",
  "42075C5NW",
  "42075C6CE",
  "42075C6NW",
  "42075C7CE",
  "42075C7NW",
  "42075C8CE",
  "42075C8NW",
  "42075D2CE",
  "42075D2NW",
  "42075D3CE",
  "42075D3NW",
  "42075D4CE",
  "42075D4NW",
  "42075D5CE",
  "42075D5NW",
  "42075D6CE",
  "42075D6NW",
  "42075D7CE",
  "42075D7NW",
  "42075D8CE",
  "42075D8NW",
  "42075E2CE",
  "42075E2NW",
  "42075E3CE",
  "42075E3NW",
  "42075E4CE",
  "42075E4NW",
  "42075E5CE",
  "42075E5NW",
  "42075E6CE",
  "42075E6NW",
  "42075E7CE",
  "42075E7NW",
  "42075E8NW",
  "42075F2CE",
  "42075F2NW",
  "42075F3CE",
  "42075F3NW",
  "42075F4CE",
  "42075F4NW",
  "42075F5CE",
  "42075F5NW",
  "42075F6CE",
  "42075F6NW",
  "42075F7CE",
  "42075F7NW",
  "42075F8CE",
  "42075F8NW",
  "42075G2CE",
  "42075G2NW",
  "42075G3CE",
  "42075G4CE",
  "42075G5CE",
  "42075G5NW",
  "42075G6NW",
  "42075H8NW",
  "42076A2NW",
  "42076A3NW",
  "42076A4CE",
  "42076A4NW",
  "42076A5CE",
  "42076A6CE",
  "42076A6NW",
  "42076A7CE",
  "42076A7NW",
  "42076A8NW",
  "42076B1NW",
  "42076B2NW",
  "42076B3CE",
  "42076B3NW",
  "42076B4CE",
  "42076B5CE",
  "42076B6CE",
  "42076B6NW",
  "42076B7CE",
  "42076B7NW",
  "42076C1NW",
  "42076C2CE",
  "42076C2NW",
  "42076C3CE",
  "42076C3NW",
  "42076C4CE",
  "42076C4NW",
  "42076C5CE",
  "42076C5NW",
  "42076C6CE",
  "42076C6NW",
  "42076C7NW",
  "42076C8NW",
  "42076D1CE",
  "42076D1NW",
  "42076D2CE",
  "42076D2NW",
  "42076D3CE",
  "42076D3NW",
  "42076D4CE",
  "42076D4NW",
  "42076D5CE",
  "42076D5NW",
  "42076D6CE",
  "42076D7CE",
  "42076D7NW",
  "42076D8NW",
  "42076E1CE",
  "42076E1NW",
  "42076E2CE",
  "42076E2NW",
  "42076E3CE",
  "42076E3NW",
  "42076E4CE",
  "42076E4NW",
  "42076E5CE",
  "42076E5NW",
  "42076E6CE",
  "42076E7CE",
  "42076F1NW",
  "42076F2CE",
  "42076F2NW",
  "42076F3CE",
  "42076F4CE",
  "42076F4NW",
  "42076F5NW",
  "42076F6NW",
  "42076F7NW",
  "42076G1CE",
  "42076G4CE",
  "42076G6CE",
  "42076G8NW",
  "42076H3NW",
  "42076H5NW",
  "42076H6CE",
  "42076H6NW",
  "42077A1CE",
  "42077A2CE",
  "42077A2NW",
  "42077A3CE",
  "42077A3NW",
  "42077A4CE",
  "42077A5CE",
  "42077A5NW",
  "42077A6CE",
  "42077A6NW",
  "42077A8CE",
  "42077B7NW",
  "42077B8NW",
  "42077C2NW",
  "42077C4NW",
  "42077C7NW",
  "42077C8CE",
  "42077C8NW",
  "42077D3CE",
  "42077D7NW",
  "42077D8CE",
  "42077E2CE",
  "42077E2NW",
  "42077E3NW",
  "42077E5NW",
  "42077E8NW",
  "42077F4CE",
  "42077F4NW",
  "42077F5CE",
  "42077F5NW",
  "42077F6CE",
  "42077F6NW",
  "42077F7CE",
  "42077F8CE",
  "42077G1NW",
  "42077G3CE",
  "42077G4CE",
  "42077G5CE",
  "42077G5NW",
  "42077G6CE",
  "42077G6NW",
  "42077G7CE",
  "42077G7NW",
  "42077G8CE",
  "42077H1NW",
  "42077H5NW",
  "42077H6NW",
  "42077H7CE",
  "42077H7NW",
  "42078A1CE",
  "42078A1NW",
  "42078A6CE",
  "42078A6NW",
  "42078A8CE",
  "42078B3NW",
  "42078C2CE",
  "42078C2NW",
  "42078C3CE",
  "42078C3NW",
  "42078C5CE",
  "42078C5NW",
  "42078C6CE",
  "42078C6NW",
  "42078C7CE",
  "42078D2CE",
  "42078D3CE",
  "42078D3NW",
  "42078D4CE",
  "42078D4NW",
  "42078D5CE",
  "42078D5NW",
  "42078D6CE",
  "42078D6NW",
  "42078D7CE",
  "42078D7NW",
  "42078E2CE",
  "42078E2NW",
  "42078E3CE",
  "42078E3NW",
  "42078E4CE",
  "42078E4NW",
  "42078E5CE",
  "42078E5NW",
  "42078E6CE",
  "42078E6NW",
  "42078E7CE",
  "42078E7NW",
  "42078E8CE",
  "42078E8NW",
  "42078F3CE",
  "42078F3NW",
  "42078F4CE",
  "42078F4NW",
  "42078F5CE",
  "42078F5NW",
  "42078F6CE",
  "42078F6NW",
  "42078F7CE",
  "42078F7NW",
  "42078F8CE",
  "42078G1NW",
  "42078G2CE",
  "42078G2NW",
  "42078G3NW",
  "42078G4CE",
  "42078G4NW",
  "42078G5CE",
  "42078G5NW",
  "42078G6CE",
  "42078G6NW",
  "42078G7CE",
  "42078G7NW",
  "42078H1CE",
  "42078H2CE",
  "42078H2NW",
  "42078H4CE",
  "42078H5CE",
  "42078H5NW",
  "42078H6CE",
  "42078H6NW",
  "42078H8CE",
  "42078H8NW",
  "42079A1CE",
  "42079A5NW",
  "42079A6CE",
  "42079B2CE",
  "42079B2NW",
  "42079B3NW",
  "42079B5CE",
  "42079B5NW",
  "42079B6NW",
  "42079C2CE",
  "42079C2NW",
  "42079C3NW",
  "42079C4CE",
  "42079C4NW",
  "42079D1CE",
  "42079D2CE",
  "42079D2NW",
  "42079D3NW",
  "42079D4CE",
  "42079E1CE",
  "42079E1NW",
  "42079E2CE",
  "42079F1CE",
  "43075A2NW",
  "43075A3NW",
  "43075A7NW",
  "43075A8CE",
  "43075B4CE",
  "43075B5CE",
  "43075B6NW",
  "43075B8NW",
  "43075C2CE",
  "43075C2NW",
  "43075C3NW",
  "43075C4CE",
  "43075C6CE",
  "43075C6NW",
  "43075C7CE",
  "43075C7NW",
  "43075C8NW",
  "43075D3NW",
  "43075D8CE",
  "43075E7CE",
  "43076A1CE",
  "43076A2NW",
  "43076A4CE",
  "43076A4NW",
  "43076A5CE",
  "43076A5NW",
  "43076A6CE",
  "43076A8CE",
  "43076A8NW",
  "43076B1NW",
  "43076B2NW",
  "43076B3CE",
  "43076B3NW",
  "43076B4CE",
  "43076B4NW",
  "43076B5CE",
  "43076B8NW",
  "43076C1CE",
  "43076C1NW",
  "43076C2CE",
  "43076C2NW",
  "43076C3CE",
  "43076C3NW",
  "43076C4CE",
  "43076C4NW",
  "43076C5CE",
  "43076C5NW",
  "43076C6CE",
  "43076C6NW",
  "43076C7CE",
  "43076D1CE",
  "43076D1NW",
  "43076D2CE",
  "43076D2NW",
  "43076D3CE",
  "43076D3NW",
  "43076D4CE",
  "43076D4NW",
  "43076D5CE",
  "43076E1CE",
  "43076E2CE",
  "43076E2NW",
  "43076F2CE",
  "43076F2NW",
  "43077A2NW",
  "43077A3CE",
  "43077A3NW",
  "43077A4CE",
  "43077A5CE",
  "43077A5NW",
  "43077A6NW",
  "43077A7CE",
  "43077A8NW",
  "43077B1NW",
  "43077B2NW",
  "43077B3NW",
  "43077B4CE",
  "43077B4NW",
  "43077B5CE",
  "43077B5NW",
  "43077B8CE",
  "43077B8NW",
  "43077C7CE",
  "43077C7NW",
  "43077C8CE",
  "43077C8NW",
  "43078A3CE",
  "43078A3NW",
  "43078A4CE",
  "43078A4NW",
  "43078A5CE",
  "43078A6CE",
  "43078A6NW",
  "43078A7CE",
  "43078A8CE",
  "43078B1NW",
  "43078B2CE",
  "43078B3CE",
  "43078B3NW",
  "43078B4CE",
  "43078B4NW",
  "43078B5CE",
  "43078B5NW",
  "43078B6CE",
  "43078B7CE",
  "43078B8CE",
  "43078B8NW",
  "43078C1CE",
  "43078C1NW",
  "43078C2CE",
  "43078C2NW",
  "43078C3CE",
  "43078C3NW",
  "43078C4NW",
  "43078C5CE",
  "43078C5NW",
  "43078C6CE",
  "43078C6NW",
  "43078C7CE",
}

##########################
# START START START START
##########################

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
    """
    coordinates are 5 sets of y,x (not x,y) points:
        0: lower left
        1: upper left
        2: upper right
        3: lower right
        4: lower left (== 0)
    """
    coordelt = one(pm.iter(NS + 'coordinates'))
    coordtexts = [coord.split(',', 1) for coord in coordelt.text.split()]
    return coordtexts

def get_llcoord(pm):
    coordtexts = get_coords(pm)
    assert len(coordtexts) == 5
    assert coordtexts[0] == coordtexts[4]
    return tuple(map(float, coordtexts[0]))

def get_ulcoord(pm):
    coordtexts = get_coords(pm)
    assert len(coordtexts) == 5
    assert coordtexts[0] == coordtexts[4]
    return tuple(map(float, coordtexts[1]))

#######################################################

def for_each_placemark(fol):
    return fol.findall(NS + 'Placemark')

def et_folder(et):
    kml = et.getroot()
    ns, kmltag = kml.tag.rsplit('}', 1)
    ns += '}'
    assert ns == NS
    single = set() # compare one() above
    for doc in kml:
        for elt in doc:
            if elt.tag == NS + "Schema":
                pass
            elif elt.tag == NS + "Folder":
                if not single:
                    single.add(elt)
                else:
                    raise MyException("Too many Folders")
            else:
                raise MyException("Unexpected Document child: " + elt.tag)
    return single.pop()

# XXX obsolete
def for_each_folder(et):
    kml = et.getroot()
    ns, kmltag = kml.tag.rsplit('}', 1)
    ns += '}'
    assert ns == NS
    for doc in kml:
        for fol in doc:
            yield fol

#######################################################

def get_block_urlid(block_name):
    assert block_name.endswith(("_NW", "_NE", "_CW", "_CE", "_SW", "_SE"))
    base = block_name[:-3]
    corner = block_name[-2:]
    urlid = USGSBLOCK_TO_URLID[base]
    return urlid + corner

def get_block_url(urlid):
    return "https://ebird.org/atlasny/block/" + urlid

def mkdir_exist_ok(dirname):
    if os.path.exists(dirname):
        assert os.path.isdir(dirname)
    else:
        os.mkdir(dirname)
    return dirname

def assert_sameish_block_name(name1, name2):
    # casefold: for DeRuyter vs Deruyter
    if name1.replace("_", " ").casefold() != name2.casefold():
        raise MyException(f"block names differ: {name1} vs {name2}")

#######################################################

def check_placemark_coords(pm):
    coords = get_llcoord(pm)
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

def check_placemark_counties(pm):
    block_name = get_block_name(pm)
    urlid = get_block_urlid(block_name)
    maincounty = WNYCNY_URLID_TO_MAINCOUNTY.get(urlid, None)
    return maincounty in COUNTIES

#######################################################

def add_name(pm):
    block_name = get_block_name(pm)
    name = ET.SubElement(pm, 'name')
    name.text = block_name
    print("Adding name", block_name)

POLYSTYLE_FILL0 = None
def polystyle_fill0():
    """
    <PolyStyle>
      <fill>0</fill>
    </PolyStyle>
    """
    global POLYSTYLE_FILL0
    if POLYSTYLE_FILL0 is None:
      fill0 = ET.Element("fill")
      fill0.text = "0"
      ps = ET.Element("PolyStyle")
      ps.append(fill0)
      POLYSTYLE_FILL0 = ps
    return POLYSTYLE_FILL0

def make_color_style(agbr):
    """
    <Style>
      <LineStyle>
        <color>ff0000ff</color>
      </LineStyle>
      <PolyStyle>
        <fill>0</fill>
      </PolyStyle>
    </Style>
    """
    color = ET.Element("color")
    color.text = agbr
    ls = ET.Element("LineStyle")
    ls.append(color)
    style = ET.Element("Style")
    style.append(ls)
    style.append(polystyle_fill0())
    return style

COLOR_STYLES = dict()
def color_style(rgb):
    agbr = "ff" + rgb[4:6] + rgb[2:4] + rgb[0:2]
    if agbr in COLOR_STYLES:
        return COLOR_STYLES[agbr]
    else:
        return COLOR_STYLES.setdefault(agbr, make_color_style(agbr))


# Return summary, complete, rgb
def get_block_summary_shallow(urlid):
    complete = urlid in WNYCNY_COMPLETE_URLID
    return "", complete, "000000" if complete else "ffff00"

# Return summary, complete, rgb
def get_block_summary_from_file(urlid):
    url = get_block_url(urlid)
    # Fetch block html to outfile
    outfile = os.path.join(mkdir_exist_ok("tmp_html"), urlid)
    if DO_DOWNLOAD:
        if USE_CACHE and os.path.exists(outfile):
            print("Cached: ", outfile) # verbose
        else:
            req = requests.get(url, allow_redirects=True)
            with open(outfile, "wb") as outf:
                outf.write(req.content)
            print("Fetched: ", outfile) # verbose
    stats = parse_block_html(outfile)
    assert_sameish_block_name(block_name, stats.block_name)
    #if stats.complete:
    #    print("Skipping complete block:", stats.block_name)
    #    return None, None, None # Skip completed blocks

    rgb = "ffffff"
    if stats.complete:
        rgb = "000000"
    elif stats.confirmed <= 10:
        rgb = "9bc4cf"
    elif stats.confirmed <= 20:
        rgb = "c7e466"
    elif stats.confirmed <= 30:
        rgb = "eaeb1f"
    elif stats.confirmed <= 40:
        rgb = "fac500"
    elif stats.confirmed <= 50:
        rgb = "e57701"
    elif stats.confirmed <= 60:
        rgb = "e33b15"
    else:
        rgb = "ad0002"

    return stats.short_repr(), stats.complete, rgb

def update_placemark(pm, get_block_summary):
    block_name = get_block_name(pm)
    urlid = get_block_urlid(block_name)
    url = get_block_url(urlid)

    summary, complete, rgb = get_block_summary(urlid)
    if summary is None:
        return None

    pm2 = ET.Element('Placemark')
    name = ET.SubElement(pm2, 'name')
    name.text = block_name + (" (complete)" if complete else "")

    descr = ET.SubElement(pm2, 'description')
    descr.text = summary + f"{url}"

    polygon = one(pm.findall(NS + 'Polygon'))
    pm2.append(polygon)

    pm2.append(color_style(rgb))
    return pm2

def fol_collect_placemarks(fol, check_placemark, get_block_summary):
    """ rich mode: create new pm's with updated attrs """
    keepers = list()
    nkeepers = 0
    ncomplete = 0
    ndiscard = 0
    for pm in for_each_placemark(fol):
        if check_placemark(pm):
            pm2 = update_placemark(pm, get_block_summary)
            if pm2 is None:
                ncomplete += 1
            else:
                keepers.append(pm2)
                nkeepers += 1
        else:
            ndiscard += 1
    print("Keepers:", nkeepers, "Complete:", ncomplete, "Discards:", ndiscard)
    fol.clear()
    name = ET.SubElement(fol, 'name')
    name.text = 'Priority Blocks'
    for pm in keepers:
        fol.append(pm)

# OBSOLETE: use fol_collect_placemarks instead
def fol_filter_placemarks(fol, check_placemark):
    """ non-rich mode: just keep existing pm's, remove discards """
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

def fol_dump_urls(fol, check_placemark, outfile):
    with open(outfile, "w") as fp:
        for pm in for_each_placemark(fol):
            block_name = get_block_name(pm)
            urlid = get_block_urlid(block_name)
            url = get_block_url(urlid)
            if check_placemark(pm):
                print(url, file=fp)
            #else:
            #    print("#", url, file=fp)

def lat_lon_bname_key(lat_lon_bname):
    lat, lon, bname = lat_lon_bname
    return (-lat, -lon, bname)

def et_dump_coords(et, outfile):
    lat_lon_bname = set()
    for pm in for_each_placemark(et_folder(et)):
        bname = get_block_name(pm)
        ulcoords = get_llcoord(pm)
        lat_lon_bname.add((ulcoords[1], ulcoords[0], bname))
    with open(outfile, "w") as outf:
        for lat, lon, bname in sorted(lat_lon_bname, key=lat_lon_bname_key):
            print(lat, lon, bname, file=outf)

def lonlat2id(lon, lat):
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

def et_dump_url_ids(et, outfile):
    id2name = dict()
    nw_name2coords = dict()                                 # SANITY
    ce_name2coords = dict()                                 # SANITY
    for pm in for_each_placemark(et_folder(et)):
        bname = get_block_name(pm)
        if bname.endswith("_NW"):
            name = bname[:-3]
            ulcoords = get_ulcoord(pm)
            blk_id = lonlat2id(*ulcoords)
            oldval = id2name.setdefault(blk_id, name)
            assert oldval == name
            nw_name2coords[name] = ulcoords                 # SANITY
        else:
            assert bname.endswith("_CE")
            name = bname[:-3]
            ulcoords = get_ulcoord(pm)
            nwcoords = (ulcoords[0] - (1/16), round(ulcoords[1] + (1/24), 3))
            blk_id = lonlat2id(*nwcoords)
            oldval = id2name.setdefault(blk_id, name)
            assert oldval == name
            ce_name2coords[name] = nwcoords                 # SANITY
    for name in sorted(nw_name2coords):                     # SANITY
        if (name in ce_name2coords and                      # SANITY
            nw_name2coords[name] != ce_name2coords[name]    # SANITY
            ):                                              # SANITY
           print(f'{name} NW {nw_name2coords[name]}')       # SANITY
           print(f'{name} CE {ce_name2coords[name]}')       # SANITY
    with open(outfile, "w") as outf:
        for blk_id in sorted(id2name):
            # Longest USGS block names in NYS:
            #   "Cannonsville Reservoir"
            #   "Vanderwhacker Mountain"
            namestr = f'"{id2name[blk_id]}"'.ljust(24)
            print(f'  {namestr} : "{blk_id}",', file=outf)

#######################################################
# Parsing html of https://ebird.org/atlasny/block/43074G7NW

def extract_td_number(line):
    """ <td headers="th-summary-pos" class="h2 num">18</td> """
    res = line.split(">", 1)[1].split("<", 1)[0]
    return int(res)

class BlockStats(object):
    def __init__(self):
        self.block_name = None
        self.complete = None
        self.diurnal = None
        self.nocturnal = None
        self.observed = None
        self.possible = None
        self.probable = None
        self.confirmed = None
        self.total = None

    def __repr__(self):
        return f"""block_name: {self.block_name}
complete: {self.complete}
diurnal: {self.diurnal}
nocturnal: {self.nocturnal}
observed: {self.observed}
possible: {self.possible}
probable: {self.probable}
confirmed: {self.confirmed}
total: {self.total}
"""

    def short_repr(self):
        cfmpos = self.confirmed + self.possible
        return (f"cfm={self.confirmed} +pos={cfmpos} tot={self.total}\n\n"
                f"dhrs={self.diurnal}\n")

    def parse_block_name(self, line):
        """ <title>Eagle Bay NW - New York Breeding Bird Atlas</title> """
        assert self.block_name is None
        self.block_name = line.split(">", 1)[1].split(" - ", 1)[0]
        assert self.block_name.endswith(
                (" NW", " NE", " CW", " CE", " SW", " SE"))

    def parse_status(self, line):
        assert self.complete is None
        self.complete = ("hs-complete" in line)

    def parse_effort_hours(self, line):
        """ <h2>22.74 / 0.00</h2> """
        assert self.diurnal is None
        assert self.nocturnal is None
        s1 = line.split(">", 1)[1]
        r1,s2 = s1.split(" / ", 1)
        r2 = s2.split("<", 1)[0]
        self.diurnal = float(r1.replace(',',''))
        self.nocturnal = float(r2.replace(',',''))

    def parse_stat(self, line):
        if "th-summary-obs" in line:
            assert not self.observed
            self.observed = extract_td_number(line)
            return True
        if "th-summary-pos" in line:
            assert not self.possible
            self.possible = extract_td_number(line)
            return True
        if "th-summary-pro" in line:
            assert not self.probable
            self.probable = extract_td_number(line)
            return True
        if "th-summary-con" in line:
            assert not self.confirmed
            self.confirmed = extract_td_number(line)
            return True
        if "th-summary-tot" in line:
            assert not self.total
            self.total = extract_td_number(line)
            return True

def parse_block_html(filename):
    # TODO: also parse county? - NOTE only shows one county
    """
    Look for the following parts
    Part 1:
        <title>Eagle Bay NW - New York Breeding Bird Atlas</title>

    Part 2:
        <h2 class="hs-status hs-complete">Complete <i class="ss-icon">&#x2713;</i></h2>
        <h2 class="hs-status ">Incomplete </h2>

    Part 3:
        <p>Effort hours (diurnal/nocturnal):</p>
        <h2>22.74 / 0.00</h2>

    Part 4:
        <tr class="tr--major">
        <td headers="th-summary-period" class="h2">New York Breeding Bird Atlas 3</td>

            <td headers="th-summary-obs" class="h2 num">2</td>
            <td headers="th-summary-pos" class="h2 num">18</td>
            <td headers="th-summary-pro" class="h2 num">22</td>
            <td headers="th-summary-con" class="h2 num">19</td>
            <td headers="th-summary-tot" class="h2 num">59</td>
        </tr>

    """
    stats = BlockStats()
    with open(filename) as inf:
        mode = "initial"
        for line in inf:
            if mode == "initial":
                if "<title>" in line:
                    stats.parse_block_name(line)
                    mode = "find_status"
            elif mode == "find_status":
                if '<h2 class="hs-status' in line:
                    stats.parse_status(line)
                    mode = "find_effort"
            elif mode == "find_effort":
                if "Effort hours" in line:
                    mode = "effort"
            elif mode == "effort":
                stats.parse_effort_hours(line)
                mode = "find_stats"
            elif mode == "find_stats":
                if ">New York Breeding Bird Atlas 3<" in line:
                    mode = "stats"
            elif mode == "stats":
                if line.strip() == "</tr>":
                    mode = "end"
                    break # Stop parsing; could just return stats here
                stats.parse_stat(line)
            else:
                raise MyException("Bad mode: " + mode)
    return stats

#######################################################
# "MAIN"

USAGE = """
ARGS:
  urls <blockfilter>: dump urls of matching blocks
  rich <blockfilter>: write rich kml of matching blocks, needs urls
  shallow <blockfilter>: write shallow-filtered kml of matching blocks
  coords: dump each block's ul coords ~ useless now
  url_ids: dump superblock url ids based on NW coords
  html infile: parse stats from input html file for a block

  <blockfilter> = bounds|counties|inclist
    bounds (default): matching per hard-coded bounding coordinates
    counties: matching per hard-coded COUNTIES[12] list
    inclist: matching per hard-coded INCLIST
    cny, wnycny, graves[123]: hardcoded subsets
"""

class Arg2Opts(object):
    def __init__(self, mode):
        def nop():
            pass
        self.postcheck = nop
        self.blockfilter = mode # documentation only

        global COUNTIES
        global ULCOORDS
        global LRCOORDS
        GRAVES1 = set(["Ontario", "Wayne", "Oswego"])
        GRAVES2 = set(["Seneca", "Cayuga", "Onondaga"])
        GRAVES3 = set(["Steuben", "Schuyler", "Yates"])

        if mode == "bounds":
            self.checkfn = check_placemark_coords
        elif mode == "wnycny":
            self.checkfn = check_placemark_coords
            ULCOORDS = (-79.75,43.7083333356)
            LRCOORDS = (-75.1875,42.0416666715999)
        elif mode == "counties":
            self.checkfn = check_placemark_counties
        elif mode == "cny":
            self.checkfn = check_placemark_counties
            COUNTIES = set(["Wayne", "Oswego", "Onondaga", "Madison",
                            "Ontario", "Yates", "Seneca", "Cayuga",
                            "Steuben", "Schuyler", "Tompkins", "Cortland",
                            "Chemung", "Tioga", "Broome", "Chenango"])
        elif mode == "graves1":
            self.checkfn = check_placemark_counties
            COUNTIES = GRAVES1
        elif mode == "graves2":
            self.checkfn = check_placemark_counties
            COUNTIES = GRAVES2
        elif mode == "graves3":
            self.checkfn = check_placemark_counties
            COUNTIES = GRAVES3
        elif mode == "graves":
            self.checkfn = check_placemark_counties
            COUNTIES = GRAVES1 | GRAVES2 | GRAVES3
        else:
            assert mode == "inclist"
            assert INCLIST
            self.checkfn = check_placemark_inclist_remove
            def check_leftovers():
                if INCLIST:
                    print("WARNING: leftovers in INCLIST:")
                    for name in sorted(INCLIST):
                        print("\t", name)
            self.postcheck = check_leftovers

def get_argv2_opts(argv):
    # default argv2 is "bounds"
    return Arg2Opts(argv[2] if len(argv) > 2 else "bounds")

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
    elif action == "url_ids":
        et = ET.parse('Block_Master_Priority.kml')
        outfile = "out_url_ids.txt"
        et_dump_url_ids(et, outfile)
        print("Wrote:", outfile)
        sys.exit(0)
    elif action == "urls":
        opts =  get_argv2_opts(sys.argv)
        et = ET.parse('Block_Master_Priority.kml')
        outfile = "out_urls.txt"
        fol_dump_urls(et_folder(et), opts.checkfn, outfile)
        print("Wrote:", outfile)
        opts.postcheck()
        sys.exit(0)
    elif action == "rich":
        opts =  get_argv2_opts(sys.argv)
        et = ET.parse('Block_Master_Priority.kml')
        fol_collect_placemarks(et_folder(et), opts.checkfn,
                               get_block_summary_from_file)
        opts.postcheck()
        outfile = "output.kml"
        et.write(outfile)
        print("Wrote:", outfile)
        sys.exit(0)
    elif action == "shallow":
        opts =  get_argv2_opts(sys.argv)
        et = ET.parse('Block_Master_Priority.kml')
        #fol_filter_placemarks(et_folder(et), opts.checkfn)
        fol_collect_placemarks(et_folder(et), opts.checkfn,
                               get_block_summary_shallow)
        opts.postcheck()
        outfile = "output.kml"
        et.write(outfile)
        print("Wrote:", outfile)
        sys.exit(0)
    elif action == "html":
        stats = parse_block_html(sys.argv[2])
        print(repr(stats))
        sys.exit(0)
    else:
        print("ERROR: unrecognized param", action)
        print(USAGE)
        sys.exit(1)
