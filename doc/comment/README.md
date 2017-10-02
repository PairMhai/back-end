# Comment APIs list and description

1. ^comment/$ [name='comment-creator']
    - create new comment
    - request method: `POST`
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

2. ^comment/all/$ [name='comment-list']
    - list all comment in database
    - request method: `GET`
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
