from bs4 import BeautifulSoup
import requests
import itertools


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
	numbers, nums_holder = [], []
	for number in numbers_src:
		if len(nums_holder) < 5:
			nums_holder.append(number.text.split()[0])
		if len(nums_holder) == 5:
			numbers.append(nums_holder)
			nums_holder = []
	return numbers


def get_mega_multiplier(source):
	bonus_src = source.find_all("li", class_="mega-ball")
	bonus_holder = []
	for mm in bonus_src:
		bonus_holder.append(mm.text.split()[0])
	return bonus_holder


def numbers_of_the_year(year):
	link = "https://www.lottery.net/mega-millions/numbers/" + str(year)
	source = get_source(link)
	numbers_yr = get_numbers(source)
	multipliers_yr = get_mega_multiplier(source)
	return numbers_yr, multipliers_yr


def find_roster(end_year):
	freq, mm_freq = dict(), dict()
	for year in range(1996, end_year + 1):
		num_list = numbers_of_the_year(year)[0]
		mm_list = numbers_of_the_year(year)[1]
		for item in num_list:
			for n in item:
				if n in freq:
					freq[n] += 1
				else:
					freq[n] = 1
		for mm in mm_list:
			for nm in mm:
				if nm in mm_freq:
					mm_freq[nm] += 1
				else:
					mm_freq[nm] = 1
	sorted_tuples = sorted(freq.items(), key=lambda item: item[1], reverse=True)
	sorted_tuples_mm = sorted(mm_freq.items(), key=lambda item: item[1], reverse=True)
	result = {k: v for k, v in sorted_tuples}
	result_mm = {k: v for k, v in sorted_tuples_mm}
	return result, result_mm


def finalize_roster(end_year):
	ros, mm_ros = find_roster(end_year)[0], find_roster(end_year)[1]
	final, final_mm, counts, mm_counts = [], [], [], []
	for count in ros.values():
		counts.append(count)
	for mm_count in mm_ros.keys():
		mm_counts.append(mm_count)
	nums = sorted(set(counts), reverse=True)[:6]
	mm = sorted(set(mm_counts), reverse=True)[:1]
	for k, v in ros.items():
		if v in nums:
			final.append(k)
	return final, mm


def find_best(end_year):
	best, ros, best_finals = [], [], []
	roster = finalize_roster(end_year)[0]
	mm = finalize_roster(end_year)[1]
	if len(roster) == 5:
		best = roster
	else:
		for L in range(0, len(roster) + 1):
			for subset in itertools.combinations(roster, L):
				ros.append(subset)
	for comb in ros:
		if len(comb) == 5:
			best.append(comb)
	best_finals = list(itertools.product(best, mm))
	return best_finals


# link1 = "https://www.lottery.net/mega-millions/numbers/2021"
# link2 = "https://www.lottery.net/mega-millions/numbers/2020"
# link3 = "https://www.lottery.net/mega-millions/numbers/2019"
# link4 = "https://www.lottery.net/mega-millions/numbers/2018"
# print(get_mega_multiplier(get_source(link1)))
# print(get_mega_multiplier(get_source(link2)))
# print(get_mega_multiplier(get_source(link3)))
# print(get_mega_multiplier(get_source(link4)))

#print(find_roster(2021))
#print(finalize_roster(2021))
#print(find_best(2021))

from datetime import datetime

year = int(str(datetime.now())[:4])
best_combinations = find_best(year)
print("The best combination(s):")
if len(best_combinations[0]) == 1:
	print(best_combinations)
else:
	for item in best_combinations:
		n1, n2, n3, n4, n5, mega_multiplier = \
			item[0][0], item[0][1], item[0][2], item[0][3], item[0][4], item[1]
		print("Numbers: {}, {}, {}, {}, {} | Mega Ball: {}".format(n1, n2, n3, n4, n5, mega_multiplier))
print("Data based on the past winning numbers from 1996\n")
