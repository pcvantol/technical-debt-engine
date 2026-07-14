def warning(a, b, c, d):
    if a:
        return 1
    if b:
        return 2
    if c:
        return 3
    if d:
        return 4
    return 0


def blocking(items):
    total = 0
    for item in items:
        if item > 0:
            if item % 2:
                total += 1
            else:
                total += 2
        elif item < -1:
            total -= 1
        elif item == -1:
            total -= 2
        else:
            total += 0
    return total
