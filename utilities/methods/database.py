def get_customer_from_user_id(uid):
    from membership.models import Customer

    return Customer.objects.get(user_id=uid)


def get_user_by_token(token):
    from rest_framework.authtoken.models import Token
    user_id = Token.objects.get(key=token).user_id
    return get_user_by_id(user_id)


def get_user_by_id(userid):
    from membership.models import User
    return User.objects.get(id=userid)


def get_customer_by_token(token):
    from membership.models import Customer
    return Customer.objects.get(user=get_user_by_token(token))


def get_customer_by_uid(userid):
    from membership.models import Customer
    return Customer.objects.get(user_id=userid)


def get_customer_by_cid(customerid):
    from membership.models import Customer
    return Customer.objects.get(id=customerid)


def update_all_status_promotions(list_of_promotion):
    from django.utils.timezone import now

    sets = list_of_promotion.filter(start_date__lt=now(), end_date__gt=now())
    for q in sets:
        q.change_status(True)
    return sets.filter(status=True)


def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    from django.shortcuts import get_object_or_404 as _get_object_or_404
    from django.core.exceptions import ValidationError
    from django.http import Http404

    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError, ValidationError):
        raise Http404
