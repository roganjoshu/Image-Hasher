class Image:

    #constructor
    def __init__(self, image_name, date_created, image_shape):
        self.image_hash = 0
        self.image_name = image_name
        if date_created != 0:
            self.date_created = date_created
        else:
            self.date_created = 0
        self.image_shape = image_shape
        self.is_duplicate_tag = False

    # getters
    def get_name(self):
        return self.image_name
    def get_hash(self):
        return self.image_hash
    def get_image(self):
        return self.image
    def get_image_shape(self):
        return self.image_shape
    def get_tag(self):
        return self.is_duplicate_tag

    # setters
    def set_hash(self, image_hash):
        self.image_hash = image_hash
    def set_image(self, image):
        self.image = image
    def set_tag(self, is_duplicate_tag):
        self.is_duplicate_tag = duplicate_tag