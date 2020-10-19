class Postcodes:
    def __int__(self, id, postcode, locality, state, long, lat, dc, type, status, sa3, sa3name, sa4, sa4name):
        self._id = id
        self._postcode = postcode
        self._locality = locality
        self._state = state
        self._long = long
        self._lat = lat
        self._dc = dc
        self._type = type
        self._status = status
        self._sa3 = sa3
        self._sa3name = sa3name
        self._sa4 = sa4
        self._sa4name = sa4name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def postcode(self):
        return self._postcode

    @postcode.setter
    def postcode(self, value):
        self._postcode = value

    @property
    def locality(self):
        return self._locality

    @locality.setter
    def locality(self, value):
        self._locality = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

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

    @property
    def dc(self):
        return self._dc

    @dc.setter
    def dc(self, value):
        self._dc = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def sa3(self):
        return self._sa3

    @sa3.setter
    def sa3(self, value):
        self._sa3 = value

    @property
    def sa3name(self):
        return self._sa3name

    @sa3name.setter
    def sa3name(self, value):
        self._sa3name = value

    @property
    def sa4(self):
        return self._sa4

    @sa4.setter
    def sa4(self, value):
        self._sa4 = value

    @property
    def sa4name(self):
        return self._sa4name

    @sa4name.setter
    def ssa4name(self, value):
        self._sa4name = value
