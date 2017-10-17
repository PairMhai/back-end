1. ^cart/transportation$ [name='transportation-list']
    - list all transportations in backend
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
2. ^cart/calculate$ [name='calculate'] **(v0.9.2)**
    - calculate price of ordering product
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
                ]
            }
            ```
        2. **Response**
            1. Successfully
                - code: `200_OK`
                - body:
                ```json
                {
                    "raw_price": 5000.0,
                    "customer_discount": 250.0,
                    "final_price": 4750.0
                }
                ```
            1. Failure
                - code: `400_BAD_REQUEST`
                - body:
                ```json
                {
                     "detail": "error message/object"
                }
                ```
3. ^cart/$ [name='order-creator']
    - create ordering in customer cart
        1. **Request**
            - method: `POST`
            - body:
            ```json
            {
                "customer": "customer token",
                "creditcard": 1,
                "transportation": 1,
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
                ]
            }
            ```
        2. **Response**
            1. Successfully
                - code: `201_CREATED`
                - body:
                ```json
                {
                    "id": 1,
                    "total_price": 0.00,
                    "total_product": 1,
                    "transportation": {
                        "name": "trans 1",
                        "description": "descp 1",
                        "price": 0.00
                    },
                    "created_at": "0001-02-03T04:05:06.123456Z"
                }
                ```
                - 0001 - year
                - 02 - month
                - 03 - day
                - 04 - hour
                - 05 - minute
                - 06 - second
                - 123456 - milisecond
4. ^cart/history/(?P<token>\w+)$ [name='history-detail']
    - get history of customer by `token`
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
                        "id": 2,
                        "customer": "name",
                        "products": [
                            {
                                "product": {
                                    "id": 3,
                                    "design": 3,
                                    "material": null
                                },
                                "quantity": 1
                            }
                        ]
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
