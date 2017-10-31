from django.test import TestCase
from random import uniform, randrange

from catalog.models import Design, Material, Image, Product, Promotion

class DataTestCase(TestCase):
    fixtures = ['init_design.yaml',
                'init_images.yaml',
                'init_material.yaml',
                'init_product.yaml',
                'init_promotion.yaml']