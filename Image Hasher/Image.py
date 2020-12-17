class Image:

    #constructor
    def __init__(self, image_name, date_created, image_shape, channels):
        self.image_hash = 0
        self.image_name = image_name
        if date_created != 0:
            self.date_created = date_created
        else:
            self.date_created = 0
        self.image_shape = image_shape
        self.group = list()
        self.is_duplicate = False
        self.image_channels = channels

    # getters
    def get_name(self):
        return self.image_name
    def get_hash(self):
        return self.image_hash
    def get_image(self):
        return self.image
    def get_image_shape(self):
        return self.image_shape
    def get_group(self):
        return self.group
    def get_is_duplicate(self):
        return is_duplicate
    def get_image_channels(self):
        return image_channels

    # setters
    def set_hash(self, image_hash):
        self.image_hash = image_hash
    def set_image(self, image):
        self.image = image
    def append_group(self, individual):
        self.group.append(individual)
    def set_is_duplicate(self, flag):
        self.is_duplicate = flag