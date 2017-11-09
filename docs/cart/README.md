# APIs for cart and transportation

### Transportation List **(v0.2.3)**
- Path: `^cart/transportation$`
- Description: list all transportations in backend
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
                "name": "trans 1",
                "description": "descp 1",
                "price": "0.00"
            },
            {
                "id": 2,
                "name": "trans 2",
                "description": "descp 2",
                "price": "0.00"
            }
        ]
        ```

### Calculate **(v1.2.0)**
- Path: `^cart/calculate$`
- Description: calculate price of ordering product
1. **Request**
    - method: `POST`
    - body:
    ```json
    {
        "customer": "customer token",
        "products": [
            {
                "pid": 1,
                "quantity": 1
            },
            {
                "pid": 2,
                "quantity": 1
            },
            {
                "pid": 1,
                "quantity": 1
            }
        ],
        "transportation": 1
    }
    ```
2. **Response**
    1. Successfully
        - code: `200_OK`
        - body:
        ```json
        {
            "calculate_id": "ea2747f2-8b6c-4c74-9abb-139b35210e7d",
            "full_price": 36000,
            "customer_discount": 5400,
            "event_discount": 34271,
            "transportation_price": 1234,
            "total_price": 0
        }
        ```
        - calculate_id -> uuid from sent when complete order
        - full_price -> price without any calculation
        - customer_discount -> discount by customer class (unit: baht)
        - event_discount -> discount by event class (unit: baht)
        - total_price -> final price but no include transport yet.
        - transportation_price -> price of input shipment
    2. Failure
        - code: `400_BAD_REQUEST`
        - body: 
        ```json 
            {
                "detail": [
                    {
                        "id": 15, 
                        "name": "Light Purple Dress", 
                        "message": "Doesn't have enough stock."
                    }
                ]
            }
        ```

### Order Creator **(v1.2.0)**
- Path: `^cart/$`
- Description: create ordering in customer cart
1. **Request**
    - method: `POST`
    - body:
    ```json
    {
        "uuid": "ea2747f2-8b6c-4c74-9abb-139b35210e7d",
        "creditcard": 1
    }
    ```
    - uuid -> get from calculate_id in calculation APIs
2. **Response**
    1. Successfully
        - code: `201_CREATED`
        - body:
        ```json
        {
            "final_price": 150,
            "total_product": 2,
            "transportation": {
                "name": "Thai Post Office",
                "description": "The leader of postal and logistics service in ASEAN.",
                "price": 150
            }
        }
        ```

### History Detail **(v1.1.4)**

- Path: `^cart/history/(?P<token>\w+)$`
- Description: get history of customer by `token`
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
                            "id": 1,
                            "design": {
                                "id": 2,
                                "name": "Dark Blue Dress",
                                "material": {
                                    "id": 2,
                                    "name": "Tasar",
                                    "color": "blue",
                                    "price": "1500.00",
                                    "image_name": "darkblue.jpg"
                                },
                                "price": 3000,
                                "images": [
                                    {
                                        "id": 4,
                                        "file_name": "darkblue-dress.jpg"
                                    }
                                ]
                            }
                        },
                        "quantity": 2
                    }
                ],
                "created_at": "2017-01-01T00:00:00+07:00",
                "updated_at": "2017-01-01T00:00:00+07:00"
            },
            {
                "id": 5,
                "final_price": "8000.00",
                "products": [
                    {
                        "product": {
                            "id": 2,
                            "material": {
                                "id": 2,
                                "name": "Tasar",
                                "color": "blue",
                                "price": "1500.00",
                                "image_name": "darkblue.jpg"
                            },
                        },
                        "quantity": 2
                    }
                ],
                "created_at": "2017-01-01T00:00:00+07:00",
                "updated_at": "2017-01-01T00:00:00+07:00"
            }
        ]
        ```
    2. Failure
        - code: `401_UNAUTHORIZED`
        - body:
        ```json
        {
            "detail": "get individual customer must have token"
        }
        ```