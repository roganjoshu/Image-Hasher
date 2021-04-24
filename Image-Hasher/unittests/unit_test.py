import unittest
from Image import Image

class test_Image(unittest.TestCase):

    
    def test_set_image_name(self):
        img = Image("josh.jpg", "120712", "120612", "1920x1080", "RGB", "C:/USER/JOSH/PICTURES", "PICTURES", "120712", 217.85)
        assert img.image_name == "josh.jpg"

    def test_set_image_hash(self):
        img = Image("josh.jpg", "120712", "120612", "1920x1080", "RGB", "C:/USER/JOSH/PICTURES", "PICTURES", "120712", 217.85)
        img.set_hash(20189)
        assert img.image_hash == 20189
    
    def test_get_image_shape(self):
        img = Image("josh.jpg", "120712", "120612", "1920x1080", "RGB", "C:/USER/JOSH/PICTURES", "PICTURES", "120712", 217.85)
        assert img.get_image_shape() == "1920x1080"

    def test_append_group(self):
        img = Image("josh.jpg", "120712", "120612", "1920x1080", "RGB", "C:/USER/JOSH/PICTURES", "PICTURES", "120712", 217.85)
        img2 = Image("alice.jpg", "130611", "110611", "2560x1440", "RGB", "C:/USER/JOSH/PICTURES", "PICTURES", "130611", 859.85)
        img2.append_group(img)
        assert img2.duplicate_group[0].get_image_name() == img.get_image_name()

    def test_get_group(self):
        img = Image("josh.jpg", "120712", "120612", "1920x1080", "RGB", "C:/USER/JOSH/PICTURES", "PICTURES", "120712", 217.85)
        img2 = Image("alice.jpg", "130611", "110611", "2560x1440", "RGB", "C:/USER/JOSH/PICTURES", "PICTURES", "130611", 859.85)
        img2.append_group(img)
        assert img2.get_group()[0].image_name == "josh.jpg"

    def test_get_image_hash(self):
        img = Image("josh.jpg", "120712", "120612", "1920x1080", "RGB", "C:/USER/JOSH/PICTURES", "PICTURES", "120712", 217.85)
        img.image_hash = 2023897
        self.assertEqual(img.get_image_hash(), 2023897, msg='{0}, {1}'.format(img.get_image_hash(), img.image_hash))

    

if __name__ == '__main__':
    unittest.main