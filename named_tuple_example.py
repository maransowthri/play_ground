import collections

person = collections.namedtuple('person', ['first_name', 'last_name', 'age'])
maran = person('Maran', 'Sowthri', 18)
print(maran.first_name)