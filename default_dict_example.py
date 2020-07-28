from collections import defaultdict


def have_nothing():
    return "Nothing"

sample_dedict = defaultdict(have_nothing)
print(sample_dedict['name'])

sample1_dedict = defaultdict(lambda: "Not Present")
print(sample_dedict['name'])

my_dedict = defaultdict(list)
my_dedict['hey'].append('Karan')
my_dedict['hey'].append('Maran')
print(my_dedict['hey'])