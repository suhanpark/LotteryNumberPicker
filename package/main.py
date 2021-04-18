from datetime import datetime

def run(mod):
	year = int(str(datetime.now())[:4])
	best_combinations = mod.find_best(year)
	print("The best combination(s):")
	if len(best_combinations[0]) == 1:
		print(best_combinations)
	else:
		for item in best_combinations:
			print(item)
	print("Data based on the past winning numbers from 1996\n")

if __name__ == '__main__':
	def ask():
		choice = input("Choose your lottery ticket type:\n"
			                     "1) Megamillion\n"
			                     "2) Power Ball\n"
			                "Please input the number indicates the type.\n"
			                "Type 'quit' to exit\n"
		                    ">")
		return choice

	while True:
		choice = ask()
		if choice == "1":
			import megamillion as mg
			run(mg)
		elif choice == "2":
			import powerball as pb
			run(pb)
		elif choice == "quit":
			print("Thank you for using the app.")
			break
		else:
			print("Invalid response")