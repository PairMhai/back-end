# Catalog APIs list and description

### Material List **(v0.12.0)**
- Path: ^catalog/materials$
- Description: List all materials
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
                "product_id": 1,
                "id": 1,
                "name": "name1",
                "quantity": 1,
                "description": "description of name1",
                "price": "00.00",
                "discounted_price": "00.000000",
                "color": "color",
                "image_name": "name1.jpg"
            },
            {
                "product_id": 2,
                "id": 2,
                "name": "name2",
                "quantity": 1,
                "description": "description of name2",
                "price": "00.00",
                "discounted_price": "00.000000",
                "color": "color",
                "image_name": "name2.jpg"
            }
        ]
        ```

### Material Detail **(v0.12.0)**
- Path: ^catalog/material/(?P<pk>[0-9]+)$
- Description: Get individual material by `material id`
1. **Request**
    - method: `GET`
    - body: [none]
2. **Response**
    1. Successfully
        - code: `200_OK`
        - body:
        ```json
        {
            "product_id": 6,
           "id": 1,
           "name": "name1",
           "quantity": 1,
           "description": "description of name1",
           "price": "00.00",
           "discounted_price": "00.00",
           "color": "red",
           "image_name": "red.jpg",
           "associate_promotions": [
               {
                   "name": "Test Promotion",
                   "image_name": "test_promotion.png",
                   "status": true,
                   "start": "2017-01-01T00:00:00+07:00",
                   "end": "2017-10-25T00:00:00+07:00"
               }
           ]
        }
        ```

### Design List **(v0.12.0)**
- Path: ^catalog/designs$
- Description: List all designs
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
                "product_id": 1,
                "id": 1,
                "name": "name1",
                "description": "description of name1",
                "price": 4000,
                "discounted_price": "1.00000000",
                "material": {
                    "product_id": 8,
                    "id": 3,
                    "name": "mat-name1",
                    "description": "description mat-name1",
                    "color": "red",
                    "image_name": "red.jpg"
                },
                "images": [
                    {
                        "id": 1,
                        "file_name": "name1.jpg"
                    }
                ],
                "associate_promotions": [
                    {
                        "name": "Test Promotion",
                        "image_name": "test_promotion.png",
                        "status": true,
                        "start": "2017-01-01T00:00:00+07:00",
                        "end": "2017-10-25T00:00:00+07:00"
                    }
                ]
            },
            {
                "product_id": 12,
                "id": 2,
                "name": "name2",
                "description": "description of name2",
                "price": 2000,
                "discounted_price": "2.00000000",
                "material": {
                    "product_id": 7,
                    "id": 1,
                    "name": "mat-name1",
                    "description": "description mat-name1",
                    "color": "blue",
                    "image_name": "blue.jpg"
                },
                "images": [
                    {
                        "id": 2,
                        "file_name": "name2.jpg"
                    }
                ],
                "associate_promotions": [
                    {
                        "name": "Test Promotion",
                        "image_name": "test_promotion.png",
                        "status": true,
                        "start": "2017-01-01T00:00:00+07:00",
                        "end": "2017-10-25T00:00:00+07:00"
                    }
                ]
            }
        ]
        ```

### Design Detail **(v0.12.0)**
- Path: ^catalog/design/(?P<pk>[0-9]+)$
- Description: Get individual design by `design id`
1. **Request**
    - method: `GET`
    - body: [none]
2. **Response**
    1. Successfully
        - code: `200_OK`
        - body:
        ```json
        {
            "product_id": 1,
            "id": 1,
            "name": "name1",
            "description": "description of name1",
            "price": 4000,
            "discounted_price": "1.00000000",
            "material": {
                "product_id": 8,
                "id": 3,
                "name": "mat-name1",
                "description": "description mat-name1",
                "color": "red",
                "image_name": "red.jpg"
            },
            "images": [
                {
                    "id": 1,
                    "file_name": "name1.jpg"
                }
            ],
            "associate_promotions": [
                {
                    "name": "Test Promotion",
                    "image_name": "test_promotion.png",
                    "status": true,
                    "start": "2017-01-01T00:00:00+07:00",
                    "end": "2017-10-25T00:00:00+07:00"
                }
            ]
        }
        ```

### Promotion list **(v1.0.1)**
- Path: ^catalog/promotions$
- Description: List all promotions
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
                "final_price": "1000.00",
                "products": [
                    {
                        "product": {
                            "id": 3,
                            "design": {
                                "product_id": 3,
                                "id": 3,
                                "name": "name-1",
                                "description": "description-1",
                                "material": {
                                    "product_id": 10,
                                    "id": 5,
                                    "name": "name-11",
                                    "description": "description-11",
                                    "color": "red",
                                    "image_name": "red.jpg"
                                },
                                "images": [
                                    {
                                        "id": 3,
                                        "file_name": "name-1.jpg"
                                    }
                                ]
                            }
                        },
                        "quantity": 1
                    }
                ],
                "updated_at": "2016-12-31T17:00:00Z"
            }
        ]
        ```
