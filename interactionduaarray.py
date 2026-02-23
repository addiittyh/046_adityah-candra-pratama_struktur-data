def intersection(list1, list2):
    set2 = set(list2)
    hasil = []

    for item in list1:
        if item in set2 and item not in hasil:
            hasil.append(item)

    return hasil


# Pengujian
a = [1, 2, 3, 4]
b = [3, 4, 5, 6]

print("Intersection:", intersection(a, b))
