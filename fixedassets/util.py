def asset_incrementor(initial_count):
    count = initial_count
    def number():
        nonlocal count
        count += 1
        return count
    return number