import sys
import os
import itertools
import pickle
#word_dict = {}
def main(argv):
	rootdir = sys.argv[1]
	modelfile = sys.argv[2]
	#rootdir = "textcat"
	data = {}
	value = []
	for subdirectory,directory,files in os.walk(rootdir):
		value = []
		for filename in files:
			f = open(subdirectory+"/"+filename,"rb")
			lines = f.read()
			#print type(lines)
			value.append(lines)
			lines = ""
			data[subdirectory[-3:]] = value

	word_dict = {}
	for key in data:
		for file_content in data[key]:
			#print len(file_content)
			#break
			splitwords = file_content.split()
			for word in splitwords:
				if word not in word_dict:
					if key == "pos":
						word_dict[word] = [1,0,1]
					else:
						word_dict[word] = [0,1,1]
				else:
					if key == "pos":
						l1 = word_dict[word]
						l1[0] = l1[0] + 1
						l1[2] = l1[0] + l1[1]
						word_dict[word] = l1
					else:
						l2 = word_dict[word]
						l2[1] = l2[1] + 1
						l2[2] = l2[0] + l2[1]
						word_dict[word] = l2

	print len(word_dict)
	eliminate_words(word_dict)
	print word_dict
	poscount = 0
	negcount = 0
	probability_scores = {}
	for key in word_dict.keys():
		val = word_dict[key]
		poscount = poscount + val[0]
		negcount = negcount + val[1]
	total = poscount + negcount 
	print "poscount : "+str(poscount) +" Negcount : " +str(negcount)+ " Total : "+str(poscount +negcount) 
	V = len(word_dict)
	for key in word_dict.keys():
		weights = word_dict[key]
		weights[0] = (weights[0] + 1)/float(poscount + V)
		weights[1] = (weights[1] + 1)/float(negcount + V)
		weights[2] = (weights[2] + 1)/float(total + V)
		probability_scores[key] = weights
	print probability_scores
	priorPos = poscount/float(total)
	priorNeg = negcount/float(total)

	obj = []
	obj.append(probability_scores)
	obj.append(priorNeg)
	obj.append(priorPos)
	#with open("output.txt",'wb') as f:
	with open(modelfile,'wb') as f:
		pickle.dump(obj,f)


def eliminate_words(word_dict):
	for key in word_dict.keys():
		l3 = word_dict[key]
		if l3[2] < 5:
			#word_dict.pop(key)
			del word_dict[key]
	print len(word_dict)
if __name__ == "__main__":
	main(sys.argv[0:])
