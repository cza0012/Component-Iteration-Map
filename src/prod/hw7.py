"""
   Created for HW7
   Baselined: 18 April 2011  
   Modified:  27 April 2011
   @author:   Chulakorn Aritajati
"""

from math import log, pow, ceil, exp, sqrt
import re
import string

class Buckets():
    
    def __init__(self):
        #The average of the natural log of a set of values
        self.avg = None
        #The Standard deviation of the natural log of a set of values
        self.std = None
        #The very small category of a set of values
        self.vs = None
        #The small category of a set of values
        self.s = None
        #The medium category of a set of values
        self.m = None
        #The large category of a set of values
        self.l = None
        #The very large category of a set of values
        self.vl = None
        
    def buildLogNormal(self, itemList):
        #An attribute should be a list.
        if isinstance(itemList, list):
            #List should has length more than 2.
            if len(itemList) >= 2:
                #Summation of natural logarithm
                sumLn = 0.0
                #Summation of number - self.avg**number - self.avg
                sumPow = 0.0
                calitemList = itemList[:]
                #numnerOfComponent = len(itemList)
                listLn = []
                #Extract a list
                for x in itemList:
                    try:
                        numberLn = self.lnComponent(x)
                        listLn.append(numberLn)
                        sumLn += numberLn
                    except:
                        calitemList.remove(x)
                numnerOfComponent = len(calitemList)
                self.avg = float(sumLn / numnerOfComponent)
                if len(listLn) >= 2:
                    for x in listLn:
                        #To make sure that it is float. 
                        number = float(x)
                        sumPow += pow(number - self.avg, 2)
                    self.std = sqrt(sumPow / (numnerOfComponent - 1))
                    #vs = e^(avg-2std)
                    self.vs = int(ceil(exp(self.avg - (2 * self.std))))
                    #s = e^(avg-std)
                    self.s = int(ceil(exp(self.avg - self.std)))
                    #m = e^avg
                    self.m = int(ceil(exp(self.avg)))
                    #l = e^(avg+std)
                    self.l = int(ceil(exp(self.avg + self.std)))
                    #vl = e^(avg+2std)
                    self.vl = int(ceil(exp(self.avg + (2 * self.std))))
                    #upperVS is a upper bound of very small value.
                    upperVS = int(ceil(exp(self.avg - (1.5 * self.std))))
                    #upperS is a upper bound of small value.
                    upperS = int(ceil(exp(self.avg - (0.5 * self.std))))
                    #upperM is a upper bound of medium value.
                    upperM = int(ceil(exp(self.avg + (0.5 * self.std))))
                    #upperL is a upper bound of large value.
                    upperL = int(ceil(exp(self.avg + (1.5 * self.std))))
                    
                    #To set relative size value to each component
                    for x in calitemList:
                        locMethod = float(x.getLocCount() / x.getMethodCount())
                        if locMethod <= upperVS:
                            x.setRelativeSize("VS")
                        elif upperVS < locMethod and locMethod <= upperS:
                            x.setRelativeSize("S")
                        elif upperS < locMethod and locMethod <= upperM:
                            x.setRelativeSize("M")
                        elif upperM < locMethod and locMethod <= upperL:
                            x.setRelativeSize("L")
                        elif upperL > locMethod:
                            x.setRelativeSize("VS")
                else:
                    raise ValueError('Invalid size')
            else:
                raise ValueError('Invalid size')
        else:
            raise ValueError('Invalid List')
        #Always return None
        return None       
    
    #Calculate a natural log of a component
    def lnComponent(self, component):
        #Check an instance of a Component
        if isinstance(component, Component):
            if float(component.getMethodCount()) > 0:
                locMethod = float(component.getLocCount()) / float(component.getMethodCount())
                #its loc/Method is more than 0.
                if  locMethod > 0:
                    numberLn = log(locMethod)
                else:
                    #A length of a list is more than 2. 
                    raise ValueError('Non-positive integer')
            else:
                #A length of a list is more than 2. 
                raise ValueError('Non-positive integer')
        else:
            #Check an instance of a Component
            raise ValueError('Invalid Component')   
        
        return numberLn  

class Component(): 
    
    def __init__(self, name, methodCount, locCount, description=None):
        #Check parameters
        if len(name) > 0 and int(methodCount) >= 0 and int(locCount) >= 0:  
            self.relativeSize = None
            self.name = name
            self.methodCount = methodCount
            self.locCount = locCount
            self.description = description
        else:
            raise ValueError('Invalid parm')
        
    #Return name
    def getName(self):
        return self.name
    
    #Return description
    def getDescription(self):
        return self.description
    
    #Return methodCount
    def getMethodCount(self):
        return self.methodCount
    
    #Return locCount
    def getLocCount(self):
        return self.locCount
    
    #Return relativeSize 
    def getRelativeSize(self):
        return self.relativeSize
    
    #Set relativeSize 
    def setRelativeSize(self, newRelativeSize):
        if self.isRelativeSize(newRelativeSize):
            self.relativeSize = newRelativeSize
            
    #Check value setting relativeSize 
    def isRelativeSize(self, relativeSize):
        if relativeSize == "VS" or relativeSize == "S" or relativeSize == "M" or relativeSize == "L" or relativeSize == "VL":
            return True;
        else:
            raise ValueError('Invalid relative size')

class Script():
    #The average of the natural log of a set of values
    fileName = None
    #aFile is a file object.
    aFile = None
    
    #Initial a Script object    
    def __init__(self, fileName):
        #Initialize a file name
        self.fileName = fileName
        #Open a python file
        if self.isPy(fileName):
            try:
                self.aFile = open(fileName, 'r')
            except:
                raise IOError('File not Found')     
        else:
            raise IOError('Invalid file name')
        
    #Get a file name     
    def getFileName(self):
        return self.fileName
    
    #Extract components from a file
    def extractComponents(self):
        classTrigger = False
        methodNumber = 0
        methodTrigger = False
        className = ""
        lineNumber = 0
        componentList = []
        docsStrTrigger = ""
        docsStrClass = ""
        methodName = ""
        docStrCount = 0
        #Read line in a file 
        for line in self.aFile:
            #aList = re.split('\s+', line)
            aLine = line.strip()
            aList = aLine.split()
            #Find a class and '#' not in line
            docsStr = self.findOpenDocString(line)
            if docsStr != "" and not self.isComment(line):
                if docsStrTrigger == docsStr:
                    #Found doc string and need to be verified a line doc string 
                    docsStrTrigger = "Found"
                elif docsStrTrigger == "":
                    #Trigger record doc string
                    docsStrTrigger = docsStr
                    if classTrigger == True or methodTrigger == True:
                        docStrCount += 1
            if docsStrTrigger == "":
                if self.isClass(line):
                    #Class is found
                    if classTrigger == False:
                        classTrigger = True 
                        if methodTrigger == True:
                            if docsStrClass == "":
                                docsStrClass = None
                            #New class is found and a previous class put to a result list
                            self.componentListAppend(componentList, methodName, int(methodNumber), int(lineNumber), docsStrClass)
                            methodNumber = 0
                            lineNumber = 0
                            docsStrClass = ""
                            docStrCount = 0
                            methodTrigger = False
                    else:
                        if docsStrClass == "":
                            docsStrClass = None
                        #New class is found and a previous class put to a result list
                        self.componentListAppend(componentList, className, int(methodNumber), int(lineNumber), docsStrClass)
                        methodNumber = 0
                        lineNumber = 0
                        docsStrClass = ""
                        docStrCount = 0
                    #Find a class name
                    className = self.extractClassName(aList)
                elif self.isIndependentMethod(line):
                    #Method is found
                    if methodTrigger == False:
                        #Method is found
                        methodTrigger = True
                        if classTrigger == True:
                            #No doc string put none
                            if docsStrClass == "":
                                docsStrClass = None
                            #New class is found and a previous class put to a result list
                            self.componentListAppend(componentList, className, int(methodNumber), int(lineNumber), docsStrClass)
                            methodNumber = 0
                            lineNumber = 0
                            docsStrClass = ""
                            docStrCount = 0
                            #End a class scope
                            classTrigger = False
                    else:
                        #No doc string put none
                        if docsStrClass == "":
                            docsStrClass = None
                        #New class is found and a previous class put to a result list
                        self.componentListAppend(componentList, methodName, int(methodNumber), int(lineNumber), docsStrClass)
                        methodNumber = 0
                        lineNumber = 0
                        docsStrClass = ""
                        docStrCount = 0
                    #Find a method name
                    methodName = self.extractMethodName(aList)
                elif self.isNonIdent(line):
                    #Find methods are outside a class 
                    if methodTrigger == True:
                        #No doc string put none
                        if docsStrClass == "":
                            docsStrClass = None
                        #New class is found and a previous class put to a result list
                        self.componentListAppend(componentList, methodName, int(methodNumber), int(lineNumber), docsStrClass)
                        methodNumber = 0
                        lineNumber = 0
                        docsStrClass = ""
                        docStrCount = 0
                        #End of a method
                        methodTrigger = False
                    if classTrigger == True:
                        #No doc string put none
                        if docsStrClass == "":
                                docsStrClass = None
                            #New class is found and a previous class put to a result list
                        self.componentListAppend(componentList, className, int(methodNumber), int(lineNumber), docsStrClass)
                        methodNumber = 0
                        lineNumber = 0
                        docsStrClass = ""
                        docStrCount = 0
                        classTrigger = False
                if classTrigger == True or methodTrigger == True:
                    #Count lines of a class
                    if not self.isOneLineDocString(aList, line) and not self.isWhiteSpace(line) and not self.isComment(line) and not self.isMultipleLine(line):
                        lineNumber += 1
                    #Count methods of a class and '#' not in line
                    if self.isMethod(line):
                        methodNumber += 1
            #Detect doc strip
            if self.isOneLineDocString(aList, line):
                #End of doc string
                docsStrTrigger = ""
                if classTrigger == True or methodTrigger == True:
                    if aList[0] == "\"" or aList[0] == "\'":
                        #Count doc string
                        docStrCount += 1
                    if docStrCount == 1:
                        #Save a doc string
                        docsStrClass += line
            if  classTrigger == True or methodTrigger == True:
                if docsStrTrigger != "" and docStrCount == 1:
                    #Increase doc string
                    docsStrClass += line
            if docsStrTrigger == "Found":
                #End of doc string
                docsStrTrigger = "" 
        if classTrigger == True :
            #No doc string put none
            if docsStrClass == "":
                docsStrClass = None
            #The last class put to a result list
            self.componentListAppend(componentList, className, int(methodNumber), int(lineNumber), docsStrClass)
        elif methodTrigger == True :
            #No doc string put none
            if docsStrClass == "":
                docsStrClass = None
            #The Method class put to a result list
            self.componentListAppend(componentList, methodName, int(methodNumber), int(lineNumber), docsStrClass)
        return componentList
    
    #Check a python file
    def isPy(self, fileName):
        #Position of invalid file name 
        result = False
        aDotPosition = len(fileName) - 3
        dot = fileName[int(aDotPosition):]
        if dot == ".py":
            result = True
        return result 
    
    #Add a component to a list
    def componentListAppend(self, componentList, className, methodNumber, lineNumber, description):
        resultComponentList = componentList
        resultComponentList.append(Component(className, int(methodNumber), int(lineNumber), description))
        return resultComponentList
    
    #Find a class name in a line
    def extractClassName(self, aList):
        classIndex = aList.index('class') + 1
        fullClassName = aList[classIndex]
        endOfClassName = fullClassName.index('(')
        className = fullClassName[:endOfClassName]
        return className
    
    #Check an empty line
    def isWhiteSpace(self, line):
        result = False
        groupWhiteSpace = re.search("^\s+$", line)
        if groupWhiteSpace != None :
            result = True
        return result
    
    #Check comment
    def isComment(self, line):
        result = False
        comment = re.search("^\s*#.*", line)
        if comment != None :
            result = True
        return result
    
    #Check one line doc string
    def isOneLineDocString(self, aList, line):
        result = False
        if len(aList) > 1:
            if aList[0] == "\"\"\"" or aList[0] == "\'\'\'" or aList[0] == "\'" or aList[0] == "\"":
                if aList[-1] == "\"\"\"" or aList[-1] == "\'\'\'" or aList[-1] == "\'" or aList[-1] == "\"":
                    result = True
        return result
    
    #Check class
    def isClass(self, line):
        result = False
        aClass = re.search("^\s*class .+$", line)
        if aClass != None:
            result = True
        return result
    
    #Check Mehtod
    def isMethod(self, line):
        result = False
        aMethod = re.search("^\s*def .+$", line)
        if aMethod != None:
            result = True
        return result
    
    #Find Open doc string
    def findOpenDocString(self, line):
        result = ""
        aOpenDocString = re.search("\s*\'{3}\s*|\s*\"{3}\s*", line)
        aSix = re.search('\s*\"{6}\s*|\s*\'{6}\s*', line)
        if aOpenDocString != None and aSix == None:
            result = aOpenDocString.group(0)
            result = result.strip()
        return result
    
    #Find an independent method
    def isIndependentMethod(self, line):
        result = False
        aMethod = re.search("^def .+$", line)
        if aMethod != None:
            result = True
        return result
    
    #Find a name of method
    def extractMethodName(self, aList):
        methodIndex = aList.index('def') + 1
        fullMethodName = aList[methodIndex]
        endOfMethodName = fullMethodName.index('(')
        methodName = fullMethodName[:endOfMethodName]
        return methodName
    
    #Find an end of class or method
    def isNonIdent(self, line):
        result = ""
        aNonIdent = re.search("^\w+", line)
        if aNonIdent != None:
            result = aNonIdent.group(0)
            result = result.strip()
        return result
    
    #Find \ at the end of line
    def isMultipleLine(self, line):
        result = ""
        aMultipleLine = re.search("\\\\\s*$", line)
        if aMultipleLine != None:
            result = aMultipleLine.group(0)
            result = result.strip()
        return result

class CrcCard():   
    
    #Initial CrcCard by name, methodCount, size, and desciotion is optional 
    def __init__(self, name, methodCount, size, description=None):
        #Check parameters
        if isinstance(size, str):
            size = string.upper(size)
        else:
            raise ValueError('Invalid CRC Card')
        if len(name) > 0 and int(methodCount) >= 0 and self.isSize(size):  
            self.size = size
            self.name = name
            self.methodCount = methodCount
            self.description = description
        else:
            raise ValueError('Invalid CRC Card')
    
    #Get a name of CrcCard    
    def getName(self):
        return self.name
    
    #Get a number of method count
    def getMethodCount(self):
        return self.methodCount
    
    #Get size
    def getSize (self):
        return self.size
    
    #Get a description of CrcCard
    def getDescription (self):
        return self.description
    
    #Check a valid size
    def isSize(self, size):
        if(size == "VS" or size == "S" or size == "M" or size == "L" or size == "VL"):
            return True
        else:
            return False
        
class SizeMatrix():
    
    #initial a SizeMatrix 
    def __init__(self):
        self.validCountValue = 0
        self.componentList = []
        self.aValidComponent = None
    
    #Add a component to a SizeMethod object   
    def addComponent(self, component):  
        if isinstance(component, Component):
            self.componentList.append(component)
            if component.getMethodCount() > 0:
                self.validCountValue = self.validCountValue + 1
                self.aValidComponent = component
        return len(self.componentList)
    
    #Get a number of components
    def count(self):
        return len(self.componentList)
    
    #Get a number of valid components
    def validCount(self):
        return self.validCountValue
    
    #EstimateSize of a CrcCard and return a component
    def estimateSize(self, aCrcCard):
        
        relativeSizeValue = 0
        
        if isinstance(aCrcCard, CrcCard):
            if aCrcCard.getMethodCount() > 0:
                if self.validCountValue > 1:
                    aBucket = Buckets()
                    aBucket.buildLogNormal(self.componentList) 
                    relativeSizeValue = self.relativeSize(aBucket, aCrcCard.getSize())
                elif self.validCountValue == 1: 
                    relativeSizeValue = self.aValidComponent.getLocCount() / self.aValidComponent.getMethodCount()
                    
                locCount = relativeSizeValue * aCrcCard.getMethodCount()
                aComponent = Component(aCrcCard.getName(), aCrcCard.getMethodCount(), locCount, aCrcCard.getDescription())
                return aComponent
            else:
                raise ValueError('Insufficient size matrix') 
            
    #Find a relativeSize        
    def relativeSize(self, aBucket, size):
        if size == "VS":
            return aBucket.vs
        elif size == "S":
            return aBucket.s
        elif size == "M":
            return aBucket.m
        elif size == "L":
            return aBucket.l
        elif size == "VL":
            return aBucket.vl
        
class ComponentIterationMap():

    #initial a ComponentIterationMap
    def __init__(self, numberOfIterations):
        if isinstance(numberOfIterations, int) and numberOfIterations > 0:
            self.numberOfIterations = numberOfIterations
            self.sumComponents = 0
            self.componentList = []
            self.index = -1
        else: 
            raise ValueError('Invalid number of iterations')
    
    def addComponent(self, component, iList):
        if isinstance(component, Component) and len(iList) <= self.numberOfIterations:
            aComponetList = [component.getName()]
            for x in iList:
                if x < 0:
                    raise ValueError('Invalid number of iterations')
                if isinstance(x, int):
                    self.sumComponents = self.sumComponents + x
                else:
                    raise ValueError('Invalid number of iterations')
                aComponetList.append(x)
            pass
            if self.sumComponents >= component.getMethodCount():
                self.componentList.append(aComponetList)
            else:
                raise ValueError('Invalid number of iterations')
        else: 
            raise ValueError('Invalid number of iterations')
        return len(self.componentList)
    
    def __iter__(self):
        return self
    
    def next(self):
        if self.index == len(self.componentList) - 1:
            raise StopIteration
        self.index = self.index + 1
        return self.componentList[self.index]
    
    def getNumberOfIterations(self):
        return self.numberOfIterations
    
class Calendar():
    def __init__(self):
        self.dayList = []
        self.index = -1
    
    def addDay(self, effort):
        if effort > 0:
            self.dayList.append(effort)
        else:
            raise ValueError('Invalid day')
        return len(self.dayList)
    
    def __iter__(self):
        return self
    
    def next(self):
        if self.index == len(self.dayList) - 1:
            raise StopIteration
        self.index = self.index + 1
        return self.dayList[self.index]

class Schedule():
    
    def __init__(self, componentIterationMap, calendar):
        if isinstance(componentIterationMap, ComponentIterationMap) and isinstance(calendar, Calendar):
            self.componentIterationMap = componentIterationMap
            self.calendar = []
            self.iterations = componentIterationMap.getNumberOfIterations()
            self.allIteration = 0
            #Build a iteration table by a list
            self.summaryIteration = [0] * self.iterations
            
            #iter object is not refresh, so it must put to the list
            for y in calendar:
                self.calendar.append(y)
            
            #Calculate for all iterations
            for x in componentIterationMap:
                for index2, value2 in enumerate(x):
                        if index2 != 0:
                            self.summaryIteration[index2 - 1] = self.summaryIteration[index2 - 1] + value2
            for y in self.summaryIteration:
                self.allIteration = self.allIteration + y
        else:
            raise ValueError('Empty Component-Iteration Map')
    
    def getProjectEndDay(self, effort):
        numberOfday = 0
        sumMinutes = 0
        
        if effort >= 0:
            for x in self.calendar:
                sumMinutes = sumMinutes + x
                #Result of day which it will finish
                numberOfday = numberOfday + 1
                if sumMinutes >= effort:
                    return numberOfday
        else:
            raise ValueError('Invalid effort')
        
    def getInterationPv(self, iterationNumber):
        if iterationNumber >= 0:
            return self.summaryIteration[iterationNumber - 1]
        else:
            raise ValueError('No such iteration')
    
    def getIterationEndDay(self, effort, iterationNumber):
        sumEffort = 0
        sumMinutes = 0
        
        if iterationNumber > 0:
            if effort > 0: 
                #Calculate effort and then calculate time
                for x in self.summaryIteration[0:iterationNumber]:
                    sumEffort = int(float(sumEffort) + float(x) / float(self.allIteration) * float(effort))
                for index1, value1 in enumerate(self.calendar):
                    sumMinutes = sumMinutes + value1
                    if sumMinutes >= sumEffort:
                        return index1 + 1
            else:
                raise ValueError('Invalid Effort')
        else:
            raise ValueError('No such iteration')
        
    def getIterationBurndown(self, effort, iterationNumber):
        sumEffort = 0
        if iterationNumber > 0:
            if effort > 0: 
                for x in self.summaryIteration[0:iterationNumber]:
                    #Calculate effort usage
                    sumEffort = int(float(sumEffort) + float(x) / float(self.allIteration) * float(effort))
                return int(effort - sumEffort)
            else:
                raise ValueError('Invalid Effort')
        else:
            raise ValueError('No such iteration')
