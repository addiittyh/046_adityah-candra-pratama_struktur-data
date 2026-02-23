def cek_anagram(str1, str2):
    if len(str1) != len(str2):
        return False

    hitung = {}

    for char in str1:
        hitung[char] = hitung.get(char, 0) + 1

    for char in str2:
        if char not in hitung:
            return False
        hitung[char] -= 1
        if hitung[char] < 0:
            return False

    return True


# Pengujian
print("Apakah anagram?", cek_anagram("listen", "silent"))
