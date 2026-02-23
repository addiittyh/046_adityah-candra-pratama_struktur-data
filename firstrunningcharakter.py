def first_recurring_char(teks):
    sudah_ada = set()

    for char in teks:
        if char in sudah_ada:
            return char
        sudah_ada.add(char)

    return None


# Pengujian
print("Karakter berulang pertama:", first_recurring_char("abca"))
