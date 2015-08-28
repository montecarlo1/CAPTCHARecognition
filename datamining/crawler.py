__author__ = 'Kevin'
import urllib
import urllib2
from PIL import Image
import imageRecognition
# from pytesser import *
import os
import operator
from numpy import *


def crawlSource(counter, newimgid):
    url = 'http://210.42.121.132/servlet/GenImg'
    while True:
        filename = "images/GenImg%d.jpg" % counter
        urllib.urlretrieve(url, filename)
        newimgid = imageRecognition.img2binary(filename, newimgid)
        counter += 1


def img2vector(fname):
    f = open(fname)
    returnVec = zeros((1, 750))
    for i in range(30):
        lineStr = f.readline()
        if lineStr[-1] == '\n':
            lineStr = lineStr[:-1]
        rownum = len(lineStr)
        for j in range(rownum):
            returnVec[0, rownum * i + j] = int(lineStr[j])
    return returnVec


def handwritingClassTest():
    hwLabels = []
    trainingFileList = os.listdir('C:/Users/Kevin/PycharmProjects/datamining/trainingdigit/trainingset')
    m = len(trainingFileList)
    trainingMat = zeros((m, 750))
    for i in range(m):
        fnameStr = trainingFileList[i]
        classStr = fnameStr.split("_")[0]
        hwLabels.append(classStr)
        trainingMat[i, :] = img2vector('C:/Users/Kevin/PycharmProjects/datamining/trainingdigit/trainingset/%s' % fnameStr)
    testFileList = os.listdir('C:/Users/Kevin/PycharmProjects/datamining/trainingdigit/trainingset')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fnameStr = testFileList[i]
        classStr = fnameStr.split('_')[0]
        vTest = img2vector('C:/Users/Kevin/PycharmProjects/datamining/trainingdigit/trainingset/%s' % fnameStr)
        classifierResult = classify0(vTest, trainingMat, hwLabels, 3)
        print "classifier result: %s, the real answer:%s" % (classifierResult, classStr),
        if (classifierResult != classStr):
            errorCount += 1.0
            print "wrong"
        else:
            print "correct"
    print "error number: %d" % errorCount
    print "error rate: %f" % (errorCount / float(mTest))


# kNN algorithm
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]] #changed
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())  # get the number of lines in the file
    returnMat = zeros((numberOfLines, 3))  # prepare matrix to return
    classLabelVector = []  # prepare labels return
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()  # replace all '\0'(enter key)
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelVector.append(listFromLine[-1].encode('hex'))  # -1 represents for the last line of the list
        index += 1
    return returnMat, classLabelVector


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet / tile(ranges, (m, 1))  # element wise divide
    return normDataSet, ranges, minVals


def datingClassTest():
    hoRatio = 0.50  # hold out 10%
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')  # load data setfrom file
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 7)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print "the total error rate is: %f" % (errorCount / float(numTestVecs))

# code to crawl images
# os.chdir('D:\Python27 x86\Lib\site-packages')
# newim = Image.open('trainingdigit/letter_1.jpg')
# newtext = image_to_string(newim)
# print newtext

# code to rename the file
# counter = 421
# newimgid = 1890
# crawlSource(counter,newimgid)
# newfile = open('outputs/output_3.txt', 'r')
# signal = True
# txtid = 500
# while signal:
# line = newfile.readline()
#     if line == '':
#         signal = False
#         break
#     if line[-1] == "\n":
#         line = line[:-1]
#     print "%s0" % line
#     # os.chdir('C:/Users/Kevin/PycharmProjects/datamining/trainingdigit/')
#     oldfname = 'C:/Users/Kevin/PycharmProjects/datamining/trainingdigit/demo%d.txt' % txtid
#     newfname = 'C:/Users/Kevin/PycharmProjects/datamining/trainingdigit/%s_demo%d.txt' % (line, txtid)
#     os.rename(oldfname, newfname)
#     txtid += 1
handwritingClassTest()
