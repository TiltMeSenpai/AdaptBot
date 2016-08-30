spec = ("Keyword", "Type?", "Location")
def parse(Keyword, Location, Type=None):
    return "{}, {}, {}".format(Keyword, Location, Type)

Keyword = [
        "weather"
]

Type = [
    "snow",
    "rain",
    "wind",
    "sleet",
    "sun"
]

Location = [
    "Seattle",
    "San Francisco",
    "Tokyo"
]
