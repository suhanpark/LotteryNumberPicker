from bs4 import BeautifulSoup
import requests
import itertools


def get_source(link): # HTML -> XML
	website = requests.get(link).text
	source = BeautifulSoup(website, "lxml")
	return source


def get_numbers(source): # scrape past winning numbers except megaball numbers
	numbers_src = source.find_all("li", class_="ball") # find all numbers
	numbers, nums_holder = [], []
	for number in numbers_src:
		if len(nums_holder) < 5:
			# makes lists of 5 numbers: the amount of numbers you can pick for standard MM
			nums_holder.append(number.text.split()[0])
		if len(nums_holder) == 5:
			# when the current list holds 5 items, copy to final list and empty it
			numbers.append(nums_holder)
			nums_holder = []
	return numbers


def get_mega_multiplier(source): # same principle as above, but this function is for megaball numbers
	bonus_src = source.find_all("li", class_="mega-ball")
	bonus_holder = []
	for mm in bonus_src:
		bonus_holder.append(mm.text.split()[0])
	return bonus_holder


def numbers_of_the_year(year):
	# the link with past winning number data of each year since the start
	link = "https://www.lottery.net/mega-millions/numbers/" + str(year)
	source = get_source(link) # HTML to XML
	numbers_yr = get_numbers(source) # scrape past winning numbers -> list
	multipliers_yr = get_mega_multiplier(source) # scrape past winning megaball numbers -> list
	return numbers_yr, multipliers_yr


def find_roster(end_year): # rank numbers and megaball numbers by frequency of wins
	freq, mm_freq = dict(), dict()
	for year in range(1996, end_year + 1): # since the beginning year of MM
		num_list = numbers_of_the_year(year)[0] # list of past winning numbers of the year
		mm_list = numbers_of_the_year(year)[1] # list of past winning megaball numbers of the year
		for item in num_list:
			for n in item:
				if n in freq: # if the number is in the dictionary, add i to the value
					freq[n] += 1
				else: # if the number is not in the dict, make new key of the number
					freq[n] = 1
		for mm in mm_list: # same way as above, but for megaball numbers
			for nm in mm:
				if nm in mm_freq:
					mm_freq[nm] += 1
				else:
					mm_freq[nm] = 1
	sorted_tuples = sorted(freq.items(), key=lambda item: item[1], reverse=True) # rank
	sorted_tuples_mm = sorted(mm_freq.items(), key=lambda item: item[1], reverse=True) # rank
	result = {k: v for k, v in sorted_tuples} # only keys
	result_mm = {k: v for k, v in sorted_tuples_mm} # only keys
	return result, result_mm


def finalize_roster(end_year):
	ros, mm_ros = find_roster(end_year)[0], find_roster(end_year)[1]
	final, final_mm, vals, mm_vals = [], [], [], []
	for val in ros.values():
		vals.append(val)
	for mm_val in mm_ros.keys():
		mm_vals.append(mm_val)
	nums = sorted(set(vals), reverse=True)[:6] # 5 most frequently showing past winning numbers
	mm = sorted(set(mm_vals), reverse=True)[:1] # most frequently showing megaball
	for k, v in ros.items():
		if v in nums:
			final.append(k)
	return final, mm


def find_best(end_year): # best combinations of the numbers with the megaball number
	best, ros, best_finals = [], [], []
	roster = finalize_roster(end_year)[0]
	mm = finalize_roster(end_year)[1]
	if len(roster) == 5:
		best = roster # no need to make combinations
	else:
		for L in range(0, len(roster) + 1):
			for subset in itertools.combinations(roster, L):
				# making combinations within the number list
				ros.append(subset)
	for comb in ros:
		if len(comb) == 5: # only takes combinations of 5 items
			best.append(comb)
	best_finals = list(itertools.product(best, mm)) # combinations with megaball number
	return best_finals