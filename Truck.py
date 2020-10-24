class Truck:
    def __init__(self, orders="[]", origin="", stops="[]", destination=""):
        self._orders = orders
        self._origin = origin
        self._stop = stops
        self._destination = destination

    @property
    def orders(self):
        return self._orders

    @orders.setter
    def orders(self, value):
        self._orders = value

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin= value

    @property
    def stops(self):
        return self._stops

    @stops.setter
    def stops(self, value):
        self._stops = value

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value