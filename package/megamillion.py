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


def find_roster(end_year):
	freq = dict()
	for year in range(1996, end_year+1):
		num_list = numbers_of_the_year(year)
		for item in num_list:
			for n in item:
				if n in freq:
					freq[n] += 1
				else:
					freq[n] = 1
	sorted_tuples = sorted(freq.items(), key=lambda item: item[1], reverse=True)
	result = {k: v for k, v in sorted_tuples}
	return result


def finalize_roster(end_year):
	ros = find_roster(end_year)
	final = []
	counts = []
	for count in ros.values():
		counts.append(count)
	nums = sorted(set(counts), reverse=True)[:6]
	for k,v in ros.items():
		if v in nums:
			final.append(k)
	return final


def find_best(end_year):
	best = []
	ros = []
	roster = finalize_roster(end_year)
	if len(roster) == 6:
		best = roster
	else:
		for L in range(0, len(roster)+1):
			for subset in itertools.combinations(roster, L):
				ros.append(subset)
	for comb in ros:
		if len(comb) == 6:
			best.append(comb)
	return best