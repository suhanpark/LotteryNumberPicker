import itertools
list1=[['a','b','c'], ["e", "f", "g"], ["h", "i", "j"], ["k", "l", "m"]]
list2=[1,2]

f = list(itertools.product(list1, list2))
print(f)