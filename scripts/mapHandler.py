import folium as folium


def findGeocode(city):
    from geopy.exc import GeocoderTimedOut
    from geopy.geocoders import Nominatim
    import numpy as np
    # try and catch is used to overcome
    # the exception thrown by geolocator
    # using geocodertimedout
    try:
        # Specify the user_agent as your
        # app name it should not be none
        geolocator = Nominatim(user_agent="your_app_name")
        return geolocator.geocode(city)

    except GeocoderTimedOut:
        return findGeocode(city)


def getLatAndLong(cityName):
    import numpy as np
    loc = findGeocode(cityName)

    if loc != None:
        return loc.latitude, loc.longitude
    else:
        return 0, 0


def createMap(cityName):
    import folium
    latitude, longitude = getLatAndLong(cityName)
    # adjust position of view of the map
    my_map = folium.Map(
        location=[13, 16],
        zoom_start=2,
    )

    # set marker for the offer
    # html = popup_html(offer)
    # popup = folium.Popup(folium.Html(html, script=True), max_width=500)
    folium.Marker(location=[latitude, longitude],
                  icon=folium.Icon(color='blue', icon='university', prefix='fa')).add_to(my_map)

    return my_map


# ---------------------

def setColorOfOffer(offerType):
    match offerType:
        case "COBE":
            return "#bb5afd"
        case "FCFS":
            return "#fdfa5a"
        case "PreAC":
            return "#5afdb2"
        case default:
            return "#FFFFFF"


def popup_html(offerList, offerCount, city):
    left_col_color = "#dfe6e3"
    right_col_color = "#ffffff"

    rows = ""
    for offer in offerList:
        color = setColorOfOffer(offer.OfferType)

        row = "<tr>"
        row += '<td style="background-color:' + color + ';"><span>' + offer.RefNo + '</span></td>'
        row += '<td style="background-color:' + color + ';"><span>' + offer.OfferType + '</span></td>'

        button = '<form action="http://127.0.0.1:8000/playground/hello/' + offer.RefNo + '" method="get" ' \
                                                                                         'target="_blank"> <button ' \
                                                                                         'type="submit">Details' \
                                                                                         '</button> </form> '

        row += '<td style = "width: 150px;background-color: ' + color + ';"> ' + button + '</td>'
        row += "</tr>"
        rows += row

    offersInfo = ""
    if offerCount == 1:
        offersInfo = "offer"
    else:
        offersInfo = "offers"

    html = """<!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="../static/css/mapStyles.css"/>
            <h4 class="tableHeader"> """ + str(offerCount) + ' ' + offersInfo + ' in ' + city + """</h4>

        </head>
            <table id="popupTable" class="centerTable">
            <thead>
                  <tr>
                    <th id="RefNoHeader">RefNo</th>
                    <th id="OfferTypeHeader">Type</th>
                    <th id="DetailsHeader">Details</th>
                  </tr>
            </thead>
                <tbody>
                """ + rows + """
                </tbody>
            </table>
        </html>
        """
    return html


def countFrequenciesOfCities(allOffers):
    # Creating an empty dictionary
    freq = {}
    for offer in allOffers:
        if (offer.City in freq):
            freq[offer.City] += 1
        else:
            freq[offer.City] = 1

    return freq


def createMapForMultipleOffers():
    from playground.models import Offer
    allOffers = Offer.objects.all()

    cityFreq = countFrequenciesOfCities(allOffers)

    import folium

    my_map = folium.Map(
        location=[13, 16],
        zoom_start=2,
    )

    for city, counter in cityFreq.items():
        offerList = list(Offer.objects.filter(City=city))

        lat, long = getLatAndLong(city)

        # set marker for the offer
        html = popup_html(offerList, counter, city)
        popup = folium.Popup(folium.Html(html, script=True))
        folium.Marker(location=[lat, long], popup=popup,
                      icon=folium.Icon(color='blue', icon='university', prefix='fa')).add_to(my_map)

    return my_map