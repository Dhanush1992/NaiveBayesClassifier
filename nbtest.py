import pickle
import sys
import os
import operator
import math



def main(argv):

	modelfile = sys.argv[1]
	testdir = sys.argv[2]
	predictionsfile = sys.argv[3]

	#with open("output.txt",'rb') as f:
	with open(modelfile,"rb") as f:
		global obj
	        obj = pickle.load(f)
	global probability_scores
	probability_scores = obj[0]
	global priorNeg
	priorNeg = obj[1]
	global priorPos
	priorPos = obj[2]
	#print probability_scores

	#rootdir = "pos"   # Give root directory containing files pos,neg and test
	logposscore = {}
	lognegscore = {}
	for key in probability_scores:
		y = probability_scores[key]
		math.log(y[0],2)
		math.log(y[1],2)
		logposscore[key] = math.log((math.log(y[0],2))/float(math.log(y[1],2)),2)
		lognegscore[key] = math.log((math.log(y[1],2))/float(math.log(y[0],2)),2)
	sorted_pos = sorted(logposscore.items(),key=operator.itemgetter(1))
	sorted_neg = sorted(lognegscore.items(),key=operator.itemgetter(1))

	#print sorted_pos
	pcount = 0
	ncount = 0
	with open("logratiopos","w") as lrp:
		lrp.write("\n log(pos/neg)\n")
		for posterm in sorted_pos:
			if(pcount < 20):
				lrp.write(str(posterm[0])+" : "+str(posterm[1])+"\n")
			pcount = pcount + 1

	with open("logrationeg","w") as lrn:
		lrn.write("\n log(neg/pos)\n")
		for negterm in sorted_neg:
			if(ncount < 20):
				lrn.write(str(negterm[0])+" : "+str(negterm[1])+"\n")
			ncount = ncount + 1
	



	rootdir = testdir
	#print rootdir
	global data
	data = {}
	for dirs,subdirs,files in os.walk(rootdir):
		for filename in files:
			try:
				f = open(dirs+"/"+filename,"r")
				lines = f.read()
				#print lines
				data[filename] = lines
				lines = ""
			except:
				pass
			
			#data[dirs[-3:]] = value
	#print data
	global logclassified
	global classified_set
	classified_set = {}
	logclassified = {}
	scorelist = {}
	poscount = 0
	negcount = 0
	#poslgcount = 0
	#neglgcount = 0
	count = 0
	for key in data.keys():
		review = data[key]
		terms = review.split()
		#print terms
		posscore = 0
		negscore = 0
		poslg = 0
		neglg = 0
		for term in terms:
			if term in probability_scores:
				val = probability_scores[term]
				#print val[0]
				#print val[1]
				posscore = posscore + float(math.log(val[0],10))
				negscore = negscore + float(math.log(val[1],10))
				#posscore = posscore * float(val[0])
				#negscore = negscore * float(val[1])
				#poslg = poslg + logposscore[term]
				#neglg = neglg + lognegscore[term]
		#finallgps = math.log(priorPos,2) + poslg
		#finallgng = math.log(priorNeg,2) + neglg
		finalpos = math.log(priorPos,10) + float(posscore)
		finalneg = math.log(priorNeg,10) + float(negscore)
		#finalpos = priorPos * float(posscore)
		#finalneg = priorNeg * float(negscore)
		#print "pos:"+str(finalpos)+"   neg: "+str(finalneg)
		count = count + 1
		z = []
		z.append(posscore)
		z.append(negscore)
		z.append(math.log((posscore/float(negscore)),2))
		z.append(math.log((negscore/float(posscore)),2))
		scorelist[key] = z
		#if posscore > negscore:
		if finalpos > finalneg:
			classified_set[key] = "pos"
			poscount = poscount + 1
		else:
			classified_set[key] = "neg"
			negcount = negcount + 1
		
	#print classified_set
	#print "poscount : "+str(poscount) +" negcount :" +str(negcount) +" Pos percentage :"+str((poscount/float(count))* 100)+" neg percentage :"+str((negcount/float(count))*100)
	a = "\n\nposcount : "+str(poscount) +" negcount :" +str(negcount) +" Pos percentage :"+str((poscount/float(count))* 100)+" neg percentage :"+str((negcount/float(count))*100)
	#c = "\n\nposlgcount : "+str(poslgcount) +" neglgcount :" +str(neglgcount) +" Poslg percentage :"+str((poslgcount/float(count))* 100)+" neglg percentage :"+str((neglgcount/float(count))*100)
	#with open(predictionsfile,"a") as x:
	print a
	#print c
	#	x.write(str(scorelist))
	#	x.write(str(classified_set))
	#	x.write(a)

	with open(predictionsfile,"w") as x:
		for key in scorelist:
			value = scorelist[key]
			classification = classified_set[key]
			b = "Filename : "+key+"  Classification :"+str(classification)+"  Positive score : "+str(value[0])+"  Negative Score : "+str(value[1])+"  log(Pos/Neg) : "+str(value[2])+" log(Neg/Pos) : "+str(value[3])+"\n"
			x.write(b)
		x.write(a)





if __name__ == "__main__":
	main(sys.argv[0:])