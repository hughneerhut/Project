class Order:
    def __init__(self):
        self._orderedDate = None
        self._fromSuburb = None
        self._fromState = None
        self._toSuburb = None
        self._toState = None
        self._toPCode = None
        self._itemQty = None
        self._volume = None
        self._weight = None

    @property
    def ordered_date(self):
        return self._orderedDate

    @ordered_date.setter
    def ordered_date(self, value):
        self._orderedDate = value

    @property
    def from_suburb(self):
        return self._fromSuburb

    @from_suburb.setter
    def from_suburb(self, value):
        self._fromSuburb = value

    @property
    def from_state(self):
        return self._fromState

    @from_state.setter
    def from_state(self, value):
        self._fromState = value

    @property
    def to_suburb(self):
        return self.toSuburb

    @to_suburb.setter
    def to_suburb(self, value):
        self._toSuburb = value

    @property
    def to_state(self):
        return self.toState

    @to_state.setter
    def to_state(self, value):
        self._toState = value

    @property
    def to_pcode(self):
        return self._toPCode

    @to_pcode.setter
    def to_pcode(self, value):
        self._toPCode = value

    @property
    def item_qty(self):
        return self._itemQty

    @item_qty.setter
    def item_qty(self, value):
        self._itemQty = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value


#c = C()
#c.x = 'foo'  # setter called
#foo = c.x    # getter called
#del c.x      # deleter called