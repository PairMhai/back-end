# Membership APIs list and description

1. ^membership/password/reset/$ [name='rest_password_reset'] **(vx.x.x)**
    - Reset password by email
    1. **Request**
        - method: `POST`
        - body:
        ```json
        {
            "email": "email@pairmhai.com"
        }
        ```
    2. **Response**
        1. Successfully
            - code: `200_OK`
            - body:
            ```json
            {
                "detail": "Password reset e-mail has been sent."
            }
            ```
2. ^membership/password/reset/confirm/$ [name='rest_password_reset_confirm'] **(vx.x.x)**
    - Confirm newest password
    1. **Request**
        - method: `POST`
        - body:
        ```json
        {
            "new_password1": "password1",
            "new_password2": "password1",
            "uid": "user id hash",
            "token": "token"
        }
        ```
    2. **Response**
        1. Successfully
            - code: `200_OK`
            - body: [none]
3. ^membership/login/$ [name='rest_login'] **(v0.2.2)**
    - Login
    1. **Request**
        - method: `POST`
        - body:
        ```json
        {
        	"username": "admin",
            "password": "password123"
        }
        ```
    2. **Response**
        1. Successfully
            - code: `200_OK`
            - body:
            ```json
            {
                "key": "django base-token"
            }
            ```
4. ^membership/logout/$ [name='rest_logout'] **(v0.2.2)**
    - Logout
    1. **Request**
        - method: `POST`
        - body: [none]
    2. **Response**
        1. Successfully
            - code: `200_OK`
            - body:
            ```json
            {
                "detail": "Successfully logged out."
            }
            ```
5. ^membership/password/change/$ [name='rest_password_change'] **(vx.x.x)**
    - Change password of currently user
    1. **Request**
        - method: `POST`
        - body:
        ```json
        {
            "new_password1": "newpass",
            "new_password2": "newpass",
            "old_password": "oldpass"
        }
        ```
    2. **Response**
        1. Successfully
            - code: `200_OK`
            - body:
            ```json
            {
                "detail": "New password has been saved."
            }
            ```
6. ^membership/register/$ [name='rest_register'] **(v1.0.2)**
    - Register new customer, **This api will sent email to imput email-address.**
    - and To confirm user email please click on the link that send together with email
    1. **Request**
        - method: `POST`
        - body:
        ```json
        {
            "user": {
                "username": "username",
                "first_name": "firstname",
                "last_name": "lastname",
                "email": "someone@pairmhai.com",
                "telephone": "085-XXX-XXXX",
                "address": "address",
                "date_of_birth": "yyyy-mm-dd",
                "gender": "male"
            },
            "password1": "password123",
            "password2": "password123",
            "classes": 3,
            "credit_cards": [
                {
                   "owner": "Some User-1",
                   "credit_no": "1234123412341234",
                   "ccv": "123",
                   "expire_date": "2022-01-01"
               },
               {
                  "owner": "Some User-2",
                  "credit_no": "1231231231231231",
                  "ccv": "321",
                  "expire_date": "2023-12-12"
              },
            ]
        }
        ```
        - optional field: **telephone**, **address**, **date_of_birth**, **gender**, **classes**, **credit_cards**
    2. **Response**
        1. Successfully
            - code: `200_OK`
            - body:
            ```json
            {
                "detail": "Verification e-mail sent."
            }
            ```
7. ^membership/cust/(?P<token>\w+)$ [name='membership-cust-detail'] **(v1.0.1)**
    - Get customer information by `customer token`
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
                "user": {
                    "id": 1,
                    "username": "name",
                    "first_name": "first",
                    "last_name": "last",
                    "email_address": "someone@pairmhai.com",
                    "address": "place",
                    "age": 99,
                    "date_of_birth": "yyyy-mm-dd",
                    "telephone": "08X-XXX-XXXX",
                    "gender": "unknown"
                },
                "classes": {
                    "id": 1,
                    "name": "Bronze",
                    "price": 0,
                    "description": "Discount 0% each time that purchase product."
                }
            }
            ```
8. ^membership/user/(?P<token>\w+)$ [name='membership-user-detail'] **(v1.0.1)**
    - Get user information by `user token`
    1. **Request**
        - method: `GET`
        - body: [none]
    2. **Response**
        1. Successfully
            - code: `200_OK`
            - body:
            ```json
            {
                "id": 2,
                "username": "test_user",
                "first_name": "Test",
                "last_name": "User",
                "email_address": "test@pairmhai.com",
                "age": 98,
                "gender": "female",
                "address": "test countr",
                "date_of_birth": "1919-09-18",
                "telephone": "087-654-3210"
            }
            ```
9. ^membership/class/(?P<pk>[0-9]+)$ [name='membership-class'] **(v0.2.2)**
    - Get class of customer by `class id`
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
                "name": "Bronze",
                "price": 0,
                "description": "Discount 0% each time that purchase product."
            }
            ```
