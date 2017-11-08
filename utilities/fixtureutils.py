class UserFixture:
    fixtures = ['init_class.yaml', 'init_user.yaml', 'init_email.yaml']


class CustomerFixture:
    fixtures = ['init_customer.yaml']


class CreditCardFixture:
    fixtures = ['init_creditcard.yaml']


class MembershipFixture:
    """
        merge `UserFixture` and `CustomerFixture`
        and add `token` as well
    """
    fixtures = UserFixture.fixtures + \
        CustomerFixture.fixtures + \
        ['init_token.yaml']


class DesignFixture:
    fixtures = ['init_design.yaml', 'init_images.yaml']


class MaterialFixture:
    fixtures = ['init_material.yaml']


class CatalogFixture:
    fixtures = DesignFixture.fixtures + \
        MaterialFixture.fixtures + \
        ['init_product.yaml']


class PromotionFixture:
    fixtures = ['init_promotion.yaml']


class CartFixture:
    fixtures = ['init_order.yaml',
                'init_orderinfo.yaml',
                'init_transportation.yaml']


class AllFixture:
    fixtures = MembershipFixture.fixtures + \
        CreditCardFixture.fixtures + \
        CatalogFixture.fixtures + \
        PromotionFixture.fixtures + \
        CartFixture.fixtures + \
        ['init_site.yaml', 'init_comment.yaml']
