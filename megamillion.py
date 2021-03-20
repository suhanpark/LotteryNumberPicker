from bs4 import BeautifulSoup
import requests


def get_source(link):
	website = requests.get(link).text
	source = BeautifulSoup(website, "lxml")
	return source


def get_dates(source):
	dates = []
	dates_src = source.find_all("a", title="View the prize payout information for this draw")
	for i in range(0, len(dates_src)):
		date = dates_src[i].text
		dates.append(date)
	return dates


def get_numbers(source):
	numbers_src = source.find_all("li", class_="ball")
	bonus_src = source.find_all("li", class_="mega-ball")
	numbers = []
	nums_holder = []
	count = 0
	bonus_count = 0
	for number in numbers_src:
		if count < 5:
			nums_holder.append(number.text.split()[0])
			count += 1
		else:
			nums_holder.append(bonus_src[bonus_count].text.split()[0])
			numbers.append(nums_holder)
			nums_holder = []
			count = 0
			bonus_count += 1
	return numbers


def numbers_of_the_year(year):
	link = "https://www.lottery.net/mega-millions/numbers/" + str(year)
	source = get_source(link)
	numbers_yr = get_numbers(source)
	return numbers_yr


# def find_best(year):
# 	num_list = numbers_of_the_year(year)
# 	freq = dict()
# 	best = []
# 	for item in num_list:
# 		for n in item:
# 			if n in freq:
# 				freq[n] += 1
# 			else:
# 				freq[n] = 1
# 	sorted_tuples = sorted(freq.items(), key=lambda item: item[1], reverse=True)
# 	result = {k: v for k, v in sorted_tuples}
# 	count = 0
# 	for key in result:
# 		if count == 5:
# 			break
# 		best.append(key)
# 		count += 1
# 	return best


def even_and_odd_count(yr1, yr2):
	comb = []
	for year in range(yr1, yr2 + 1):
		comb += numbers_of_the_year(year)
	dic = {"o3e2": 0, "e3o2": 0, "o1e4": 0, "e1o4": 0, "o5": 0, "e5": 0}
	for item in comb:
		even = 0
		for number in item:
			if int(number) % 2 == 0:
				even += 1
		if even == 5:
			dic["e5"] += 1
		elif even == 0:
			dic["o5"] += 1
		elif even == 1:
			dic["e1o4"] += 1
		elif even == 4:
			dic["o1e4"] += 1
		elif even == 3:
			dic["e3o2"] += 1
		elif even == 2:
			dic["o3e2"] += 1
	sorted_tuples = sorted(dic.items(), key=lambda item: item[1], reverse=True)
	result = {k: v for k, v in sorted_tuples}
	return result


def find_rep_set(L):
	reps = dict()
	combs = []
	for set in L:
		count = 0
		for item in L:
			if set == item:
				count += 1
		if count > 1:
			reps[count] = set
	max_rep = max(reps)
	for item in reps:
		if item == max_rep:
			combs += reps[item]
	return combs


def find_quadruples(L):
