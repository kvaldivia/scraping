from scrapy import Item, Field, String

class Gadget(Item):
    name = Field()
    brand = Field()
    specs = Field()

    def __init__(self, name, brand, specs=None):
        if specs is None:
            self.specs = Field()
        self.name = name
        self.brand = brand
        super(Gadget, self).__init__(name=self.name, brand=self.brand, specs=self.specs)

class Phone(Gadget):
    specs = Field()

    def __init__(self, name, brand, specs=None):
        super(Phone, self).__init__(*args, **kwargs);
        self.specs = Phone.Specs()


    class Specs(Field):
        network = Field()
        height = Field()
        width = Field()
        weight = Field()
        sim = Field()
        operating_system = Field()
        chipset = Field()
        cpu = Field()
        gpu = Field()
        card_slot = Field()
        internal_storage = Field()
        primary_camera = Field()
        secondary_camera = Field()
        camera_features =Field()
        video_res = Field()
        loudspeaker = Field()
        jack = Field()
        wlan = Field()
        bluetooth = Field()
        gps = Field()
        radio = Field()
        usb = Field()
        battery = Field()
        talk_time = Field()
        colors = Field()
        price = Field()

class Brand():
    name = Field()
