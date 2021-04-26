from ..Image import Image
import unittest



class test_Image(unittest.TestCase):

    def test_get_image_name(self):
        result = img.get_image_name()
        name = "josh.jpg"
        self.assertEqual(result, name)

    def test_get_image_hash(self):
        d_hash = 9870987
        img.set_hash(d_hash)
        self.assertEqual(d_hash, img.get_image_hash())

    def test_get_image_shape(self):
        result = img.get_image_shape()
        shape = "1920x1080"
        self.assertEqual(shape, result)

    def test_get_group(self):
        img.append_group(img2)
        self.assertEqual(img.get_group()[0].get_image_name(), "Alive.jpg")

    def test_get_is_duplicate(self):
        duplicate_flag = True
        img.set_is_duplicate(duplicate_flag)
        result = img.get_is_duplicate()
        self.assertEqual(result, duplicate_flag)

    def test_get_is_similar(self):
        similar_flag = True
        img.set_is_similar(similar_flag)
        result = img.get_is_similar()
        self.assertEqual(result, similar_flag)

    def test_get_image_channels(self):
        target_channels = "RGB"
        result = img.get_image_channels()
        self.assertEqual(target_channels, result)
    
    def test_get_creation_date(self):
        target_date = "120712"
        result = img.get_creation_date()
        self.assertEqual(target_date, result)
    
    def test_get_path(self):
        target_path = "C:/USER/JOSH/PICTURES"
        result = img.get_path()
        self.assertEqual(target_path, result)

    def test_get_image_location(self):
        target_location = "PICTURES"
        result = img.get_image_location()
        self.assertEqual(target_location, result)

    def test_get_modification_date(self):
        target_mod_date = "120712"
        result = img.get_modification_date()
        self.assertEqual(target_mod_date, result)
    
    def test_get_image_size(self):
        target_size = 217.85
        result = img.get_image_size()
        self.assertEqual(target_size, result)

    def test_get_date_taken(self):
        target_date = "120612"
        result = img.get_date_taken()
        self.assertEqual(target_date, result)

    def test_get_bitstring_hash(self):
        img.set_bitstring_hash("1001010111010100101010110100010101")
        target_bitstring = "1001010111010100101010110100010101"
        result = img.get_bitstring_hash()
        self.assertEqual(target_bitstring, result)
    

    
img = Image("josh.jpg", "120712", "120612", "1920x1080", "RGB", "C:/USER/JOSH/PICTURES", "PICTURES", "120712", 217.85)
img2 = Image("Alive.jpg", "130611", "120611", "2560x1440", "L", "C:/USER/JOSH/PICTURES", "PICTURES", "120611", 874.81)

if __name__ == '__main__':
    unittest.main