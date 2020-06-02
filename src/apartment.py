
COL_PLACEHOLDER = "{:<14}"

class Apartment():

    def __init__(self, **kwargs):
        self.type = kwargs.get('type', None)
        self.sqft = kwargs.get('sqft', None)
        self.price = kwargs.get('price', None)
        self.availability = kwargs.get('availability', None)
        self.floorplan = kwargs.get('floorplan', None)

    def __str__(self):
        # attributes = vars(self)
        attributes = [self.floorplan, self.type, self.sqft, self.price, self.availability]
        attributes = [str(a) for a in attributes]
        placeholders = [COL_PLACEHOLDER] * len(attributes)
        return "".join(placeholders).format(*attributes)

    def get_print_header():
        attributes = ["Floorplan", "Type", "SQFT", "Price", "Availability"]
        return "".join([COL_PLACEHOLDER] * len(attributes)).format(*attributes)
