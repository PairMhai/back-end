from utilities.testcaseutils import ImpTestCase
from random import uniform, randrange

from cart.models import Order, OrderInfo

from utilities.fixtureutils import AllFixture

class ModelsTestCase(ImpTestCase):
    fixtures = AllFixture.fixtures

    # total_product = models.IntegerField(default=0)
    # final_price = models.DecimalField(
    #     max_digits=8, decimal_places=2, default=0.00)
    # customer = models.ForeignKey(
    #     'membership.Customer',
    #     on_delete=models.CASCADE
    # )
    # creditcard = models.ForeignKey(
    #     'payment.CreditCard',
    #     on_delete=models.CASCADE
    # )
    # transportation = models.ForeignKey(
    #     'Transportation',
    #     on_delete=models.CASCADE
    # )
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def set_constants(self):
        pass
        # self.order_1 = Order.objects.create(total_product=5, final_price=)
        # self.images = OrderInfo.objects.get(pk=1)

    def test_name_of_design_match_with_images(self):
        """test if the image's name is in correct format"""
        pass
        # name = self.design.name
        # name = name.lower()
        # name = name.replace(" ", "-")
        # name += ".jpg"
        # self.assertEqual(name, self.images.file_name)

    def test_design_has_material(self):
        """test if the design includes a kind of material in the database"""
        pass
        # self.assertNotEqual(self.design.material, "")

    def test_quantity_material_not_zero(self):
        """test if the quantity of the material is not less than zero"""
        pass
        # self.assertTrue(self.material.quantity >= 0)

    def test_design_must_have_product_id(self):
        pass
        # designs = Design.objects.all()
        # for d in designs:
        #     self.assertIsNotNone(Product.objects.get(design=d))

    def test_material_must_have_product_id(self):
        pass
        # materials = Material.objects.all()
        # for m in materials:
        #     self.assertIsNotNone(Product.objects.get(material=m))
