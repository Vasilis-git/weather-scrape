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
