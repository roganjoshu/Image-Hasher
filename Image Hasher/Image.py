class Image:

    #constructor
    def __init__(self, image, image_name, date_created, image_shape):
        self.image = image
        self.image_hash = 0
        self.image_name = image_name
        if date_created != 0:
            self.date_created = date_created
        else:
            self.date_created = 0
        self.image_shape = image_shape

    # getters
    def get_name(self):
        return self.image_name
    def get_hash(self):
        return self.image_hash
    def get_image(self):
        return self.image
    def get_image_shape(self):
        return self.image_shape

    # setters
    def set_hash(self, image_hash):
        self.image_hash = image_hash
    def set_image(self, image):
        self.image = image