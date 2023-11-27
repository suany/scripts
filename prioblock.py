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

NYS_URLID_TO_USGSBLOCK = [
  ("40072F7", "Pattersquash Island"),
  ("40072G4", "Shinnecock Inlet"),
  ("40072G5", "Quogue"),
  ("40072G6", "Eastport"),
  ("40072G7", "Moriches"),
  ("40072G8", "Bellport"),
  ("40072H1", "Napeague Beach"),
  ("40072H2", "East Hampton"),
  ("40072H3", "Sag Harbor"),
  ("40072H4", "Southampton"),
  ("40072H5", "Mattituck"),
  ("40072H6", "Riverhead"),
  ("40072H7", "Wading River"),
  ("40073E4", "West Gilgo Beach"),
  ("40073E5", "Jones Inlet"),
  ("40073E6", "Lawrence"),
  ("40073E7", "Far Rockaway"),
  ("40073E8", "Coney Island"),
  ("40073F1", "Sayville"),
  ("40073F2", "Bay Shore East"),
  ("40073F3", "Bay Shore West"),
  ("40073F4", "Amityville"),
  ("40073F5", "Freeport"),
  ("40073F6", "Lynbrook"),
  ("40073F7", "Jamaica"),
  ("40073F8", "Brooklyn"),
  ("40073G1", "Patchogue"),
  ("40073G2", "Central Islip"),
  ("40073G3", "Greenlawn"),
  ("40073G4", "Huntington"),
  ("40073G5", "Hicksville"),
  ("40073G6", "Sea Cliff"),
  ("40073G7", "Flushing"),
  ("40073H1", "Port Jefferson"),
  ("40073H6", "Mamaroneck"),
  ("40073H7", "Mount Vernon"),
  ("40074E1", "The Narrows"),
  ("40074E2", "Arthur Kill"),
  ("41072A1", "Gardiners Island East"),
  ("41072A3", "Greenport"),
  ("41073A6", "Glenville"),
  ("41073A7", "White Plains"),
  ("41073A8", "Nyack"),
  ("41073B5", "Pound Ridge"),
  ("41073B6", "Mount Kisco"),
  ("41073B7", "Ossining"),
  ("41073B8", "Haverstraw"),
  ("41073C5", "Peach Lake"),
  ("41073C6", "Croton Falls"),
  ("41073C7", "Mohegan Lake"),
  ("41073C8", "Peekskill"),
  ("41073D5", "Brewster"),
  ("41073D6", "Lake Carmel"),
  ("41073D7", "Oscawana Lake"),
  ("41073D8", "West Point"),
  ("41073E5", "Pawling"),
  ("41073E6", "Poughquag"),
  ("41073E7", "Hopewell Junction"),
  ("41073E8", "Wappingers Falls"),
  ("41073F5", "Dover Plains"),
  ("41073F6", "Verbank"),
  ("41073F7", "Pleasant Valley"),
  ("41073F8", "Poughkeepsie"),
  ("41073G5", "Amenia"),
  ("41073G6", "Millbrook"),
  ("41073G7", "Salt Point"),
  ("41073G8", "Hyde Park"),
  ("41073H4", "Sharon"),
  ("41073H5", "Millerton"),
  ("41073H6", "Pine Plains"),
  ("41073H7", "Rock City"),
  ("41073H8", "Kingston East"),
  ("41074A1", "Park Ridge"),
  ("41074B1", "Thiells"),
  ("41074B2", "Sloatsburg"),
  ("41074B3", "Greenwood Lake"),
  ("41074C1", "Popolopen Lake"),
  ("41074C2", "Monroe"),
  ("41074C3", "Warwick"),
  ("41074C4", "Pine Island"),
  ("41074C5", "Unionville"),
  ("41074D1", "Cornwall-on-Hudson"),
  ("41074D2", "Maybrook"),
  ("41074D3", "Goshen"),
  ("41074D4", "Middletown"),
  ("41074D5", "Otisville"),
  ("41074D6", "Port Jervis North"),
  ("41074D7", "Pond Eddy"),
  ("41074D8", "Shohola"),
  ("41074E1", "Newburgh"),
  ("41074E2", "Walden"),
  ("41074E3", "Pine Bush"),
  ("41074E4", "Wurtsboro"),
  ("41074E5", "Yankee Lake"),
  ("41074E6", "Hartwood"),
  ("41074E7", "Highland Lake"),
  ("41074E8", "Eldred"),
  ("41074F1", "Clintondale"),
  ("41074F2", "Gardiner"),
  ("41074F3", "Napanoch"),
  ("41074F4", "Ellenville"),
  ("41074F5", "Woodridge"),
  ("41074F6", "Monticello"),
  ("41074F7", "White Lake"),
  ("41074F8", "Lake Huntington"),
  ("41074G1", "Rosendale"),
  ("41074G2", "Mohonk Lake"),
  ("41074G3", "Kerhonkson"),
  ("41074G4", "Rondout Reservoir"),
  ("41074G5", "Grahamsville"),
  ("41074G6", "Liberty East"),
  ("41074G7", "Liberty West"),
  ("41074G8", "Jeffersonville"),
  ("41074H1", "Kingston West"),
  ("41074H2", "Ashokan"),
  ("41074H3", "West Shokan"),
  ("41074H4", "Peekamoose Mountain"),
  ("41074H5", "Claryville"),
  ("41074H6", "Willowemoc"),
  ("41074H7", "Livingston Manor"),
  ("41074H8", "Roscoe"),
  ("41075G1", "Callicoon"),
  ("41075G2", "Long Eddy"),
  ("41075H1", "Horton"),
  ("41075H2", "Fishs Eddy"),
  ("41075H3", "Hancock"),
  ("42073A5", "Copake"),
  ("42073A6", "Ancram"),
  ("42073A7", "Clermont"),
  ("42073A8", "Saugerties"),
  ("42073B4", "Egremont"),
  ("42073B5", "Hillsdale"),
  ("42073B6", "Claverack"),
  ("42073B7", "Hudson South"),
  ("42073B8", "Cementon"),
  ("42073C4", "State Line"),
  ("42073C5", "Chatham"),
  ("42073C6", "Stottville"),
  ("42073C7", "Hudson North"),
  ("42073C8", "Leeds"),
  ("42073D4", "Canaan"),
  ("42073D5", "East Chatham"),
  ("42073D6", "Kinderhook"),
  ("42073D7", "Ravena"),
  ("42073D8", "Alcove"),
  ("42073E3", "Hancock MA"),
  ("42073E4", "Stephentown Center"),
  ("42073E5", "Nassau"),
  ("42073E6", "East Greenbush"),
  ("42073E7", "Delmar"),
  ("42073E8", "Clarksville"),
  ("42073F3", "Berlin"),
  ("42073F4", "Taborton"),
  ("42073F5", "Averill Park"),
  ("42073F6", "Troy South"),
  ("42073F7", "Albany"),
  ("42073F8", "Voorheesville"),
  ("42073G3", "North Pownal"),
  ("42073G4", "Grafton"),
  ("42073G5", "Tomhannock"),
  ("42073G6", "Troy North"),
  ("42073G7", "Niskayuna"),
  ("42073G8", "Schenectady"),
  ("42073H3", "Hoosick Falls"),
  ("42073H4", "Eagle Bridge"),
  ("42073H5", "Schaghticoke"),
  ("42073H6", "Mechanicville"),
  ("42073H7", "Round Lake"),
  ("42073H8", "Burnt Hills"),
  ("42074A1", "Woodstock"),
  ("42074A2", "Bearsville"),
  ("42074A3", "Phoenicia"),
  ("42074A4", "Shandaken"),
  ("42074A5", "Seager"),
  ("42074A6", "Arena"),
  ("42074A7", "Lewbeach"),
  ("42074A8", "Downsville"),
  ("42074B1", "Kaaterskill Clove"),
  ("42074B2", "Hunter"),
  ("42074B3", "Lexington"),
  ("42074B4", "West Kill"),
  ("42074B5", "Fleischmanns"),
  ("42074B6", "Margaretville"),
  ("42074B7", "Andes"),
  ("42074B8", "Hamden"),
  ("42074C1", "Freehold"),
  ("42074C2", "Hensonville"),
  ("42074C3", "Ashland"),
  ("42074C4", "Prattsville"),
  ("42074C5", "Roxbury"),
  ("42074C6", "Hobart"),
  ("42074C7", "Bloomville"),
  ("42074C8", "Delhi"),
  ("42074D1", "Greenville"),
  ("42074D2", "Durham"),
  ("42074D3", "Livingstonville"),
  ("42074D4", "Gilboa"),
  ("42074D5", "Stamford"),
  ("42074D6", "Harpersfield"),
  ("42074D7", "Davenport"),
  ("42074D8", "West Davenport"),
  ("42074E1", "Westerlo"),
  ("42074E2", "Rensselaerville"),
  ("42074E3", "Middleburgh"),
  ("42074E4", "Breakabeen"),
  ("42074E5", "Summit"),
  ("42074E6", "Charlotteville"),
  ("42074E7", "Schenevus"),
  ("42074E8", "Milford"),
  ("42074F1", "Altamont"),
  ("42074F2", "Gallupville"),
  ("42074F3", "Schoharie"),
  ("42074F4", "Cobleskill"),
  ("42074F5", "Richmondville"),
  ("42074F6", "South Valley"),
  ("42074F7", "Westford"),
  ("42074F8", "Cooperstown"),
  ("42074G1", "Rotterdam Junction"),
  ("42074G2", "Duanesburg"),
  ("42074G3", "Esperance"),
  ("42074G4", "Carlisle"),
  ("42074G5", "Sharon Springs"),
  ("42074G6", "Sprout Brook"),
  ("42074G7", "East Springfield"),
  ("42074G8", "Richfield Springs"),
  ("42074H1", "Pattersonville"),
  ("42074H2", "Amsterdam"),
  ("42074H3", "Tribes Hill"),
  ("42074H4", "Randall"),
  ("42074H5", "Canajoharie"),
  ("42074H6", "Fort Plain"),
  ("42074H7", "Van Hornesville"),
  ("42074H8", "Jordanville"),
  ("42075A1", "Corbett"),
  ("42075A2", "Readburn"),
  ("42075A3", "Cannonsville Reservoir"),
  ("42075A4", "Deposit"),
  ("42075A5", "Gulf Summit"),
  ("42075A6", "Windsor"),
  ("42075A7", "Binghamton East"),
  ("42075A8", "Binghamton West"),
  ("42075B1", "Walton East"),
  ("42075B2", "Walton West"),
  ("42075B3", "Trout Creek"),
  ("42075B4", "North Sanford"),
  ("42075B5", "Afton"),
  ("42075B6", "Belden"),
  ("42075B7", "Chenango Forks"),
  ("42075B8", "Castle Creek"),
  ("42075C1", "Treadwell"),
  ("42075C2", "Franklin"),
  ("42075C3", "Unadilla"),
  ("42075C4", "Sidney"),
  ("42075C5", "West Bainbridge"),
  ("42075C6", "Brisben"),
  ("42075C7", "Greene"),
  ("42075C8", "Whitney Point"),
  ("42075D1", "Oneonta"),
  ("42075D2", "Otego"),
  ("42075D3", "Gilbertsville"),
  ("42075D4", "Guilford"),
  ("42075D5", "Oxford"),
  ("42075D6", "Tyner"),
  ("42075D7", "Smithville Flats"),
  ("42075D8", "Willet"),
  ("42075E1", "Mount Vision"),
  ("42075E2", "Morris"),
  ("42075E3", "New Berlin South"),
  ("42075E4", "Holmesville"),
  ("42075E5", "Norwich"),
  ("42075E6", "East Pharsalia"),
  ("42075E7", "Pitcher"),
  ("42075E8", "Cincinnatus"),
  ("42075F1", "Hartwick"),
  ("42075F2", "Edmeston"),
  ("42075F3", "New Berlin North"),
  ("42075F4", "Sherburne"),
  ("42075F5", "Earlville"),
  ("42075F6", "Otselic"),
  ("42075F7", "South Otselic"),
  ("42075F8", "Cuyler"),
  ("42075G1", "Schuyler Lake"),
  ("42075G2", "Unadilla Forks"),
  ("42075G3", "Brookfield"),
  ("42075G4", "Hubbardsville"),
  ("42075G5", "Hamilton"),
  ("42075G6", "West Eaton"),
  ("42075G7", "Erieville"),
  ("42075G8", "DeRuyter"),
  ("42075H1", "Millers Mills"),
  ("42075H2", "West Winfield"),
  ("42075H3", "Cassville"),
  ("42075H4", "Oriskany Falls"),
  ("42075H5", "Munnsville"),
  ("42075H6", "Morrisville"),
  ("42075H7", "Cazenovia"),
  ("42075H8", "Oran"),
  ("42076A1", "Endicott"),
  ("42076A2", "Apalachin"),
  ("42076A3", "Owego"),
  ("42076A4", "Barton"),
  ("42076A5", "Waverly"),
  ("42076A6", "Wellsburg"),
  ("42076A7", "Elmira"),
  ("42076A8", "Seeley Creek"),
  ("42076B1", "Maine"),
  ("42076B2", "Newark Valley"),
  ("42076B3", "Candor"),
  ("42076B4", "Spencer"),
  ("42076B5", "Van Etten"),
  ("42076B6", "Erin"),
  ("42076B7", "Horseheads"),
  ("42076B8", "Big Flats"),
  ("42076C1", "Lisle"),
  ("42076C2", "Richford"),
  ("42076C3", "Speedsville"),
  ("42076C4", "Willseyville"),
  ("42076C5", "West Danby"),
  ("42076C6", "Alpine"),
  ("42076C7", "Montour Falls"),
  ("42076C8", "Beaver Dams"),
  ("42076D1", "Marathon"),
  ("42076D2", "Harford"),
  ("42076D3", "Dryden"),
  ("42076D4", "Ithaca East"),
  ("42076D5", "Ithaca West"),
  ("42076D6", "Mecklenburg"),
  ("42076D7", "Burdett"),
  ("42076D8", "Reading Center"),
  ("42076E1", "McGraw"),
  ("42076E2", "Cortland"),
  ("42076E3", "Groton"),
  ("42076E4", "West Groton"),
  ("42076E5", "Ludlowville"),
  ("42076E6", "Trumansburg"),
  ("42076E7", "Lodi"),
  ("42076E8", "Dundee"),
  ("42076F1", "Truxton"),
  ("42076F2", "Homer"),
  ("42076F3", "Sempronius"),
  ("42076F4", "Moravia"),
  ("42076F5", "Genoa"),
  ("42076F6", "Sheldrake"),
  ("42076F7", "Ovid"),
  ("42076F8", "Dresden"),
  ("42076G1", "Tully"),
  ("42076G2", "Otisco Valley"),
  ("42076G3", "Spafford"),
  ("42076G4", "Owasco"),
  ("42076G5", "Scipio Center"),
  ("42076G6", "Union Springs"),
  ("42076G7", "Romulus"),
  ("42076G8", "Geneva South"),
  ("42076H1", "Jamesville"),
  ("42076H2", "South Onondaga"),
  ("42076H3", "Marcellus"),
  ("42076H4", "Skaneateles"),
  ("42076H5", "Auburn"),
  ("42076H6", "Cayuga"),
  ("42076H7", "Seneca Falls"),
  ("42076H8", "Geneva North"),
  ("42077A1", "Caton"),
  ("42077A2", "Addison"),
  ("42077A3", "Borden"),
  ("42077A4", "Woodhull"),
  ("42077A5", "Troupsburg"),
  ("42077A6", "Rexville"),
  ("42077A7", "Whitesville"),
  ("42077A8", "Wellsville South"),
  ("42077B1", "Corning"),
  ("42077B2", "Campbell"),
  ("42077B3", "Rathbone"),
  ("42077B4", "Cameron"),
  ("42077B5", "South Canisteo"),
  ("42077B6", "Greenwood"),
  ("42077B7", "Andover"),
  ("42077B8", "Wellsville North"),
  ("42077C1", "Bradford"),
  ("42077C2", "Savona"),
  ("42077C3", "Bath"),
  ("42077C4", "Towlesville"),
  ("42077C5", "Canisteo"),
  ("42077C6", "Hornell"),
  ("42077C7", "Alfred"),
  ("42077C8", "West Almond"),
  ("42077D1", "Wayne"),
  ("42077D2", "Hammondsport"),
  ("42077D3", "Rheims"),
  ("42077D4", "Avoca"),
  ("42077D5", "Haskinville"),
  ("42077D6", "Arkport"),
  ("42077D7", "Canaseraga"),
  ("42077D8", "Birdsall"),
  ("42077E1", "Keuka Park"),
  ("42077E2", "Pulteney"),
  ("42077E3", "Prattsburg"),
  ("42077E4", "Naples"),
  ("42077E5", "Wayland"),
  ("42077E6", "Dansville"),
  ("42077E7", "Ossian"),
  ("42077E8", "Nunda"),
  ("42077F1", "Penn Yan"),
  ("42077F2", "Potter"),
  ("42077F3", "Middlesex"),
  ("42077F4", "Bristol Springs"),
  ("42077F5", "Springwater"),
  ("42077F6", "Conesus"),
  ("42077F7", "Sonyea"),
  ("42077F8", "Mount Morris"),
  ("42077G1", "Stanley"),
  ("42077G2", "Rushville"),
  ("42077G3", "Canandaigua Lake"),
  ("42077G4", "Bristol Center"),
  ("42077G5", "Honeoye"),
  ("42077G6", "Livonia"),
  ("42077G7", "Geneseo"),
  ("42077G8", "Leicester"),
  ("42077H1", "Phelps"),
  ("42077H2", "Clifton Springs"),
  ("42077H3", "Canandaigua"),
  ("42077H4", "Victor"),
  ("42077H5", "Honeoye Falls"),
  ("42077H6", "Rush"),
  ("42077H7", "Caledonia"),
  ("42077H8", "Le Roy"),
  ("42078A1", "Allentown"),
  ("42078A2", "Bolivar"),
  ("42078A3", "Portville"),
  ("42078A4", "Olean"),
  ("42078A5", "Knapp Creek"),
  ("42078A6", "Limestone"),
  ("42078A7", "Red House"),
  ("42078A8", "Steamburg"),
  ("42078B1", "Belmont"),
  ("42078B2", "Friendship"),
  ("42078B3", "Cuba"),
  ("42078B4", "Hinsdale"),
  ("42078B5", "Humphrey"),
  ("42078B6", "Salamanca"),
  ("42078B7", "Little Valley"),
  ("42078B8", "Randolph"),
  ("42078C1", "Angelica"),
  ("42078C2", "Black Creek"),
  ("42078C3", "Rawson"),
  ("42078C4", "Franklinville"),
  ("42078C5", "Ashford"),
  ("42078C6", "Ellicottville"),
  ("42078C7", "Cattaraugus"),
  ("42078C8", "New Albion"),
  ("42078D1", "Fillmore"),
  ("42078D2", "Houghton"),
  ("42078D3", "Freedom"),
  ("42078D4", "Delevan"),
  ("42078D5", "West Valley"),
  ("42078D6", "Ashford Hollow"),
  ("42078D7", "Collins Center"),
  ("42078D8", "Gowanda"),
  ("42078E1", "Portageville"),
  ("42078E2", "Pike"),
  ("42078E3", "Bliss"),
  ("42078E4", "Arcade"),
  ("42078E5", "Sardinia"),
  ("42078E6", "Springville"),
  ("42078E7", "Langford"),
  ("42078E8", "North Collins"),
  ("42078F1", "Castile"),
  ("42078F2", "Warsaw"),
  ("42078F3", "Johnsonburg"),
  ("42078F4", "Strykersville"),
  ("42078F5", "Holland"),
  ("42078F6", "Colden"),
  ("42078F7", "Hamburg"),
  ("42078F8", "Eden"),
  ("42078G1", "Wyoming"),
  ("42078G2", "Dale"),
  ("42078G3", "Attica"),
  ("42078G4", "Cowlesville"),
  ("42078G5", "East Aurora"),
  ("42078G6", "Orchard Park"),
  ("42078G7", "Buffalo SE"),
  ("42078H1", "Stafford"),
  ("42078H2", "Batavia South"),
  ("42078H3", "Alexander"),
  ("42078H4", "Corfu"),
  ("42078H5", "Clarence"),
  ("42078H6", "Lancaster"),
  ("42078H7", "Buffalo NE"),
  ("42078H8", "Buffalo NW"),
  ("42079A1", "Ivory"),
  ("42079A2", "Jamestown"),
  ("42079A3", "Lakewood"),
  ("42079A4", "Panama"),
  ("42079A5", "North Clymer"),
  ("42079A6", "Clymer"),
  ("42079B1", "Kennedy"),
  ("42079B2", "Gerry"),
  ("42079B3", "Ellery Center"),
  ("42079B4", "Chautauqua"),
  ("42079B5", "Sherman"),
  ("42079B6", "South Ripley"),
  ("42079C1", "Cherry Creek"),
  ("42079C2", "Hamlet"),
  ("42079C3", "Cassadaga"),
  ("42079C4", "Hartfield"),
  ("42079D1", "Perrysburg"),
  ("42079D2", "Forestville"),
  ("42079D3", "Dunkirk"),
  ("42079E1", "Farnham"),
  ("43073A3", "Shushan"),
  ("43073A4", "Cambridge"),
  ("43073A5", "Schuylerville"),
  ("43073A6", "Quaker Springs"),
  ("43073A7", "Saratoga Springs"),
  ("43073A8", "Middle Grove"),
  ("43073B3", "Salem"),
  ("43073B4", "Cossayuna"),
  ("43073B5", "Fort Miller"),
  ("43073B6", "Gansevoort"),
  ("43073B7", "Corinth"),
  ("43073B8", "Porter Corners"),
  ("43073C3", "West Pawlet"),
  ("43073C4", "Hartford"),
  ("43073C5", "Hudson Falls"),
  ("43073C6", "Glens Falls"),
  ("43073C7", "Lake Luzerne"),
  ("43073C8", "Conklingville"),
  ("43073D3", "Granville"),
  ("43073D4", "Fort Ann"),
  ("43073D5", "Putnam Mountain"),
  ("43073D6", "Lake George"),
  ("43073D7", "Warrensburg"),
  ("43073D8", "Stony Creek"),
  ("43073E3", "Thorn Hill"),
  ("43073E4", "Whitehall"),
  ("43073E5", "Shelving Rock"),
  ("43073E6", "Bolton Landing"),
  ("43073E7", "The Glen"),
  ("43073E8", "Johnsburg"),
  ("43073F4", "Putnam"),
  ("43073F5", "Silver Bay"),
  ("43073F6", "Brant Lake"),
  ("43073F7", "Chestertown"),
  ("43073F8", "North Creek"),
  ("43073G4", "Ticonderoga"),
  ("43073G5", "Graphite"),
  ("43073G6", "Pharaoh Mountain"),
  ("43073G7", "Schroon Lake"),
  ("43073G8", "Minerva"),
  ("43073H4", "Crown Point"),
  ("43073H5", "Eagle Lake"),
  ("43073H6", "Paradox Lake"),
  ("43073H7", "Blue Ridge"),
  ("43073H8", "Cheney Pond"),
  ("43074A1", "Galway"),
  ("43074A2", "Broadalbin"),
  ("43074A3", "Gloversville"),
  ("43074A4", "Peck Lake"),
  ("43074A5", "Lassellsville"),
  ("43074A6", "Oppenheim"),
  ("43074A7", "Little Falls"),
  ("43074A8", "Herkimer"),
  ("43074B1", "Edinburg"),
  ("43074B2", "Northville"),
  ("43074B3", "Jackson Summit"),
  ("43074B4", "Caroga Lake"),
  ("43074B5", "Canada Lake"),
  ("43074B6", "Stratford"),
  ("43074B7", "Salisbury"),
  ("43074B8", "Middleville"),
  ("43074C1", "Ohmer Mountain"),
  ("43074C2", "Hope Falls"),
  ("43074C3", "Cathead Mountain"),
  ("43074C4", "Whitehouse"),
  ("43074C5", "Tomany Mountain"),
  ("43074C6", "Morehouse Lake"),
  ("43074C7", "Jerseyfield Lake"),
  ("43074C8", "Ohio"),
  ("43074D1", "Harrisburg"),
  ("43074D2", "Griffin"),
  ("43074D3", "Wells"),
  ("43074D4", "Lake Pleasant"),
  ("43074D5", "Piseco Lake"),
  ("43074D6", "Hoffmeister"),
  ("43074D7", "Morehouseville"),
  ("43074D8", "Black Creek Lake"),
  ("43074E1", "Bakers Mills"),
  ("43074E2", "South Pond Mountain"),
  ("43074E3", "Kunjamuk River"),
  ("43074E4", "Page Mountain"),
  ("43074E5", "Spruce Lake"),
  ("43074E6", "Spruce Lake Mountain"),
  ("43074E7", "Honnedaga Lake"),
  ("43074E8", "Bisby Lakes"),
  ("43074F1", "Gore Mountain"),
  ("43074F2", "Bullhead Mountain"),
  ("43074F3", "Indian Lake"),
  ("43074F4", "Snowy Mountain"),
  ("43074F5", "Wakely Mountain"),
  ("43074F6", "Mount Tom"),
  ("43074F7", "Limekiln Lake"),
  ("43074F8", "Old Forge"),
  ("43074G1", "Dutton Mountain"),
  ("43074G2", "Bad Luck Mountain"),
  ("43074G3", "Rock Lake"),
  ("43074G4", "Blue Mountain Lake"),
  ("43074G5", "Sargent Ponds"),
  ("43074G6", "Raquette Lake"),
  ("43074G8", "Big Moose"),
  ("43074H1", "Vanderwhacker Mountain"),
  ("43074H2", "Newcomb"),
  ("43074H3", "Dun Brook Mountain"),
  ("43074H4", "Deerland"),
  ("43074H5", "Forked Lake"),
  ("43074H6", "Brandreth Lake"),
  ("43074H7", "Nehasane Lake"),
  ("43074H8", "Beaver River"),
  ("43075A1", "Ilion"),
  ("43075A2", "Utica East"),
  ("43075A3", "Utica West"),
  ("43075A4", "Clinton"),
  ("43075A5", "Vernon"),
  ("43075A6", "Oneida"),
  ("43075A7", "Canastota"),
  ("43075A8", "Manlius"),
  ("43075B1", "Newport"),
  ("43075B2", "South Trenton"),
  ("43075B3", "Oriskany"),
  ("43075B4", "Rome"),
  ("43075B5", "Verona"),
  ("43075B6", "Sylvan Beach"),
  ("43075B7", "Jewell"),
  ("43075B8", "Cleveland"),
  ("43075C1", "Hinckley"),
  ("43075C2", "Remsen"),
  ("43075C3", "North Western"),
  ("43075C4", "Westernville"),
  ("43075C5", "Lee Center"),
  ("43075C6", "Camden East"),
  ("43075C7", "Camden West"),
  ("43075C8", "Panther Lake"),
  ("43075D1", "North Wilmurt"),
  ("43075D2", "Forestport"),
  ("43075D3", "Boonville"),
  ("43075D4", "West Leyden"),
  ("43075D5", "Point Rock"),
  ("43075D6", "Florence"),
  ("43075D7", "Westdale"),
  ("43075D8", "Williamstown"),
  ("43075E1", "McKeever"),
  ("43075E2", "Woodgate"),
  ("43075E3", "Port Leyden"),
  ("43075E4", "Constableville"),
  ("43075E5", "High Market"),
  ("43075E6", "North Osceola"),
  ("43075E7", "Redfield"),
  ("43075E8", "Orwell"),
  ("43075F1", "Thendara"),
  ("43075F2", "Copper Lake"),
  ("43075F3", "Brantingham"),
  ("43075F4", "Glenfield"),
  ("43075F5", "Page"),
  ("43075F6", "Sears Pond"),
  ("43075F7", "Worth Center"),
  ("43075F8", "Boylston Center"),
  ("43075G1", "Stillwater Mountain"),
  ("43075G2", "Number Four"),
  ("43075G3", "Crystal Dale"),
  ("43075G4", "Lowville"),
  ("43075G5", "West Lowville"),
  ("43075G6", "New Boston"),
  ("43075G7", "Barnes Corners"),
  ("43075G8", "Rodman"),
  ("43075H1", "Stillwater"),
  ("43075H2", "Soft Maple Reservoir"),
  ("43075H3", "Belfort"),
  ("43075H4", "Croghan"),
  ("43075H5", "Carthage"),
  ("43075H6", "Copenhagen"),
  ("43075H7", "Rutland Center"),
  ("43075H8", "Watertown"),
  ("43076A1", "Syracuse East"),
  ("43076A2", "Syracuse West"),
  ("43076A3", "Camillus"),
  ("43076A4", "Jordan"),
  ("43076A5", "Weedsport"),
  ("43076A6", "Montezuma"),
  ("43076A7", "Savannah"),
  ("43076A8", "Lyons"),
  ("43076B1", "Cicero"),
  ("43076B2", "Brewerton"),
  ("43076B3", "Baldwinsville"),
  ("43076B4", "Lysander"),
  ("43076B5", "Cato"),
  ("43076B6", "Victory"),
  ("43076B7", "Wolcott"),
  ("43076B8", "Rose"),
  ("43076C1", "Mallory"),
  ("43076C2", "Central Square"),
  ("43076C3", "Pennellville"),
  ("43076C4", "Fulton"),
  ("43076C5", "Hannibal"),
  ("43076C6", "Fair Haven"),
  ("43076D1", "Dugway"),
  ("43076D2", "Mexico"),
  ("43076D3", "New Haven"),
  ("43076D4", "Oswego East"),
  ("43076E1", "Richland"),
  ("43076E2", "Pulaski"),
  ("43076F1", "Sandy Creek"),
  ("43076F2", "Ellisburg"),
  ("43076G1", "Adams"),
  ("43076G2", "Henderson"),
  ("43076H1", "Sackets Harbor"),
  ("43076H2", "Henderson Bay"),
  ("43077A1", "Newark"),
  ("43077A2", "Palmyra"),
  ("43077A3", "Macedon"),
  ("43077A4", "Fairport"),
  ("43077A5", "Pittsford"),
  ("43077A6", "West Henrietta"),
  ("43077A7", "Clifton"),
  ("43077A8", "Churchville"),
  ("43077B1", "Sodus"),
  ("43077B2", "Williamson"),
  ("43077B3", "Ontario"),
  ("43077B4", "Webster"),
  ("43077B5", "Rochester East"),
  ("43077B6", "Rochester West"),
  ("43077B7", "Spencerport"),
  ("43077B8", "Brockport"),
  ("43077C7", "Hilton"),
  ("43077C8", "Hamlin"),
  ("43078A1", "Byron"),
  ("43078A2", "Batavia North"),
  ("43078A3", "Oakfield"),
  ("43078A4", "Akron"),
  ("43078A5", "Wolcottsville"),
  ("43078A6", "Clarence Center"),
  ("43078A7", "Tonawanda East"),
  ("43078A8", "Tonawanda West"),
  ("43078B1", "Holley"),
  ("43078B2", "Albion"),
  ("43078B3", "Knowlesville"),
  ("43078B4", "Medina"),
  ("43078B5", "Gasport"),
  ("43078B6", "Lockport"),
  ("43078B7", "Cambria"),
  ("43078B8", "Ransomville"),
  ("43078C1", "Kendall"),
  ("43078C2", "Kent"),
  ("43078C3", "Ashwood"),
  ("43078C4", "Lyndonville"),
  ("43078C5", "Barker"),
  ("43078C6", "Newfane"),
  ("44073A4", "Port Henry"),
  ("44073A5", "Witherbee"),
  ("44073A6", "Underwood"),
  ("44073A7", "Dix Mountain"),
  ("44073A8", "Mount Marcy"),
  ("44073B3", "Vergennes West"),
  ("44073B4", "Westport"),
  ("44073B5", "Elizabethtown"),
  ("44073B6", "Rocky Peak Ridge"),
  ("44073B7", "Keene Valley"),
  ("44073B8", "North Elba"),
  ("44073C3", "Charlotte"),
  ("44073C4", "Willsboro"),
  ("44073C5", "Lewis"),
  ("44073C6", "Jay Mountain"),
  ("44073C7", "Keene"),
  ("44073C8", "Lake Placid"),
  ("44073D4", "Port Douglass"),
  ("44073D5", "Clintonville"),
  ("44073D6", "Au Sable Forks"),
  ("44073D7", "Wilmington"),
  ("44073D8", "Franklin Falls"),
  ("44073E4", "Keeseville"),
  ("44073E5", "Peru"),
  ("44073E6", "Peasleeville"),
  ("44073E7", "Redford"),
  ("44073E8", "Alder Brook"),
  ("44073F4", "Plattsburgh"),
  ("44073F5", "Morrisonville"),
  ("44073F6", "Dannemora"),
  ("44073F7", "Moffitsville"),
  ("44073F8", "Lyon Mountain"),
  ("44073G4", "Beekmantown"),
  ("44073G5", "West Chazy"),
  ("44073G6", "Jericho"),
  ("44073G7", "Ellenburg Mountain"),
  ("44073G8", "Ellenburg Center"),
  ("44073H3", "Rouses Point"),
  ("44073H4", "Champlain"),
  ("44073H5", "Mooers"),
  ("44073H6", "Altona"),
  ("44073H7", "Ellenburg Depot"),
  ("44073H8", "Churubusco"),
  ("44074A1", "Mount Adams"),
  ("44074A2", "Santanoni Peak"),
  ("44074A3", "Kempshall Mountain"),
  ("44074A4", "Grampus Lake"),
  ("44074A5", "Little Tupper Lake"),
  ("44074A6", "Sabattis"),
  ("44074A7", "Wolf Mountain"),
  ("44074A8", "Five Ponds"),
  ("44074B1", "Street Mountain"),
  ("44074B2", "Ampersand Lake"),
  ("44074B3", "Stony Creek Mountain"),
  ("44074B4", "Tupper Lake"),
  ("44074B5", "Piercefield"),
  ("44074B6", "Long Tom Mountain"),
  ("44074B7", "Cranberry Lake"),
  ("44074B8", "Newton Falls"),
  ("44074C1", "McKenzie Mountain"),
  ("44074C2", "Saranac Lake"),
  ("44074C3", "Upper Saranac Lake"),
  ("44074C4", "Derrick"),
  ("44074C5", "Mount Matumbla"),
  ("44074C6", "Childwold"),
  ("44074C7", "Brother Ponds"),
  ("44074C8", "Tooley Pond"),
  ("44074D1", "Bloomingdale"),
  ("44074D2", "Gabriels"),
  ("44074D3", "Saint Regis Mountain"),
  ("44074D4", "Bay Pond"),
  ("44074D5", "Augerhole Falls"),
  ("44074D6", "Carry Falls Reservoir"),
  ("44074D7", "Stark"),
  ("44074D8", "Albert Marsh"),
  ("44074E1", "Loon Lake"),
  ("44074E2", "Debar Mountain"),
  ("44074E3", "Meacham Lake"),
  ("44074E4", "Meno"),
  ("44074E5", "Lake Ozonia"),
  ("44074E6", "Sylvan Falls"),
  ("44074E7", "Rainbow Falls"),
  ("44074E8", "Colton"),
  ("44074F1", "Ragged Lake"),
  ("44074F2", "Owls Head"),
  ("44074F3", "Lake Titus"),
  ("44074F4", "Santa Clara"),
  ("44074F5", "Saint Regis Falls"),
  ("44074F6", "Nicholville"),
  ("44074F7", "Parishville"),
  ("44074F8", "Potsdam"),
  ("44074G1", "Brainardsville"),
  ("44074G2", "Chasm Falls"),
  ("44074G3", "Malone"),
  ("44074G4", "Bangor"),
  ("44074G5", "Brushton"),
  ("44074G6", "North Lawrence"),
  ("44074G7", "Brasher Falls"),
  ("44074G8", "Norfolk"),
  ("44074H1", "Chateaugay"),
  ("44074H2", "Burke"),
  ("44074H3", "Constable"),
  ("44074H4", "Fort Covington"),
  ("44074H5", "Bombay"),
  ("44074H6", "Hogansburg"),
  ("44074H7", "Raquette River"),
  ("44074H8", "Massena"),
  ("44075A1", "Oswegatchie SE"),
  ("44075A2", "Oswegatchie SW"),
  ("44075A3", "Remington Corners"),
  ("44075A4", "Natural Bridge"),
  ("44075A5", "North Wilna"),
  ("44075A6", "Deferiet"),
  ("44075A7", "Black River"),
  ("44075A8", "Brownville"),
  ("44075B1", "Oswegatchie"),
  ("44075B2", "Fine"),
  ("44075B3", "Harrisville"),
  ("44075B4", "Lake Bonaparte"),
  ("44075B5", "Antwerp"),
  ("44075B6", "Philadelphia"),
  ("44075B7", "Theresa"),
  ("44075B8", "La Fargeville"),
  ("44075C1", "Degrasse"),
  ("44075C2", "South Edwards"),
  ("44075C3", "Edwards"),
  ("44075C4", "Gouverneur"),
  ("44075C5", "Natural Dam"),
  ("44075C6", "Muskellunge Lake"),
  ("44075C7", "Redwood"),
  ("44075C8", "Alexandria Bay"),
  ("44075D1", "West Pierrepont"),
  ("44075D2", "Hermon"),
  ("44075D3", "Bigelow"),
  ("44075D4", "Richville"),
  ("44075D5", "Pope Mills"),
  ("44075D6", "Hammond"),
  ("44075E1", "Pierrepont"),
  ("44075E2", "Canton"),
  ("44075E3", "Rensselaer Falls"),
  ("44075E4", "Heuvelton"),
  ("44075E5", "Edwardsville"),
  ("44075F1", "West Potsdam"),
  ("44075F2", "Morley"),
  ("44075F3", "Lisbon"),
  ("44075G1", "Chase Mills"),
  ("44075G2", "Waddington"),
  ("44076A1", "Dexter"),
  ("44076A2", "Chaumont"),
  ("44076A3", "Cape Vincent South"),
  ("44076B1", "Clayton"),
  ]

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
