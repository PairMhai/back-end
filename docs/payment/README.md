# Payment APIs list and description

### Payment Creator **(v0.2.2)**
- Path: ^payment/$
- Description: create new credit card
1. **Request**
    - method: `POST`
    - body:
    ```json
    {
        "owner": "Some User",
        "credit_no": "1234123412341234",
        "ccv": "123",
        "expire_date": "2022-01-01",
        "customer": "token"
    }
    ```
2. **Response**
    1. Successfully
        - code: `201_CREATED`
        - body:
        ```json
        {
            "id": 1,
            "owner": "Some User",
            "credit_no": "1234123412341234",
            "ccv": "123",
            "expire_date": "2022-01-01",
            "customer": "username: name surname"
        }
        ```

### Payment Destroyer **(v1.4.2)**
- Path: ^payment/delete/(?P<token>\w+)/(?P<ip>[0-9]+)$
- Description: delete payment
1. **Request**
    - method: `DELETE`
    - body: [none]
2. **Response**
    1. Successfully
        - code: `204_NO_CONTENT`
        - body: [none]
