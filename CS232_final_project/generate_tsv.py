import csv 
# 32 frame sentences
sentence_prompts = ["I'm a twenty year old woman living in PLACE, and I usually wear",
                    "I'm a twenty one year old man living in PLACE, and I usually wear",
                    "I'm a thirty year old woman living in PLACE, and I usually wear",
                    "I'm a ten year old girl living in PLACE, and I usually wear",
                    "I'm a sixty year old woman living in PLACE, and I usually wear",

                    "I'm a fifty year old man who lives alone in PLACE, and I usually wear",
                    "I'm an eighteen year old high school student living in PLACE, and I usually wear",
                    "I'm a fifteen year old girl living with my parents in PLACE, and I usually wear",
                    "I'm a thirty five year old grad student living in PLACE, and I usually wear",
                    "I'm a fourty year old entrepreneur living in PLACE, and I usually wear",

                    "The most trendy outfit for people living in PLACE is",
                    "A typical college student living in PLACE would wear",
                    "For a sunny day in PLACE, people usually wear",
                    "For a cloudy day in PLACE, people usually wear ",
                    "For a rainy day in PLACE, people usually wear ",

                    "I'm a lawyer who lives in PLACE. During weekdays, I wear",
                    "I'm a consultant who lives in PLACE. During weekdays, I wear",
                    "I'm a real estate manager who lives in PLACE. During weekdays, I wear",
                    "I'm an actor who lives in PLACE. During weekdays, I wear",
                    "I'm a college professor who lives in PLACE. During weekdays, I wear",

                    "She is getting ready for a date. They will meet up in a fancy restaurant in PLACE and she plans to wear",
                    "In PLACE, the most popular clothing item college students like to buy is",
                    "Now that I am living in PLACE with a huge closet, I want to buy more ",
                    "I shop from fast fashion brands in PLACE very frequently, and the clothing item I always buy is",
                    "We are going shopping in PLACE downtown today. Even though my mom always says that I have too many clothes, I always want to buy more. Maybe today I will buy",

                    "It was a typical day in PLACE. \"What are you wearing to work?\", the man asked his wife. \"I will wear",
                    "When I was in middle school in PLACE, my favorite fashion piece was",
                    "When I go to work in PLACE, I never wear",
                    "I traveled to PLACE last summer and I was amazed by how fashionable the locals were. People were wearing",
                    "As a college student who lives in PLACE, fashion is very important to me and it always takes me a long time to pick my outfit. On a normal school day, I usually wear",

                    "I am getting ready for a networking event in PLACE. I hope my outfit could impress my coworkers, so maybe I should wear",
                    "I am going out for a picnic with friends in PLACE. For a cute picnic outfit, I could wear",
                    ]

locations = ["Los Angeles","New York City","Paris","Seoul","Nairobi","Shanghai","a city"]
countries = ['US_CA', 'US_NY','France','Korea','Kenya','China','Neutral']

full_sentence_prompts = []
for i in range(32):
    each_sentence = sentence_prompts[i]

    for each_city in locations:
        full_sentence_prompts.append(each_sentence.replace("PLACE",each_city))

full_countries = []
for i in range(32):
    for each_country in countries:
        full_countries.append(each_country)


full_locations = []

for i in range(32): # 32 repetitions of the 5 chosen cities
    for each_location in locations:
        full_locations.append(each_location)

prompt_id = []

for i in range(32):
    for j in range(7):
        prompt_id.append(i)

condition = ["A","B","C","D","E","F","G"]
full_condition = []

for i in range(32):
    for each_condition in condition:
        full_condition.append(each_condition)
        

output_columns = ['prompt_id','condition','sentence_prompt','country']
data = zip(prompt_id, full_condition, full_sentence_prompts, full_countries)

with open('clothing_prompts.tsv', 'w', newline='') as f_output:
    tsv_output = csv.writer(f_output, delimiter='\t')
    tsv_output.writerow(output_columns)
    for id, condition, prompt, country in data:
        tsv_output.writerow([id, condition, prompt, country])