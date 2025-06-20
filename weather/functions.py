CONNECTION = "postgres://sensors:DKM-sensors37@localhost:5432/sensors"


def bofortToKm(b):
    switcher = {
        0: 1,
        1: 3.5,
        2: 8,
        3: 16,
        4: 25,
        5: 33,
        6: 45,
        7: 56,
        8: 69,
        9: 80,
        10: 96,
        11: 110,
        12: 124
    }
    return switcher.get(b)


def convertWindDir(wind_dir):
    switcher = {
        'N': 'B',
        'S': 'N',
        'E': 'A',
        'W': 'Δ',
        'NE': 'BA',
        'NW': 'ΒΔ',
        'SE': 'ΝΑ',
        'SW': 'ΝΔ'
    }
    return switcher.get(wind_dir)


# for usage with okairos.gr, day format: [day_n]/[month_abr]:
def convertDay(day):  # expected input: [text] [day_n] [month_abr], [text] is optional
    details = day.split()
    switcher = {
        "Απρ:": '4',
        "Απρ": '4',
        "Μάι:": '5',
        "Μάι": '5',
        "ΜΑΪΟΥ": '5',
        "Ιούν:": '6',
        "Ιούλ:": '7',
        "Αύγ:": '8',
        "Σεπ:": '9',
        "Οκτ:": '10',
        "Νοέ:": '11',
        "Δεκ:": '12',
        "Ιαν:": '1',
        "Φεβ:": '2',
        "Μάρ:": '3',
        'ΙΑΝΟΥΑΡΙΟΥ': '1',
        'ΦΕΒΡΟΥΑΡΙΟΥ': '2',
        'ΜΑΡΤΙΟΥ': '3',
        'ΑΠΡΙΛΙΟΥ': '4',
        'ΜΑΙΟΥ': '5',
        'ΙΟΥΝΙΟΥ': '6',
        'ΙΟΥΛΙΟΥ': '7',
        'ΑΥΓΟΥΣΤΟΥ': '8',
        'ΣΕΠΤΕΜΒΡΙΟΥ': '9',
        'ΟΚΤΩΒΡΙΟΥ': '10',
        'ΝΟΕΜΒΡΙΟΥ': '11',
        'ΔΕΚΕΜΒΡΙΟΥ': '12'
    }
    if len(details) == 2:
        offset = 0
    else:
        offset = 1
    return details[offset] + '/' + switcher.get(details[offset + 1])
