from megamillion import numbers_of_the_year

def find_best(year):
	num_list = numbers_of_the_year(year)
	freq = dict()
	best = []
	for item in num_list:
		for n in item:
			if n in freq:
				freq[n] += 1
			else:
				freq[n] = 1
	sorted_tuples = sorted(freq.items(), key=lambda item: item[1], reverse=True)
	result = {k: v for k, v in sorted_tuples}
	count = 0
	# for key in result:
	# 	if count == 5:
	# 		break
	# 	best.append(key)
	# 	count += 1
	return result


print(find_best(2021))