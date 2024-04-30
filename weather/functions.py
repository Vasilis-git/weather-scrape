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
    return switcher.get(b, 0)


# for usage with okairos.gr, day format: [day_n]/[month_abr]:
def convertDay(day):
    details = day.split()
    switcher = {
        "Απρ:": '4',
        "Απρ": '4',
        "Μάι:": '5',
        "Μάι": '5'
    }
    if len(details) == 2:
        offset = 0
    else:
        offset = 1
    return str(int(details[offset])) + '/' + switcher.get(details[offset+1], details[offset+1])
