# Comment APIs list and description

1. ^comment/$ [name='comment'] **(v0.2.2)**
    1. request method: `POST`
        - create new comment
        - request body:
        ```json
        {
            "email": "email@pairmhai.com",
            "message": "message 1"
        }
        ```
        - response code: `201_CREATED`
        - response message:
        ```json
        {
            "id": 1,
            "email": "email@pairmhai.com",
            "message": "message 1"
        }
        ```
    2. request method: `GET`
        - list all comment in database
        - response code: `200_OK`
        - response message:
        ```json
        [
            {
                "id": 1,
                "email": "aaa@pairmhai.com",
                "message": "message 1"
            },
            {
                "id": 2,
                "email": "bbb@pairmhai.com",
                "message": "message 2"
            }
        ]
        ```
