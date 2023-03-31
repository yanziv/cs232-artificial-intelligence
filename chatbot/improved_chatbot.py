import os
import sys
import openai
import re 
openai.api_key = "" # auth token removed for security
openai.Engine.list()


def query(text,max_tokens=5,temperature=0.1,top_p=1,engine="text-davinci-002"):
	completion = openai.Completion.create(engine=engine, prompt=text, max_tokens=max_tokens,temperature=temperature,top_p=top_p,n=1)
	return completion['choices'][0]['text']

# filler authentification token?
def main():
	q = sys.argv[1].strip()
	print(q)
	ans = query(q)
	print(ans)

#main()  #uncomment this and run program with a command-line string argument to see how query() works

# recursive helper functions 
def occasion(ans):
	if ans == "Y":
		specificOccasion = input("What occasion or holiday is this gift for? ")
		return(specificOccasion)
	if ans == "N":
		print("I see.")
	elif ans != "Y" and ans != "N":
		ans = input(invalid_msg)
		occasion(ans)

def haveBudget(ans):
	if ans == "Y":
		money = input("How much is your budget (USD)? ")
	if ans != "Y" and ans != "N":
		ans = input(invalid_msg)
		haveBudget(ans)

def generateGift(text, dislikedStuff):
	gift = query(text)
	if gift not in dislikedStuff:
		return gift 
	else:
		return generateGift(text)

def printSuggestions(giftDict):
	if specificOccasion != None:
		infoLine = "|| Gift Receiver: " + receiver + " Age: " + age + " Gender: " + gender + " Occasion: " + specificOccasion + " ||"
	if specificOccasion == None:
		infoLine = "|| Gift Receiver: " + receiver + " Age: " + age + " Gender: " + gender + " Occasion: N/A ||"
	divider = "=" * len(infoLine)
	print(divider)
	print(infoLine)
	print(divider)
	for i in giftDict:
		print("|| " + str(i+1) + ". " + str(giftDict[i]) + " " * (len(infoLine)-len(str(giftDict[i]))-8) + "||")
	print(divider)

### NEW HELPER METHOD ######
def happyResults(ans):
	if ans == "Y":
		print("Yay, I'm glad to hear that.")
		print("It's nice talking with you today. Thank you for choosing the service! See you next time!")
	if ans == "N":
		print("Oh no! I'm sorry to hear that.")
		giftNum = input("Maybe I could come up with another idea. Could you choose the gift you like the most out of the three options we have here? (Please specify the number) ")
		if giftNum not in "123":
			giftNum = input("Sorry, could you specify the gift number again? Type 1, 2, or 3. ")
		return giftNum 
	if ans != "Y" and ans != "N":
		ans = input(invalid_msg)
		return happyResults(ans)
# gift-giving prompt outline

# print this when the user inputs an invalid message 
invalid_msg = "Sorry, I don't understand. Could you please try answering the question again? "

print("Hello, I'm Vanessa. I am your gift selection service robot.")
name = input("Please enter your name: ")
print("Hello " + name + ", let's get started.")
receiver = input("Who are you selecting the gift for? ").strip()
age = input("May I ask the age of the gift receiver? If you are unsure, please put down an estimated number. ").strip()
gender = input("May I also ask the gender of the gift receiver? Please type \"Prefer not to say.\" if you do not wish to disclose this information. ").lower().strip()
isOccasion = input("Awesome, is this gift for a specific occassion or holiday? (Y/N) ").strip()
specificOccasion = None 
specificOccasion = occasion(isOccasion)
budget = input("Do you have a budget for this gift? (Y/N) ").strip()
money = ""
haveBudget(budget)
if specificOccasion != None:
	specificOccasion = specificOccasion.strip()
	print("Okay, just to recap, we are selecting a gift for " + receiver + " who is a " + gender + " person at the age of " + age + " for " + specificOccasion + ". ")
	if len(money) > 0:
		print("And your budget is " + money + " dollars.")
elif specificOccasion == None:
	print("Okay, just to recap, we are selecting a gift for " + receiver + " who is a " + gender + " person at the age of " + age + ".")
	if len(money) > 0:
		print("And your budget is " + money + " dollars.")

dislikedThings = input("Moving on, could you list a few things that this person doesn't like? ")
###############FIX THIS#######################
likedThings = input("Great, and are there things they really like in particular? ")
if " and " in likedThings:
	likedThings = likedThings.replace(" and ", ",") #replace "and" with commas 
#likedThings = re.sub("[^0-9\,]","",likedThings)
goalItems = [x.strip() for x in likedThings.split(',')] # convert all the things they like into a list 
goalItems = list(filter(None, goalItems)) # remove empty strings from list
#print("GOAL ITEMS:")
#print(goalItems)


######### generate text for query() #############
#### text 1 
textLst = []
text1 = "some good gifts"
if len(money) > 0:
	text1 += " that costs at around " + money 
text1 += " for a " + gender + " person "
if specificOccasion != None:
	text1 += "for " + specificOccasion
text1 += " are:"
for item in goalItems:
	text1 += " +" + item + "\n"
#print("TEXT1:"+text1)
textLst.append(text1)

#### text 2 
text2 = "some gifts for a " + gender + " person at the age of " + age + " are:"
for item in goalItems:
	text2 += " +" + item + "\n"
#print("TEXT2:"+text2)
textLst.append(text2)
#### text3
text3 = "some gifts for a person who doesn't like " + dislikedThings + " are:" 
for item in goalItems:
	text3 += " +" + item + "\n"
#print("TEXT3:"+text3)
textLst.append(text3)

print("Okay, based on the information about " + receiver + ", here are 3 gift suggestions: ")
giftDict = {}
for i in range(3):
	giftDict[i] = query(textLst[i]).strip()
	regex = re.compile('[^a-zA-Z]')
	regex.sub('', giftDict[i])
	giftDict[i] = giftDict[i].replace("+",'').replace("-",'').strip()

printSuggestions(giftDict)
################################################
############## IMPROVED PART ###################
################################################
print()
print("I hope this suggestions are helpful! :)")
isHappy = input("Are you happy with these three gift suggestions? (Y/N) ")
whichGift = happyResults(isHappy)
if whichGift != None: # if the user is unhappy with the previous suggestions and wants one more 
	textNum = whichGift.strip() 

	if textNum == "1":
		text1 = "some good gifts"
		if len(money) > 0:
			text1 += " that costs at around " + money 
		text1 += " for a " + gender + " person at the age of " + age # age is newly added 
		if specificOccasion != None:
			text1 += " for " + specificOccasion
		text1 += " are:"
		for item in goalItems:
			text1 += " +" + item + "\n"
		improvedText = text1 
	
	elif textNum == "2":
		text2 = "some awesome gifts for a person at the age of " + age + " who doesn't like " + dislikedThings + " are:" # disliked things are newly added 
		for item in goalItems:
			text2 += " +" + item + "\n"
		improvedText = text2

	elif textNum == "3":
		text3 = "some great gifts for a " + gender + " person who doesn't like " + dislikedThings + " are:" # gender is newly added
		for item in goalItems:
			text3 += " +" + item + "\n"
		improvedText = text3

	additionalOption = query(improvedText).replace("+",'').replace("-",'').strip()
	regex = re.compile('[^a-zA-Z]')
	regex.sub('', additionalOption)
	
	print("Okay, here's another option: " + additionalOption)
	print("Thank you for using the service! I hope the suggestions are helpful!")
	print("Have a good rest of your day! :)")
	print()


  