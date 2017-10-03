# Payment APIs list and description

1. ^payment/$ [name='payment-creator'] **(v0.2.2)**
    - create new credit card
    - request method: `POST`
    - request body:
        - **Note:** customer can be either `customer id` or `token`
    ```json
    {
        "owner": "Some User",
        "credit_no": "1234123412341234",
        "ccv": "123",
        "expire_date": "2022-01-01",
        "customer": 1
    }
    ```
    - response code: `201_CREATED`
    - response message:
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
