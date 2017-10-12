# Guide

[link](http://toastdriven.com/blog/2011/apr/10/guide-to-testing-in-django/)

# Example test

```python
    from Backend.test_utils import ImpTestCase

    class LoginTestCase(ImpTestCase):
        def setUp(self):
            self.client = APIClient()
            self.data = 'some data'

        def test_one(self):
            response = self.client.post(
                reverse('name of url'),
                self.data,
                format="json"
            )

            # self.assertResponseCode201(response)       # for test status code
            # self.assertResponseCode200(response)       # for test status code
            # self.assertResponseData(response, 'id', 1) # for test value in data key
```
