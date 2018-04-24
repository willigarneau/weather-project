
class City(object):

    lon = 0
    lat = 0
    x = 0
    y = 0
    tempC = 0
    name = ""

    def __init__(self, lo, la):
        self.lon = lo
        self.lat = la
        self.x = ((lo + 180.0) * (1920 / 360.0))
        self.y = (((la * -1.0) + 90.0) * (967 / 180.0))
