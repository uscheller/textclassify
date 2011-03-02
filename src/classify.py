import os
j = os.path.join

def train(text):
	"""
	Train a dictionary with the given text. Returns a dictionary of dictionaries, 
	that describes the probabilities of all word-folling-ocurrences in the text.
	
	For example, the string "a test" gives this result:
	>>> train("a test")
	{'': {'a': 1}, 'a': {'test': 1}}
	Meaning that the empty string '' has been followed once by 'a' and 'a' has been 
	followed by 'test' as well.
	
	A longer example leads to a more complex dictionary:
	>>> train("this is a test oh what a test")
	{'': {'this': 1}, 'a': {'test': 2}, 'what': {'a': 1}, 'oh': {'what': 1}, 'this': {'is': 1}, 'is': {'a': 1}, 'test': {'oh': 1}}
	"""
	c = {}
	lastword = ""
	for word in text.split():
		word = word.lower()
		if c.has_key(lastword):
			inner = c[lastword]
			if inner.has_key(word):
				inner[word] += 1
			else:
				inner[word] = 1
		else:
			c[lastword] = {word: 1}
		lastword = word
	return c

def probability_of(dict, lastword, word):
	"""
	Helper function for calculating the probability of word following lastword
	in the category given by dict.
	
	>>> category = train("this is a test")
	>>> probability_of(category, "a", "test")
	1.0
	
	>>> probability_of(category, "any", "words")
	0
	"""
	word = word.lower()
	if dict.has_key(lastword):
		inner = dict[lastword]
		sumvalues = sum([v for v in inner.values()])
		if inner.has_key(word):
			return inner[word] / (sumvalues * 1.0)
	return 0

def classify(text, dict):
	"""
	Returns the probability that a text is from the given category. For every pair of
	words the probability_of value is calculated, summarized and divided by the amount
	of words in the text.
	
	>>> category = train("this is a test")
	>>> classify("a test with some words", category)
	0.2
	
	>>> classify("just writing test or a doesn't improve the ranking", category)
	0.0
	"""
	lastword = ""
	probabilities = 0
	for word in text.split():
		probabilities += probability_of(dict, lastword, word)
		lastword = word
	return probabilities / (len(text.split()) * 1.0)

if __name__ == "__main__":
	"""
	Calculate the category, that the text in ../test matches best.
	"""
	ranking = []
	os.chdir("..")
	for file in os.listdir("categories"):
		trained = train(open(j("categories", file)).read())
		value = classify(open("test").read(), trained)
		print "test is", file, "with", value, "% probability"
		ranking.append((value, file))
	
	ranking.sort()
	print
	print "The test text is probably from", ranking[-1][1]
	print "(second guess is", ranking[-2][1] + ")"


