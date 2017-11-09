from datetime import datetime


def str_to_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def date_to_str(date):
    return date.strftime('%Y-%m-%d')


def str_to_datedatetime(datetime_str):
    from django.utils.dateparse import parse_datetime
    return parse_datetime(datetime_str)


def is_between_date(start, end, current):
    from django.utils.dateparse import parse_date

    if isinstance(start, str):
        start = parse_date(start)
    else:
        start = start

    if isinstance(end, str):
        end = parse_date(end)
    else:
        end = end

    if isinstance(current, str):
        current = parse_date(current)
    else:
        current = current

    if start < current < end:
        return True
    return False


def change_default_timezone(date):
    from django.utils import timezone
    return timezone.localtime(date)

def round_money(x, base=25):
    """
    https://stackoverflow.com/questions/2272149/round-to-5-or-other-number-in-python
    """
    return int(base * round(float(x)/base))