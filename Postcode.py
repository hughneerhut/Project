class Postcode:
    def __int__(self, postcode, long, lat):
        self._postcode = postcode
        self._long = long
        self._lat = lat

    @property
    def postcode(self):
        return self._postcode

    @postcode.setter
    def postcode(self, value):
        self._postcode = value

    @property
    def long(self):
        return self._long

    @long.setter
    def long(self, value):
        self._long = value

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value):
        self._lat = value

