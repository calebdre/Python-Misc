import sys

fileName = sys.argv[1]

file = open(fileName)
lines = file.readlines()
totalWords = {}
for line in lines:
	for words in line.split(' '):
		if words in totalWords:
			totalWords[words] += 1
		else:
			totalWords[words] = 1

for key, value in totalWords.items():
	print(key,value)
print('Total # of Words:', len(totalWords))
print('done!')