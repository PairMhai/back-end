# Guide

[link](http://toastdriven.com/blog/2011/apr/10/guide-to-testing-in-django/)

# Example test

```python
    from utils.testcaseutils import ImpTestCase
    """
        - run `pre_setup` -> `set_constants` -> `post_setup`
        - self.client is preload
    """

    class LoginTestCase(ImpTestCase):
        fixtures = ['init_xxx.yaml']                     # load fixture (test data)

        def set_constants(self):
            self.data = 'some data'

        def pre_setup(self):
            print("do something")

        def post_setup(self):
            print("do something")

        def test_one(self):
            # response = self.run_post("name of url", body) # run post http
            # response = self.run_get("name of url", args)  # run get http (args must be list)


            # self.assertResponseCode201(response)                                # for test status code (200)
            # self.assertResponseCode200(response)                                # for test status code (201)
            # self.assertResponseCode400(response)                                # for test status code (400)
            # self.assertResponseData(response, 'id', 1)                          # for test value in data key
            # self.assertResponseData2(response, 'user', 'name', 1)               # for test value in data key
            # r_k >> response key, d_k >> dict key
            # self.assertResponseDict(response, r_k, d_k, expected)               # for test dict inside response key
            # self.assertResponseDictKeyExist(response, r_k, d_k, many=False)     # for test dict key inside response key
            # self.assertResponseDictKeyNotExist(response, r_k, d_k, many=False)  # for test dict key inside response key
```
