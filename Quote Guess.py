import requests, os, random
from bs4 import BeautifulSoup
from csv import writer

######################################################################################################################

def show_topic(main_soup):
	for item in main_soup.select(".topicContentName"):
		print(item.get_text())

def check_answer(num):
	user_answer = input("\nAuthor of above Quote is: ")
	if user_answer.lower() != quote_author[num].get_text().lower():
		global count
		count = count - 1
		os.system('cls')
		return False
	else:
		print("\n\nYES!!!! That's Right Answer")
		return True

def show_quote(num, count):
	print(quote_text[num].get_text())
	print(f"\n\nYou have {count-1} Chances remaining")

######################################################################################################################

url = "https://www.brainyquote.com"
url_bio = "https://www.brainyquote.com/quotes/biography/"

response_topics = requests.get("https://www.brainyquote.com/topics")
main_soup = BeautifulSoup(response_topics.text, "html.parser")

topic_list = []
topic_url_list = []

for topic_url in main_soup.findAll("a", {"href" : lambda L: L and L.startswith('/topics/')}):
	topic_url_list.append(topic_url.attrs["href"])

for topic in main_soup.select(".topicContentName"):
	topic_list.append(topic.get_text().lower())


while(True):
	show_topic(main_soup)
	user_input_topic = input("Choose a Topic from the List: ")
	if user_input_topic not in topic_list:
		os.system('cls')
		continue
	os.system('cls')
	index = topic_list.index(user_input_topic)
	topic_link = url + topic_url_list[index]

	response_quotes = requests.get(topic_link)
	quote_soup = BeautifulSoup(response_quotes.text, "html.parser")
	quote_text = quote_soup.findAll("a", {"title": "view quote"})
	quote_author = quote_soup.findAll("a", {"title": "view author"})
	while(True):
		num = random.randint(0,len(quote_text)-1)

		flag=1
		author_bio_link = url_bio + quote_author[num].get_text().lower().replace(" ", "-") + "-biography"
		response_author_bio = requests.get(author_bio_link)
		if response_author_bio.status_code == 200:
			author_soup = BeautifulSoup(response_author_bio.text, "html.parser")
			author_nationality = author_soup.select(".bio-prof-and-nat")
			author_dob = author_soup.select(".bio-birth-death")
		else:
			flag=2
			author_bio_link = url + quote_text[num].attrs["href"]
			response_author_bio = requests.get(author_bio_link)
			author_soup = BeautifulSoup(response_author_bio.text, "html.parser")
			author_profession = author_soup.findAll("a", {"href" : lambda L: L and L.startswith('/profession/quotes')})
			author_nationality = author_soup.findAll("a", {"href" : lambda L: L and L.startswith('/nationality/quotes')})
			author_dob = author_soup.select(".bqLn")

######################################################################################################################

		count = 4
		while(count):
			if count==4:
				show_quote(num, count)
				if(check_answer(num)):
					break
			elif count == 3:
				show_quote(num, count)
				if flag==1:
					print(f"\nHint 2: Authors Nationality or Profession - {author_nationality[0].get_text()}")
				else:
					print(f"\nHint 2: Authors Nationality or Profession - {author_nationality[0].get_text()} {author_profession[0].get_text()}")
				if(check_answer(num)):
					break
			elif count == 2:
				show_quote(num, count)
				if flag==1:
					print(f"\nHint 2: Authors Birthdate - {author_dob[0].get_text()}")
				else:
					print(f"\nHint 2: Authors Birthdate - {author_dob[2].get_text()}")
				if(check_answer(num)):
					break
			else:
				show_quote(num, count)
				print(f"\nThe Authors Correct Name is {quote_author[num].get_text()}")
				break

######################################################################################################################

		play_again = input("\n\n\nPlay Again ??? [ press N to quit / C for quote on same Topic / Any Other key for Other Topic]: ")
		if play_again[0].lower() == "n":
			exit()
		elif play_again[0].lower() == "c":
			os.system('cls')
			continue
		os.system('cls')
		break