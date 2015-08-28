__author__ = 'Kevin'
import bayes

listOPost, listClasses = bayes.loadDataSet()
myVocabList = bayes.createVocabList(listOPost)
print myVocabList
print bayes.setOfWords2Vec(myVocabList, listOPost[0])
print bayes.setOfWords2Vec(myVocabList, listOPost[3])
s = "ab,cde,fg"
print s
print s.split(",")
from numpy import *

trainMat = []
for postinDoc in listOPost:
    trainMat.append(bayes.setOfWords2Vec(myVocabList, postinDoc))
p0V, p1V, pAb = bayes.trainNB0(trainMat, listClasses)
print "pAb: %s" % pAb
print "p0V: %s" % p0V
print "p1V: %s" % p1V


class TrainingLetter:
    result = "1"
    dataset = []
    measure = 0

    def __init__(self, letter, data, measure):
        self.result = letter
        self.dataset = data
        self.measure = measure


tl = TrainingLetter("2", [], 1)














