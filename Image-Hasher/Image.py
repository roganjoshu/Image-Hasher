class Image:

    def __init__(self, image_name, image_creation_date, image_taken_date, image_shape, image_channels, image_path, image_location, image_modification_date, image_size):    #constructor
        self.image_hash = 0
        self.image_name = image_name
        if image_creation_date != 0:
            self.image_creation_date = image_creation_date
        else:
            self.image_creation_date = 0
        self.image_taken_date = image_taken_date
        self.image_shape = image_shape
        self.duplicate_group = list()
        self.is_duplicate = False
        self.is_similar = False
        self.image_channels = image_channels
        self.image_path = image_path
        self.image_location = image_location
        self.image_modification_date = image_modification_date
        self.image_size = image_size
        self.binary_value = ""

    # getters
    def get_image_name(self):
        return self.image_name
    def get_image_hash(self):
        return self.image_hash
    def get_image_shape(self):
        return self.image_shape
    def get_group(self):
        return self.duplicate_group
    def get_is_duplicate(self):
        return self.is_duplicate
    def get_is_similar(self):
        return self.is_similar
    def get_image_channels(self):
        return self.image_channels
    def get_creation_date(self):
        return self.image_creation_date
    def get_path(self):
        return self.image_path
    def get_image_location(self):
        return self.image_location
    def get_modification_date(self):
        return self.image_modification_date
    def get_image_size(self):
        return self.image_size
    def get_date_taken(self):
        return self.image_taken_date
    def get_bitstring_hash(self):
        return self.binary_value

    # setters
    def set_hash(self, image_hash):
        self.image_hash = image_hash
    def append_group(self, individual):
        self.duplicate_group.append(individual)      
    def set_is_duplicate(self, flag):
        self.is_duplicate = flag
    def set_is_similar(self, flag):
        self.is_similar = flag
    def set_binary_value(self, binary_value):
        self.binary_value = binary_value