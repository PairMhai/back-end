# Index of document
This API using [REST architectural style](REST-description.md) and API framework, I choose [Django REST framework](http://www.django-rest-framework.org).

# Testing guideline
[guide](TEST_GUIDE.md)

# Membership (WIP)
1. ^membership/password/reset/$ [name='rest_password_reset']
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
2. ^membership/password/reset/confirm/$ [name='rest_password_reset_confirm']
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
3. ^membership/login/$ [name='rest_login']
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
4. ^membership/logout/$ [name='rest_logout']
    - logout
    - request method: `POST`
    - request body: none
    - response message:
    ```json
    {
        "detail": "Successfully logged out."
    }
    ```
6. ^membership/password/change/$ [name='rest_password_change']
7. ^membership/register/
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
8. ^membership/cust/(?P<pk>[0-9]+)$ [name='membership-cust-detail']
    - get customer information by `customer id`
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
        "classes": 1
    }
    ```
9. ^membership/user/(?P<pk>[0-9]+)$ [name='membership-user-detail']
    - get user information by `user id`
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
10. ^membership/class/(?P<pk>[0-9]+)$ [name='membership-class'] (Need to change)
    - get class of customer by `class id`
    - request method: `GET`
    - response message:
    ```json
    {
        "id": 1,
        "name": "Bronze",
        "price": 0,
        "description": "Discount 2% each time that purchase product."
    }
    ```

# Alert Error
1. I didn't implement account and admin user so `api-auth/` will not found before login.
2. I not sure that I upload the database with superuser or not
  - if yes:
    - username will be `admin` and password is `password123`
  - if no:
    - run `python|python3 manage.py createsuperuser`
