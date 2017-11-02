from datetime import datetime


def str_to_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def date_to_str(date):
    return date.strftime('%Y-%m-%d')


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
