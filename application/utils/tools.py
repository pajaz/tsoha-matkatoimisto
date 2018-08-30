import datetime

# Ottaa parametrinä timedate-olion, suomenkielisen viikonpäivän, sekä kokonaisluvun
# Palauttaa seuraavien (repeat - 1):n kyseisen viikonpäivän päivämäärät muodossa dd/mm/yyyy
def next_weekdays(d, weekday, repeat):
    day_number = get_weekday_number(weekday)
    days_ahead = day_number -  d.weekday()
    if days_ahead <= 0: # Kyseinen päivä on jo menny tällä viikolla
        days_ahead += 7
    departure = d + datetime.timedelta(days_ahead)
    dates = [departure.strftime("%d.%m.%Y")]
    count = repeat
    while count > 0:
        departure = departure + datetime.timedelta(days=7)
        dates.append(departure.strftime("%d.%m.%Y"))
        count = count - 1
    return dates

def get_weekday_number(d):
    weekdays = {"Maanantai":0, "Tiistai":1, "Keskiviikko":2, "Torstai":3,
                "Perjantai":4, "Lauantai":5, "Sunnuntai":6}
    dd = weekdays[d]
    return dd

# Ottaa luvun ja kohteen. Pyöristää luvun seuraavaan kohteen kertoimeen. (round_to_next(16, 5) -> 20)
def round_to_next(n, target):
    j =  n + (target - n) % 5
    return int(j)
