# Catalog APIs list and description

1. ^catalog/materials$ [name='material-list'] **(v0.2.2)**
    - List all materials
    1. **Request**
        - method: `GET`
        - body: [none]
    2. **Response**
        1. Successfully
            - code: `200_OK`
            - body:
            ```json
            [
                {
                    "id": 1,
                    "name": "name1",
                    "quantity": 1,
                    "description": "description of name1",
                    "price": "00.00",
                    "color": "color",
                    "image_name": "name1.jpg"
                },
                {
                    "id": 2,
                    "name": "name2",
                    "quantity": 1,
                    "description": "description of name2",
                    "price": "00.00",
                    "color": "color",
                    "image_name": "name2.jpg"
                }
            ]
            ```
2. ^catalog/material/(?P<pk>[0-9]+)$ [name='material-detail'] **(v0.2.2)**
    - Get individual material by `material id`
    1. **Request**
        - method: `GET`
        - body: [none]
    2. **Response**
        1. Successfully
            - code: `200_OK`
            - body:
            ```json
            {
                "id": 1,
                "name": "name1",
                "quantity": 1,
                "description": "description of name1",
                "price": "00.00",
                "color": "color",
                "image_name": "name1.jpg"
            }
            ```
3. ^catalog/designs$ [name='design-list']
    - List all designs
    1. **Request**
        - method: `GET`
        - body: [none]
    2. **Response**
        1. Successfully
            - code: `200_OK`
            - body:
            ```json
            [
                {
                    "id": 1,
                    "name": "name1",
                    "description": "description of name1",
                    "price": "00.00",
                    "images": [
                        {
                            "id": 1,
                            "file_name": "name1.jpg"
                        }
                    ]
                },
                {
                    "id": 2,
                    "name": "name2",
                    "description": "description of name2",
                    "price": "00.00",
                    "images": [
                        {
                            "id": 2,
                            "file_name": "name2.jpg"
                        }
                    ]
                }
            ]
            ```
4. ^catalog/design/(?P<pk>[0-9]+)$ [name='design-detail']
    - Get individual design by `design id`
    1. **Request**
        - method: `GET`
        - body: [none]
    2. **Response**
        1. Successfully
            - code: `200_OK`
            - body:
            ```json
            {
                "id": 1,
                "name": "name1",
                "description": "description of name1",
                "price": "00.00",
                "images": [
                    {
                        "id": 1,
                        "file_name": "name1.jpg"
                    }
                ]
            }
            ```
5. ^catalog/promotions$ [name='promotion-list']
    - List all promotions
    1. **Request**
        - method: `GET`
        - body: [none]
    2. **Response**
        1. Successfully
            - code: `200_OK`
            - body:
            ```json
            [
                {
                    "id": 1,
                    "name": "pro1",
                    "description": "something1",
                    "discount": "10.00"
                },
                {
                    "id": 2,
                    "name": "pro2",
                    "description": "something2",
                    "discount": "0.00"
                }
            ]
            ```
6. ^catalog/promotion/(?P<pk>[0-9]+)$ [name='promotion-detail']
    - Get individual promotion by `promotion id`
    1. **Request**
        - method: `GET`
        - body: [none]
    2. **Response**
        1. Successfully
            - code: `200_OK`
            - body:
            ```json
            {
                "id": 1,
                "name": "pro1",
                "description": "something1",
                "discount": "10.00"
            }
            ```
