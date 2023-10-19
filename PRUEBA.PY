def sequencecode():
    for number in range(1, 100000):
        yield f"F-01{number:06}"
        print(number)
sequencecode()