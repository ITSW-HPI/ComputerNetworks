from collections import defaultdict

rt = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 'inf')))


rt['A']['B']['B'] = 3

print (rt[0][1])
print (rt[0][1][2])
print (rt['A'])
print (rt['A']['B'])
print (rt['A']['B']['B'])

print (rt.keys())
print (rt['A'].keys())
print (rt['B'].keys())

