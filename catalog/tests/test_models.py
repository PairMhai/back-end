from django.test import TestCase
from random import uniform, randrange

from catalog.models import Design, Material, Image, Product, Promotion

class ModelsTestCase(TestCase):
    fixtures = ['init_design.yaml',
                'init_images.yaml',
                'init_material.yaml',
                'init_product.yaml',
                'init_promotion.yaml']

    def __init__(self, *args, **kwargs):
        super(ModelsTestCase, self).__init__(*args, **kwargs)


    def setUp(self):
        self.design = Design.objects.get(pk=1)
        self.images = Image.objects.get(pk=1)
        self.material = Material.objects.get(pk=1)

    def test_name_of_design_match_with_images(self):
        """test if the image's name is in correct format"""
        name = self.design.name
        name = name.lower()
        name = name.replace(" ", "-")
        name += ".jpg"
        self.assertEqual(name, self.images.file_name)

    def test_design_has_material(self):
        """test if the design includes a kind of material in the database"""
        self.assertNotEqual(self.design.material, "")

    def test_quantity_material_not_zero(self):
        """test if the quantity of the material is not less than zero"""
        self.assertTrue(self.material.quantity >= 0)
    
    def test_design_must_have_product_id(self):
        designs = Design.objects.all()
        for d in designs:
            self.assertIsNotNone(Product.objects.get(design=d))

    def test_material_must_have_product_id(self):
        materials = Material.objects.all()
        for m in materials:
            self.assertIsNotNone(Product.objects.get(material=m))
