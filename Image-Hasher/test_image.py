import unittest
from Image import Image

class TestImage(unittest.TestCase):

    global Image_obj
    Image_obj = Image(0,0,0,0,0,0,0,0,0)

    def test_set_hash(self):
        image_hash = 122
        Image_obj.set_hash(image_hash)
        self.assertEqual(Image_obj.get_hash(), image_hash)
    
    def test_append_group(self):
        images = list()
        images.append("Image12_76.jpg")
        Image_obj.append_group(images[0])
        self.assertListEqual(images, Image_obj.get_group())
    

if __name__ == '__main__':
    unittest.main()
    