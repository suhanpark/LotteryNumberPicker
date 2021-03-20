from bs4 import BeautifulSoup
import requests
import time


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
	powerball_src = source.find_all("li", class_="powerball")
	numbers = []
	nums_holder = []
	count = 0
	pb_count = 0
	for number in numbers_src:
		if count < 5:
			nums_holder.append(number.text.split()[0])
			count += 1
		else:
			nums_holder.append(powerball_src[pb_count].text.split()[0])
			numbers.append(nums_holder)
			nums_holder = []
			count = 0
			pb_count += 1
	return numbers


def numbers_of_the_year(year):
	link = "https://www.lottery.net/powerball/numbers/" + str(year)
	source = get_source(link)
	numbers_yr = get_numbers(source)
	return numbers_yr


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
	for key in result:
		if count == 5:
			break
		best.append(key)
		count += 1
	return best

print(find_best(2021))