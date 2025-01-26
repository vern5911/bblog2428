from datetime import datetime, timedelta, date

def date_from_doy(year, day_of_year):
    return datetime(year, 1, 1) + timedelta(days=day_of_year - 1)

def get_date(bid):
    if bid<=31:
        yr=2024
        doy=bid
    elif bid<=365+31:
        yr=2025
        doy=bid-(365+31)
    elif bid<=730+31:
        yr=2026
        doy=bid-(365-31)
    elif bid<=
        yr=2027
        doy=bid-(730-31)
    elif bid<date(2028,12,31).day:
        yr=2028
        doy=bid-1095-31
    else:
        print('Incorrect input value')
    return date_from_doy(yr,doy)



# Example usage
#year = 2023
#day_of_year = 38
#date = date_from_day_of_year(year, day_of_year)
date=get_date(32)



