# Index of document
This API using [REST architectural style](REST-description.md) and API framework, I choose [Django REST framework](http://www.django-rest-framework.org).

### Path in APIs document will be like `^xx/yy/zz/(...)$ [name='name']`
1. ^ - start path with root path e.g. localhost/xx/yy/zz
2. & - end of path
3. (...) - dynamic path (it can be some text)
4. [name='...'] - name of the path (for **developer**)

# Testing guideline
[guide](TEST_GUIDE.md)

# [Membership](./membership/README.md)
This app contain all information about user customer and staff.

# [Payment](./payment/README.md)
This app contain all only credit cards of customer.

# [Comment](./comment/README.md)
This app contain api for customer to comment and rate our application

# [Catalog](./catalog/README.md)
This app contain api for catalog **add** **update** **remove** `product` and `promotion`

# Version
This have 1 url `^version$ [name='version']`, This route(url) will return currently version of the API from *setting django* as **JSON** format.

# Announcement
- admin username is `admin`
- admin password is `password123`
