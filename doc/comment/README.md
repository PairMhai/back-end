# Comment APIs list and description

1. ^comment/$ [name='comment'] **(v0.2.2)**
    - Create new comment
    1. **Request**
        - method: `POST`
        - body:
        ```json
        {
            "email": "email@pairmhai.com",
            "message": "message 1"
        }
        ```
    2. **Response**
        1. Successfully
            - code: `201_CREATED`
            - body:
            ```json
            {
                "id": 1,
                "email": "email@pairmhai.com",
                "message": "message 1"
            }
            ```
2. ^comment/$ [name='comment'] **(v0.2.2)**
    - List all comment in database
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
