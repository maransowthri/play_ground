list_in = ['Madam', 'Malayalam', 'drawer', 'radar', 'Maran']

for word in list_in:
    if word.strip().lower() == word.strip().lower()[::-1]:
        print(word)
