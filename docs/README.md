# Index of document

This API using [REST architectural style](REST-description.md) and API framework, I choose [Django REST framework](http://www.django-rest-framework.org).

# Document Template

```markdown
## Name **(vx.x.x)**
- Path: API PATH
- Desciption: DESCRIPTION
1. **Request**
    - method: [`POST`|`GET`|...]
    - body: [none]
    ```json
    ```
2. **Response**
    1. Successfully
        - code: `2XX_XXXXX`
        - body: [none]
        ```json
        ```
    2. Client Error
        - code: `4XX_XXXXX`
        - body: [none]
        ```json
        ```
    3. Server Error
        - code: `5XX_XXXXX`
        - body: [none]
        ```json
        ```
```

## Path in APIs document will be like `^xx/yy/zz/(...)$`

1. ^ - start path with root path e.g. localhost/xx/yy/zz
2. & - end of path

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

# [Cart](./cart/README.md)
This app contain api for `ordering` and getting `transportation`

# Version
This have 1 url `^version$`, This route(url) will return currently version of the API from *setting django* as **JSON** format.

# Announcement
- test admin username is `admin`
- test admin password is `password123`
- test email username is `pairmhai.test@gmail.com`
- test email password is `zkE-PXe-VdA-253`