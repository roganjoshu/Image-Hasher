class Image:

    def __init__(self, image_name, date_created, taken_date, image_shape, channels, image_path, location, mod_time, img_size):    #constructor
        self.image_hash = 0
        self.image_name = image_name
        if date_created != 0:
            self.date_created = date_created
        else:
            self.date_created = 0
        self.taken_date = taken_date
        self.image_shape = image_shape
        self.group = list()
        self.is_duplicate = False
        self.image_channels = channels
        self.image_path = image_path
        self.location = location
        self.mod_time = mod_time
        self.img_size = img_size

    # getters
    def get_name(self):
        return self.image_name
    def get_hash(self):
        return self.image_hash
    def get_image_shape(self):
        return self.image_shape
    def get_group(self):
        return self.group
    def get_is_duplicate(self):
        return self.is_duplicate
    def get_image_channels(self):
        return self.image_channels
    def get_date(self):
        return self.date_created
    def get_path(self):
        return self.image_path
    def get_location(self):
        return self.location
    def get_mod_date(self):
        return self.mod_time
    def get_size(self):
        return self.img_size
    def get_date_taken(self):
        return self.taken_date
    def get_ham_value(self):
        return self.ham_value

    # setters
    def set_hash(self, image_hash):
        self.image_hash = image_hash
    def append_group(self, individual):
        self.group.append(individual)      
    def set_is_duplicate(self, flag):
        self.is_duplicate = flag
    def set_ham_distance(self, hamming_value):
        self.ham_value = hamming_value