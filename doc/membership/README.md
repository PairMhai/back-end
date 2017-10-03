# Membership APIs list and description

1. ^membership/password/reset/$ [name='rest_password_reset'] **(v0.2.2)**
    - reset password by email
    - request method: `POST`
    - request body:
    ```json
        {
            "email": "email@pairmhai.com"
        }
    ```
    - response message:
    ```json
    {
        "detail": "Password reset e-mail has been sent."
    }
    ```
2. ^membership/password/reset/confirm/$ [name='rest_password_reset_confirm'] **(v0.2.2)**
    - reset password by email
    - request method: `POST`
    - request body:
    ```json
    {
        "new_password1": "",
        "new_password2": "",
        "uid": "",
        "token": ""
    }
    ```
    - response message:
    ```json
    ```
3. ^membership/login/$ [name='rest_login'] **(v0.2.2)**
    - login
    - request method: `POST`
    - request body:
    ```json
    {
    	"username": "admin",
        "password": "password123"
    }
    ```
    - response message:
    ```json
    {
        "key": "django base-token"
    }
    ```
4. ^membership/logout/$ [name='rest_logout'] **(v0.2.2)**
    - logout
    - request method: `POST`
    - request body: none
    - response message:
    ```json
    {
        "detail": "Successfully logged out."
    }
    ```
5. ^membership/password/change/$ [name='rest_password_change'] **(vx.x.x)**
6. ^membership/register/$ [name='rest_register'] **(v0.2.2)**
    - register new customer
    - request method: `POST`
    - request body:
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
        "classes": 3
    }
    ```
    - response message:
    ```json
    {
        "key": "django base-token"
    }
    ```
7. ^membership/cust/(?P<token>\w+)$ [name='membership-cust-detail'] **(v0.2.2)**
    - get customer information by `customer token`
    - request method: `GET`
    - response message:
    ```json
    {
        "id": 1,
        "user": {
            "id": 1,
            "username": "name",
            "first_name": "first",
            "last_name": "last",
            "email": "someone@pairmhai.com",
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
8. ^membership/user/(?P<token>\w+)$ [name='membership-user-detail'] **(v0.2.2)**
    - get user information by `user token`
    - request method: `GET`
    - response message:
    ```json
    {
        "id": 1,
        "username": "name",
        "first_name": "first",
        "last_name": "last",
        "email": "someone@pairmhai.com",
        "address": "place",
        "age": 99,
        "date_of_birth": "yyyy-mm-dd",
        "telephone": "08X-XXX-XXXX",
        "gender": "unknown"
    }
    ```
9. ^membership/class/(?P<pk>[0-9]+)$ [name='membership-class'] **(v0.2.2)**
    - get class of customer by `class id`
    - request method: `GET`
    - response message:
    ```json
    {
        "id": 1,
        "name": "Bronze",
        "price": 0,
        "description": "Discount 0% each time that purchase product."
    }
    ```
