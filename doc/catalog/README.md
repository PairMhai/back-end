# Catalog APIs list and description

### Material List **(v0.2.3)**
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
                "color": "color",
                "image_name": "name2.jpg"
            }
        ]
        ```

### Material Detail **(v0.2.3)**
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
            "product_id": 1,
            "id": 1,
            "name": "name1",
            "quantity": 1,
            "description": "description of name1",
            "price": "00.00",
            "color": "color",
            "image_name": "name1.jpg"
        }
        ```

### Design List **(v0.2.3)**
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
                "product_id": 7,
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
                "product_id": 10,
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

### Design Detail **(v0.2.3)**
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
            "product_id": 7,
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
        
### Promotion list **(v0.11.0)**
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
                "product": 1,
                "name": "pro1",
                "description": "something1",
                "discount": "10.00",
                "image_name": "something1.png"
            },
            {
                "product": 3,
                "name": "pro2",
                "description": "something2",
                "discount": "0.00",
                "image_name": "something2.png"
            }
        ]
        ```

### Promotion Detail **(Deprecate @ v0.11.0)**
- Path: ^catalog/promotion/(?P<pk>[0-9]+)$
- Description: Get individual promotion by `promotion id`
1. **Request**
    - method: `GET`
    - body: [none]
2. **Response**
    1. Successfully
        - code: `200_OK`
        - body:
        ```json
        {
            "product": 1,
            "name": "pro1",
            "description": "something1",
            "discount": "10.00",
            "image_name": "something1.png"
        }
        ```
