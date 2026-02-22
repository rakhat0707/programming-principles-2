def squares_up_to_n(n):
    for i in range(1, n + 1):
        yield i * i


# test
for x in squares_up_to_n(5):
    print(x)


def even_numbers(n):
    for i in range(0, n + 1):
        if i % 2 == 0:
            yield i


n = int(input())
print(",".join(str(x) for x in even_numbers(n)))

def divisible_by_3_and_4(n):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


for x in divisible_by_3_and_4(100):
    print(x)

def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


for value in squares(3, 7):
    print(value)

def countdown(n):
    while n >= 0:
        yield n
        n -= 1


for x in countdown(5):
    print(x)