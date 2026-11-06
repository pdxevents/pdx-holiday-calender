import csv
import re
from datetime import date, datetime, timedelta

OUT = "Portland-Holiday-Events-2026.ics"
DTSTAMP = "20261106T132053Z"

MODA = "Moda Center, 1 N Center Ct St, Portland, OR 97227"
ALADDIN = "Aladdin Theater, 3017 SE Milwaukie Ave, Portland, OR 97202"
SCHNITZ = "Arlene Schnitzer Concert Hall, 1037 SW Broadway, Portland, OR"
NEWMARK = "Newmark Theatre, 1111 SW Broadway, Portland, OR 97205"
KELLER = "Keller Auditorium, 222 SW Clay St, Portland, OR 97201"
REVHALL = "Revolution Hall, 1300 SE Stark St, Portland, OR 97214"
SQUARE = "Pioneer Courthouse Square, 701 SW 6th Ave, Portland, OR 97204"
ZOO = "Oregon Zoo, 4001 SW Canyon Rd, Portland, OR 97221"
PIR = "Portland International Raceway, 1940 N Victory Blvd, Portland, OR 97217"
OCC = "Oregon Convention Center, Hall D, 777 NE Martin Luther King Jr Blvd, Portland, OR 97232"
EXPO = "Portland Expo Center, 2025 N Expo Rd, Portland, OR 97217"
BAZAAR = "1715 NW 17th Ave, Portland, OR"
RIVERPLACE = "RiverPlace Marina, Portland, OR"
GLEASON = "M. James Gleason Boat Ramp, Portland, OR"

S_EVEROUT = "https://everout.com/portland/holidays/"
S_STAY = "https://www.stayportland.com/guide/portland-fall-winter-holidays"
S_STAY2 = "https://www.stayportland.com/guide/portland-events-festivals"
S_WW = "https://www.wweek.com/culture/2026/11/03/get-busy-what-to-do-in-portland-nov-410-2026/"
S_KOA = "https://portland.kidsoutandabout.com/content/101-ideas-holiday-family-fun-portland"
S_SHIPS = "https://www.christmasships.org/parade-schedule"
S_OBT = "https://www.obt.org/event/the-nutcracker-2026-27/"
S_PEACOCK = "https://peacocklane.org/"
S_OCC = "https://www.oregoncc.org/attend/events/2026/12/crafty-wonderland-holiday-art-craft-market-2026"
S_EXPO = "https://www.expocenter.org/events/portland-holiday-market-0"
S_ZOO = "https://thrillzing.com/seasonal-events/zoolights-2026-oregon-zoo/"
S_TC = "https://thechristmas.com/blogs/events/portland-christmas-lights"
S_LIGHTS = "https://portland-christmas-lights.pages.dev/events"
S_AC_POPS = "https://www.allclassical.org/?p=111029"
S_AC_GOSPEL = "https://www.allclassical.org/?p=111028"
S_ORS_GOSPEL = "https://orsymphony.org/productions/2627/gospel-christmas-2026/"
S_ORS_POPS = "https://www.orsymphony.org/productions/2627/holiday-pops-spectacular"
S_ORS_BRASS = "https://orsymphony.org/productions/2627/holiday-brass"
S_ORS_HOME = "https://www.orsymphony.org/productions/2627/home-alone-in-concert"
S_ORS_NINTH = "https://www.orsymphony.org/productions/2627/new-years-eve-with-beethovens-ninth"
S_ZOO_LIGHTS = "https://www.oregonzoo.org/lights"
S_ZOO_BREW = "https://www.oregonzoo.org/brewlights"
S_ORHF = "https://orhf.org/holiday-express/"
S_GROTTO = "https://thegrotto.org/christmas-festival-of-lights/"
S_TUBA = "https://www.thesquarepdx.org/event/35th-annual-tuba-christmas-concert/"
S_PITTOCK = "https://pittockmansion.org/exhibits/"
S_OBT_TEMPLE = "https://www.oregonbuddhisttemple.com/craft-fair"
S_FOODGIFT = "https://pdxparent.com/pdx-holiday-fun/"
S_FOODGIFT2 = "https://www.thecraftmap.com/fair/37th-annual-holiday-food-gift-festival-nov-13th-15th-hillsboro-or"


def eo(slug):
    return f"https://everout.com/portland/events/{slug}/"


NO_TIME = "Time not listed in the sources, so this is an all-day entry. Check before going."

# (date, weekday, start "HH:MM" or None, end or None, title, location, notes, source)
E = [
    ("2026-11-06", "Fri", "10:00", "19:00", "Portland Holiday Market", EXPO, "", S_EXPO),
    ("2026-11-07", "Sat", "10:00", "19:00", "Portland Holiday Market", EXPO, "", S_EXPO),
    ("2026-11-08", "Sun", "10:00", "18:00", "Portland Holiday Market", EXPO, "", S_EXPO),
    ("2026-11-08", "Sun", "20:00", None, "Derek Hough: Dance for the Holidays", SCHNITZ, "", eo("derek-hough-dance-for-the-holidays/e249490")),
    ("2026-11-10", "Tue", "09:00", "10:30", "Stimson Lumber Tree Arrival", SQUARE, "Free. The city's tree arrives at the Square.", S_WW),
    ("2026-11-12", "Thu", "19:30", None, "Jim Brickman", "Patricia Reser Center for the Arts, 12625 SW Crescent St, Beaverton, OR 97005", "", eo("jim-brickman-piano-sensation/e260328")),
    ("2026-11-13", "Fri", "17:30", "21:30", "BrewLights (21+)", ZOO, "General entry 5:30 PM, early entry 4:30 PM. Taps close 9 PM.", S_ZOO_BREW),
    ("2026-11-14", "Sat", "17:30", "21:30", "BrewLights (21+)", ZOO, "General entry 5:30 PM, early entry 4:30 PM. Taps close 9 PM.", S_ZOO_BREW),
    ("2026-11-13", "Fri", "11:00", "18:00", "Holiday Food & Gift Festival", "Westside Commons, 801 NE 34th Ave, Hillsboro, OR", "37th annual, Nov 13-15 at a new location. Hours are listed for Nov 13 only, so check Saturday and Sunday hours. Venue from The Craft Map: " + S_FOODGIFT2, S_FOODGIFT),
    ("2026-11-14", "Sat", "09:00", "15:00", "Oregon Buddhist Temple Holiday Craft Fair", "Oregon Buddhist Temple, 3720 SE 34th Ave, Portland, OR 97202", "11th annual. Free entry.", S_OBT_TEMPLE),
    ("2026-11-15", "Sun", None, None, "ZooLights Member Preview Night", ZOO, "Oregon Zoo members. " + NO_TIME, S_ZOO_LIGHTS),
    ("2026-11-16", "Mon", None, None, "Pittock Mansion: Home for the Holidays opens", "Pittock Mansion, 3229 NW Pittock Dr, Portland, OR 97210", "Holidays from Around the World, through Jan 10, 2027. Closed Thanksgiving, Christmas Day and New Year's Day. " + NO_TIME, S_PITTOCK),
    ("2026-11-16", "Mon", None, None, "ZooLights Sensory Friendly Night", ZOO, NO_TIME, S_ZOO_LIGHTS),
    ("2026-11-20", "Fri", "10:00", "18:00", "Plucky Maidens Holiday Fest", "Oaks Park Dance Pavilion, 7805 SE Oaks Park Way, Portland, OR 97202", "Free.", eo("plucky-maidens-holiday-fest/e262024")),
    ("2026-11-21", "Sat", "10:00", "18:00", "Plucky Maidens Holiday Fest", "Oaks Park Dance Pavilion, 7805 SE Oaks Park Way, Portland, OR 97202", "Free.", eo("plucky-maidens-holiday-fest/e262024")),
    ("2026-11-20", "Fri", "16:30", "20:30", "ZooLights opens", ZOO, "Runs through Jan 3, 2027, from 4:30 PM. Closed Nov 24-26 and Dec 25. Closing time varies by night. Jan 1-2 are 21+.", S_ZOO_LIGHTS),
    ("2026-11-20", "Fri", "17:00", "21:00", "Silverton Christmas Market opens", "Oregon Garden, 879 W Main St, Silverton, OR 97381", "Most nights through Dec 31, 5-9 PM. Popular nights sell out, so check open dates when booking.", eo("silverton-christmas-market/e261641")),
    ("2026-11-20", "Fri", None, None, "'Twas the Night Before Nutcracker opens (21+)", "Can Can's Paris Theatre, 6 SW 3rd Ave, Portland, OR 97204", "Runs on select dates through Jan 3, 2027. " + NO_TIME, eo("can-cans-twas-the-night-before-nutcracker/e261638")),
    ("2026-11-27", "Fri", "16:00", "17:00", "Christmas Ships: Vancouver Santa Escort", "Grant Street Pier, Vancouver, WA", "Combined fleet to Vancouver Waterfront. Schedule can change for weather or safety.", S_SHIPS),
    ("2026-11-27", "Fri", "16:30", "23:00", "Winter Wonderland opens", PIR, "Drive-through nightly through Dec 31. Mon-Thu 5-10 PM, Fri-Sun 4:30-11 PM, Dec 18-25 4:30-11 PM. No drive-through Nov 29-Dec 1.", S_STAY),
    ("2026-11-27", "Fri", "17:00", "21:30", "Grotto Christmas Festival of Lights opens", "The Grotto, 8840 NE Skidmore St, Portland, OR 97220", "Nightly 5-9:30 PM through Dec 30, closed Dec 25. Grounds close at 10 PM. Entrance at NE 85th and Sandy Blvd.", S_GROTTO),
    ("2026-11-27", "Fri", "17:30", "18:45", "42nd Annual Tree Lighting Ceremony", SQUARE, "Community sing-along with Santa.", S_STAY),
    ("2026-11-27", "Fri", "20:00", None, "The Storm Large Holiday Ordeal (Night 1)", ALADDIN, "", eo("the-storm-large-holiday-ordeal/e258693")),
    ("2026-11-27", "Fri", "10:00", None, "Holiday Express steam train begins", "Oregon Rail Heritage Center, 2250 SE Water Ave, Portland, OR 97214", "Fri-Sun through Dec 27, plus Dec 21-23. No trains Dec 24-25. Departures at 10, 11:30, 1, 2:30, 4, 5:30 and 7, but not every departure runs every day, so check the schedule. Arrive 20 minutes early.", S_ORHF),
    ("2026-11-27", "Fri", None, None, "A Christmas Celebration: Portland Choir & Orchestra", NEWMARK, "With Nathan Pacheco. Multiple shows Nov 27-28. " + NO_TIME, eo("a-christmas-celebration-portland-choir-orchestra-with-nathan-pacheco/e257195")),
    ("2026-11-28", "Sat", "13:00", "19:00", "Inaugural Holiday Bazaar Brewfest (21+)", "Crystal Ballroom, 1332 W Burnside St, Portland, OR 97209", "", eo("inaugural-holiday-bazaar-brewfest/e256356")),
    ("2026-11-28", "Sat", "15:30", None, "Trans-Siberian Orchestra (matinee)", MODA, "The Ghosts of Christmas Eve.", eo("trans-siberian-orchestra-the-ghosts-of-christmas-eve/e255450")),
    ("2026-11-28", "Sat", "20:00", None, "Trans-Siberian Orchestra (evening)", MODA, "The Ghosts of Christmas Eve.", eo("trans-siberian-orchestra-the-ghosts-of-christmas-eve/e255450")),
    ("2026-11-28", "Sat", "20:00", None, "The Storm Large Holiday Ordeal (Night 2)", ALADDIN, "", eo("the-storm-large-holiday-ordeal/e258693")),
    ("2026-11-28", "Sat", None, None, "Scandinavian Christmas Goat Market", "Norse Hall, 111 NE 11th Ave, Portland, OR", NO_TIME, S_KOA),
    ("2026-11-28", "Sat", None, None, "Black Nativity opens", "Alberta Abbey, 126 NE Alberta St, Portland, OR 97211", "Multiple shows through Dec 6. " + NO_TIME, eo("black-nativity/e261195")),
    ("2026-11-29", "Sun", "16:15", "21:30", "Bike the Lights at Winter Wonderland", PIR, "", S_STAY2),
    ("2026-11-30", "Mon", "16:15", "21:30", "Lights & Leashes at Winter Wonderland", PIR, "Dog walk through the lights. Also Dec 1.", S_STAY),
    ("2026-11-30", "Mon", "19:00", None, "Jake Shimabukuro: Holidays in Hawai'i", NEWMARK, "", eo("jake-shimabukuro-holidays-in-hawai-i/e258358")),
    ("2026-12-01", "Tue", "16:15", "21:30", "Lights & Leashes at Winter Wonderland", PIR, "Dog walk through the lights.", S_STAY),
    ("2026-12-01", "Tue", "20:00", None, "A John Waters Christmas", ALADDIN, "", eo("a-john-waters-christmas/e242479")),
    ("2026-12-03", "Thu", "16:00", "23:00", "Portland Night Market (Dec 3-6)", "100 SE Alder St, Portland, OR", "Listed as 4-11 PM. Hours can differ by day.", S_STAY2),
    ("2026-12-04", "Fri", "16:00", "20:00", "Beaverton Winter Lights & Tree Lighting", "Beaverton City Park, 12500 SW 3rd St, Beaverton, OR 97005", "", S_TC),
    ("2026-12-04", "Fri", "17:00", "20:00", "Multnomah Village Holiday Gala", "Multnomah Village, Portland, OR", "Free.", S_LIGHTS),
    ("2026-12-04", "Fri", None, None, "NOT-Cracker opens", NEWMARK, "Multiple shows Dec 4-6. " + NO_TIME, eo("not-cracker/e257201")),
    ("2026-12-05", "Sat", "14:00", None, "The Nutcracker opens (Oregon Ballet Theatre)", KELLER,
     "All shows: Dec 5 2 & 7:30; Dec 6 2; Dec 11 7:30; Dec 12 2 & 7:30; Dec 13 2; Dec 19 2 & 7:30; Dec 20 2 & 7:30; Dec 21 2 & 7:30; Dec 22 2 & 7:30; Dec 23 2 & 7:30; Dec 24 noon.", S_OBT),
    ("2026-12-05", "Sat", "20:00", None, "Matt Rogers: This Time It's Really Christmas", ALADDIN, "", eo("matt-rogers-this-time-its-really-christmas-tour/e255433")),
    ("2026-12-05", "Sat", None, None, "Portland Bazaar opens", BAZAAR, "Dec 5-6, 12-13, 19-20. Preview hour at 10 AM on Dec 5. " + NO_TIME, S_STAY2),
    ("2026-12-05", "Sat", None, None, "Breakfast With Santa at Edgefield", "McMenamins Edgefield, 2126 SW Halsey St, Troutdale, OR 97060", "Also Dec 6. " + NO_TIME, eo("breakfast-with-santa/e260146")),
    ("2026-12-05", "Sat", "19:30", None, "Gospel Christmas (Oregon Symphony)", SCHNITZ, "Oregon Symphony lists 7:30 PM. A ticket reseller lists 7 PM. Also Dec 6 at 4 PM.", S_ORS_GOSPEL),
    ("2026-12-06", "Sun", "16:00", None, "Gospel Christmas (Oregon Symphony)", SCHNITZ, "", S_AC_GOSPEL),
    ("2026-12-06", "Sun", "20:00", None, "Choir! Choir! Choir! Un-SILENT NIGHT sing-along", REVHALL, "", eo("choir-choir-choir-un-silent-night-an-epic-holiday-sing-along/e239560")),
    ("2026-12-08", "Tue", "19:00", None, "In the Christmas Mood: Glenn Miller Orchestra", NEWMARK, "", eo("in-the-christmas-mood-with-the-glenn-miller-orchestra/e234172")),
    ("2026-12-09", "Wed", "19:30", None, "Merry-achi Christmas: Mariachi Sol de Mexico", SCHNITZ, "Date and time from EverOut. Kids Out and About lists Dec 6, so confirm with the venue.", eo("merry-achi-christmas-with-mariachi-sol-de-mexico-r-de-jose-hernandez/e237817")),
    ("2026-12-10", "Thu", None, None, "Multnomah Village Hanukkah Celebration", "Multnomah Village, Portland, OR", NO_TIME, S_KOA),
    ("2026-12-11", "Fri", "17:00", "21:00", "Crafty Wonderland First Pick Party", OCC, "Timed tickets. Venue is cashless.", S_OCC),
    ("2026-12-11", "Fri", "17:30", "22:00", "Portland Holiday Brew Fest (21+)", SQUARE, "Taps close 9:30 PM.", S_STAY),
    ("2026-12-11", "Fri", "20:00", None, "Christmas with CeCe Winans", SCHNITZ, "", eo("christmas-with-cece-winans/e248398")),
    ("2026-12-11", "Fri", None, None, "Portland Gay Men's Chorus: Cool Yule opens", NEWMARK, "EverOut lists multiple dates from Dec 11. " + NO_TIME, eo("portland-gay-mens-chorus-presents-cool-yule/e259430")),
    ("2026-12-12", "Sat", "10:00", "17:00", "Crafty Wonderland Holiday Market", OCC, "Timed entry. Venue is cashless.", S_OCC),
    ("2026-12-12", "Sat", "12:00", "22:00", "Portland Holiday Brew Fest (21+)", SQUARE, "Taps close 9:30 PM.", S_STAY),
    ("2026-12-12", "Sat", "14:00", None, "Holiday Pops Spectacular (Oregon Symphony)", SCHNITZ, "Also Dec 12 at 7:30 PM and Dec 13 at 2 PM.", S_ORS_POPS),
    ("2026-12-12", "Sat", "19:30", None, "Holiday Pops Spectacular (Oregon Symphony)", SCHNITZ, "", S_ORS_POPS),
    ("2026-12-12", "Sat", "18:00", "20:00", "Christmas on the Campground", "5414 SE Duke St, Portland, OR 97206", "Live Nativity at 6 and 7 PM.", S_TC),
    ("2026-12-12", "Sat", None, None, "ScanFair Nordic Christmas Market", "Nordic Northwest, Portland, OR", NO_TIME, S_KOA),
    ("2026-12-13", "Sun", "10:00", "17:00", "Crafty Wonderland Holiday Market", OCC, "Timed entry. Venue is cashless.", S_OCC),
    ("2026-12-13", "Sun", "18:00", "20:00", "Christmas on the Campground", "5414 SE Duke St, Portland, OR 97206", "Live Nativity at 6 and 7 PM.", S_TC),
    ("2026-12-13", "Sun", "14:00", None, "Holiday Pops Spectacular (Oregon Symphony)", SCHNITZ, "", S_ORS_POPS),
    ("2026-12-13", "Sun", None, None, "ScanFair Nordic Christmas Market", "Nordic Northwest, Portland, OR", NO_TIME, S_KOA),
    ("2026-12-15", "Tue", "18:00", "22:00", "Peacock Lane opens (pedestrian-only)", "SE Peacock Ln, between SE Stark and SE Belmont, Portland, OR 97214", "Lights Dec 15-31, 6-10 PM. One banner on the official site says 11 PM. Pedestrian-only Dec 15 and 16.", S_PEACOCK),
    ("2026-12-15", "Tue", "20:00", None, "JD McPherson: SOCKS Rock N' Roll Christmas", ALADDIN, "", eo("jd-mcpherson-socks-a-rock-n-roll-christmas-tour/e256196")),
    ("2026-12-16", "Wed", "18:00", "22:00", "Peacock Lane (pedestrian-only)", "SE Peacock Ln, between SE Stark and SE Belmont, Portland, OR 97214", "", S_PEACOCK),
    ("2026-12-17", "Thu", "19:30", None, "The Jinkx & DeLa Holiday Show", SCHNITZ, "", eo("the-jinkx-dela-holiday-show/e247954")),
    ("2026-12-17", "Thu", "19:30", None, "Holiday Brass (Oregon Symphony)", "Rose Auditorium, South Salem High School, Salem, OR", "In Salem, per the Oregon Symphony. EverOut listed the Schnitzer in Portland.", S_ORS_BRASS),
    ("2026-12-18", "Fri", "16:00", "23:00", "Portland Night Market (Dec 18-19)", "100 SE Alder St, Portland, OR", "Listed as 4-11 PM. Hours can differ by day.", S_STAY2),
    ("2026-12-19", "Sat", "19:30", None, "Snow Bar Chorale", REVHALL, "", eo("snow-bar-chorale/e250926")),
    ("2026-12-19", "Sat", None, None, "Portland Saturday Market final day of 2026", "Portland Saturday Market, 2 SW Naito Pkwy, Portland, OR", NO_TIME, S_STAY),
    ("2026-12-19", "Sat", "13:30", "15:00", "35th Annual Tuba Christmas Concert", SQUARE, "Free.", S_TUBA),
    ("2026-12-19", "Sat", "19:30", None, "Home Alone in Concert (Oregon Symphony)", SCHNITZ, "Film with the score played live. Also Dec 20 at 2 PM.", S_ORS_HOME),
    ("2026-12-20", "Sun", "14:00", None, "Home Alone in Concert (Oregon Symphony)", SCHNITZ, "Film with the score played live.", S_ORS_HOME),
    ("2026-12-30", "Wed", "19:30", None, "New Year's Eve with Beethoven's Ninth (Oregon Symphony)", SCHNITZ, "Also Dec 31 at 7:30 PM.", S_ORS_NINTH),
    ("2026-12-31", "Thu", "19:30", None, "New Year's Eve with Beethoven's Ninth (Oregon Symphony)", SCHNITZ, "", S_ORS_NINTH),
    ("2026-12-30", "Wed", "19:30", None, "A Magical Cirque Christmas", KELLER, "", eo("a-magical-cirque-christmas/e249545")),
    ("2026-11-25", "Wed", None, None, "The Silver Belles opens (Broadway Rose)", "Broadway Rose Theatre Company", "Listed Nov 25-Dec 20. Showtimes not listed. " + NO_TIME, S_KOA),
    ("2026-11-27", "Fri", None, None, "Rotary Tree Lighting", "Esther Short Park & Vancouver Waterfront, Vancouver, WA", NO_TIME, S_KOA),
    ("2026-11-27", "Fri", None, None, "62nd Annual Tree Lighting Festival", "Millennium Plaza Park", NO_TIME, S_KOA),
    ("2026-11-27", "Fri", None, None, "Portland European Bazaar", BAZAAR, NO_TIME, S_KOA),
    ("2026-11-28", "Sat", None, None, "Portland European Bazaar", BAZAAR, NO_TIME, S_KOA),
    ("2026-11-28", "Sat", None, None, "Cinnamon Bear Breakfast Cruise begins", "Portland Spirit, Salmon Street Springs Dock, Portland, OR", "Listed Nov 28-Dec 27. Sailing dates not listed. " + NO_TIME, S_KOA),
    ("2026-11-29", "Sun", None, None, "Winter Village at Orenco Station opens", "Jerry Willey Plaza, Orenco Station", "Listed through Jan 10, 2027. " + NO_TIME, S_KOA),
    ("2026-12-02", "Wed", None, None, "Bethany Village Tree Lighting & Holiday Market", "4720 NW Bethany Blvd, Portland, OR", NO_TIME, S_KOA),
    ("2026-12-02", "Wed", None, None, "Tomaseen Foley's A Celtic Christmas", "Patricia Reser Center for the Arts, 12625 SW Crescent St, Beaverton, OR 97005", NO_TIME, S_KOA),
    ("2026-12-03", "Thu", None, None, "Wilsonville Community Tree Lighting", "Town Center Park, Wilsonville, OR", NO_TIME, S_KOA),
    ("2026-12-03", "Thu", None, None, "Washougal Lighted Christmas Parade & Tree Lighting", "Reflection Plaza, Washougal, WA", NO_TIME, S_KOA),
    ("2026-12-05", "Sat", None, None, "Gladstone Holiday Market & Tree Lighting", "Gladstone Community Center, Gladstone, OR", NO_TIME, S_KOA),
    ("2026-12-05", "Sat", None, None, "West Linn Holiday Parade", "Historic Willamette Main Street area, West Linn, OR", NO_TIME, S_KOA),
    ("2026-12-05", "Sat", None, None, "Troutdale Windy Wonderland", "Mayor's Square City Park, Troutdale, OR", NO_TIME, S_KOA),
    ("2026-12-06", "Sun", None, None, "Troutdale Windy Wonderland", "Mayor's Square City Park, Troutdale, OR", NO_TIME, S_KOA),
    ("2026-12-05", "Sat", None, None, "Santa Sing-Along at Broadway Rose", "Broadway Rose Theatre Company", NO_TIME, S_KOA),
    ("2026-12-05", "Sat", None, None, "Candlelight Tour at Newell Pioneer Village", "Newell Pioneer Village", NO_TIME, S_KOA),
    ("2026-12-06", "Sun", None, None, "Happy Valley Tree Lighting Ceremony", "Happy Valley City Hall, Happy Valley, OR", NO_TIME, S_KOA),
    ("2026-12-10", "Thu", None, None, "Handel's Messiah opens (Portland Baroque Orchestra)", "Portland, OR", "Listed Dec 10-13. Concert venue and showtimes not listed. " + NO_TIME, S_KOA),
    ("2026-12-11", "Fri", None, None, "Kalani Pe'a: Hawaiian Christmas", "Patricia Reser Center for the Arts, 12625 SW Crescent St, Beaverton, OR 97005", NO_TIME, S_KOA),
    ("2026-12-11", "Fri", None, None, "Yuletide Tea at Newell Pioneer Village", "Newell Pioneer Village", "Also Dec 12. " + NO_TIME, S_KOA),
    ("2026-12-12", "Sat", None, None, "Angels on Wheels Toy Run", PIR, "NW Corvette Association. " + NO_TIME, S_KOA),
    ("2026-12-12", "Sat", None, None, "A Nutcracker Tea opens (Northwest Dance Theatre)", "Portland Community College Performing Arts Center", "Listed Dec 12-20. Showtimes not listed. " + NO_TIME, S_KOA),
]

SHIPS = [
    ("2026-12-03", "Thu", "19:00", "21:00", GLEASON, "Combined fleet: Gleason Boat Ramp to Vancouver Waterfront."),
    ("2026-12-04", "Fri", "19:00", "21:00", GLEASON, "Combined fleet: Gleason Boat Ramp to North Portland Harbor."),
    ("2026-12-05", "Sat", "18:00", "20:30", "Port of Camas-Washougal, WA", "Combined fleet: Camas, Washougal, Steamboat Landing Park."),
    ("2026-12-07", "Mon", "19:00", "21:00", RIVERPLACE, "Willamette: RiverPlace to Johns Landing/Fremont Bridge. Columbia: Gleason to Washington Shores/Wintler Park."),
    ("2026-12-08", "Tue", "19:00", "21:00", RIVERPLACE, "Willamette: RiverPlace to Milwaukie. Columbia: Gleason to I-205/Steamboat Landing/164th Ave."),
    ("2026-12-09", "Wed", "19:00", "21:00", RIVERPLACE, "Willamette: RiverPlace to Johns Landing/Fremont Bridge. Columbia: Gleason to North Portland Harbor."),
    ("2026-12-11", "Fri", "19:00", "21:30", RIVERPLACE, "Willamette: RiverPlace to Milwaukie/Oregon Yacht Club, until 9:30 PM. Columbia: Gleason to Vancouver Waterfront/Hayden Bay, until 9 PM."),
    ("2026-12-12", "Sat", "18:00", "20:00", "St. Helens Public Dock, St. Helens, OR", "Combined fleet: St. Helens to Columbia City/Washington shoreline."),
    ("2026-12-13", "Sun", "16:30", "21:00", "JJ Collins Memorial Park, Scappoose, OR", "Combined fleet: Scappoose/Multnomah Channel to Willamette River."),
    ("2026-12-15", "Tue", "19:00", "21:00", RIVERPLACE, "Willamette: RiverPlace to Milwaukie. Columbia: Gleason to North Portland Harbor."),
    ("2026-12-16", "Wed", "19:00", "21:00", RIVERPLACE, "Willamette: RiverPlace to Johns Landing/Fremont Bridge. Columbia: Gleason to Vancouver Waterfront/Hayden Bay."),
    ("2026-12-17", "Thu", "19:00", "21:00", RIVERPLACE, "Willamette: RiverPlace to Milwaukie. Columbia: Gleason to I-205/Steamboat Landing/164th Ave, until 8 PM."),
    ("2026-12-18", "Fri", "19:00", "21:00", RIVERPLACE, "Willamette: RiverPlace to Johns Landing/Fremont Bridge. Columbia: Gleason to Washington Shores/Wintler Park."),
    ("2026-12-19", "Sat", "16:30", "20:00", RIVERPLACE, "Combined fleet: RiverPlace to Lake Oswego."),
    ("2026-12-20", "Sun", "17:00", "19:00", RIVERPLACE, "Combined fleet: RiverPlace to St. Johns Bridge/Cathedral Park."),
]
for d, w, s, e, loc, n in SHIPS:
    E.append((d, w, s, e, "Christmas Ships Parade", loc, n + " Schedule can change for weather or safety.", S_SHIPS))

E.sort(key=lambda x: (x[0], x[2] or "00:00", x[4]))


def esc(t):
    return t.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")


def fold(line):
    raw = line.encode("utf-8")
    parts, limit = [], 75
    while len(raw) > limit:
        cut = limit
        while raw[cut] & 0xC0 == 0x80:
            cut -= 1
        parts.append(raw[:cut])
        raw = raw[cut:]
        limit = 74
    parts.append(raw)
    return "\r\n ".join(p.decode("utf-8") for p in parts)


L = [
    "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Claude//Portland Holiday Events 2026//EN",
    "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:Portland Holiday Events 2026",
    "X-WR-TIMEZONE:America/Los_Angeles", "X-APPLE-CALENDAR-COLOR:#C0392B",
    "BEGIN:VTIMEZONE", "TZID:America/Los_Angeles",
    "BEGIN:DAYLIGHT", "TZOFFSETFROM:-0800", "TZOFFSETTO:-0700", "TZNAME:PDT",
    "DTSTART:20070311T020000", "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU", "END:DAYLIGHT",
    "BEGIN:STANDARD", "TZOFFSETFROM:-0700", "TZOFFSETTO:-0800", "TZNAME:PST",
    "DTSTART:20071104T020000", "RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU", "END:STANDARD",
    "END:VTIMEZONE",
]

rows, seen = [], set()
for day, wk, start, end, title, loc, notes, src in E:
    d = date.fromisoformat(day)
    assert d.strftime("%a") == wk, (day, wk, title)
    assert d >= date(2026, 11, 5), title
    uid = re.sub(r"[^a-z0-9]+", "-", f"{day} {start or 'allday'} {title}".lower()).strip("-")
    assert uid not in seen, uid
    seen.add(uid)
    desc = "\n".join(x for x in [notes, f"Source: {src}"] if x)
    L += ["BEGIN:VEVENT", f"UID:{uid}@portland-holiday-2026", f"DTSTAMP:{DTSTAMP}"]
    if start:
        s = datetime.fromisoformat(f"{day}T{start}")
        en = datetime.fromisoformat(f"{day}T{end}") if end else s + timedelta(hours=2)
        assert en > s, title
        L += [f"DTSTART;TZID=America/Los_Angeles:{s:%Y%m%dT%H%M%S}",
              f"DTEND;TZID=America/Los_Angeles:{en:%Y%m%dT%H%M%S}"]
    else:
        L += [f"DTSTART;VALUE=DATE:{d:%Y%m%d}", f"DTEND;VALUE=DATE:{d + timedelta(days=1):%Y%m%d}"]
    L += [f"SUMMARY:{esc(title)}", f"LOCATION:{esc(loc)}", f"DESCRIPTION:{esc(desc)}",
          f"URL:{src}", "TRANSP:TRANSPARENT", "END:VEVENT"]
    rows.append([day, wk, start or "not listed", title, loc, src])

L.append("END:VCALENDAR")
with open(OUT, "w", encoding="utf-8", newline="") as f:
    f.write("\r\n".join(fold(x) for x in L) + "\r\n")

with open("holiday_events_check.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)

print(len(E), "events;", sum(1 for e in E if not e[2]), "all-day")
