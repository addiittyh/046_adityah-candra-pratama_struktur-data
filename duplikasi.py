def deduplikasi(data):
    sudah_ada = set()
    hasil = []

    for item in data:
        if item not in sudah_ada:
            hasil.append(item)
            sudah_ada.add(item)

    return hasil


# Pengujian
data = [1, 2, 3, 2, 4, 1, 5, 3]
print("Data asli:", data)
print("Setelah deduplikasi:", deduplikasi(data))
