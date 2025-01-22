from convertdate import hebrew

def gregorian_to_hebrew(gregorian_date):
    year, month, day = hebrew.from_gregorian(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    return year, month, day
