import os
j = os.path.join

def train(text):
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
	word = word.lower()
	if dict.has_key(lastword):
		inner = dict[lastword]
		sumvalues = sum([v for v in inner.values()])
		if inner.has_key(word):
			return inner[word] / (sumvalues * 1.0)
	return 0

def classify(text, dict):
	lastword = ""
	probabilities = 0
	for word in text.split():
		probabilities += probability_of(dict, lastword, word)
		lastword = word
	return probabilities / (len(text.split()) * 1.0)

if __name__ == "__main__":
	best = 0
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


