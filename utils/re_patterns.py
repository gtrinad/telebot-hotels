PATTERN_CITY = r'"type":"CITY".*?"fullName":"(?P<fullName>[^"]+).*?"sourceId":"(?P<sourceId>[^"]+).*?"' \
               r'coordinates":{"lat":"(?P<latitude>-?\d+\.\d+)","long":"(?P<longitude>-?\d+\.\d+)'

PATTERN_PROPERTY = r'"Property","id":"(?P<Property_id>\d+).*?"name":"(?P<name>[^"]+).*?"distanceFromDestination":{' \
                   r'".*?"value":(?P<distanceFromDestination>\d+\.\d+).*?"latitude":(' \
                   r'?P<latitude>-?\d+\.\d+).*?"longitude":(?P<longitude>-?\d+\.\d+).*?"lead":{".*?"amount":(' \
                   r'?P<amount>\d+\.\d{2})'

PATTERN_SUMMARY = r'"propertyRating":{".*?"rating":(?P<rating>\d\.?\d?).*?"PropertyAddress","addressLine":"(' \
                  r'?P<addressLine>[^"]+).*?"LodgingEnrichedMessage","value":"(?P<review_info>[^"]+)'

PATTERN_IMAGES = r'"__typename":"Image","url":"(?P<image>[^"]+)'
