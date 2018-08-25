import indicoio
indicoio.config.api_key = '746c34bde0657ea9712bd07e1fcdc8aa'

# single example
print(indicoio.sentiment("I love writing code!"))

# batch example
batch = ["I love writing code!",
    "Alexander and the Terrible, Horrible, No Good, Very Bad Day"
]


for i in batch:
	print (indicoio.sentiment(i))



