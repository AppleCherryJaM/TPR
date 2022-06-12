#Import the required Libraries
from ast import main
from cProfile import label
from operator import index
from tkinter import *
from turtle import RawTurtle
from xml.dom.minidom import TypeInfo
import math


from MultiCriterianDecision import *

class Matrix():
	matrix = []
	valueMatrix = []
	sideSize = 0

	def __init__(self, matrix = list(), lineSize = 0):
		self.matrix = matrix
		self.sideSize = lineSize

	def getMatrix(self):
		return self.matrix

	def getLineSize(self):
		return self.sideSize

	def setMatrix(self, matrix):
		self.sideSize = len(matrix)
		self.matrix = matrix

	def fromArray(self, newValues, sideSize):
		self.sideSize = sideSize
		self.matrix = newValues
		tail = (len(newValues) % self.sideSize)
		if tail > 0:
			tail = self.sideSize-tail
			while tail > 0:
				self.matrix.append(0.0)
				tail -= 1
		
	def getValue(self, rowNum, columnNum):
		index = rowNum * self.sideSize + columnNum
		return self.matrix[index]

	def setValue(self, rowNum, columnNum, value):
		index = rowNum * self.sideSize + columnNum
		self.matrix[index] = value

	def toString(self):
		return str(self.matrix)

# Постійний параметр для початккового рядка вхідної таблиці
DEFAULT_PRIORITY_TABLE_ROW_START = 5
MATRIX_RAW_START = 0

#list for criteria matrix
criteriaValues = []
criteriaMatrix = Matrix()
criteriaPriorities = []
criteriaNumber = 0

#list for alternative's matrix
inputValues = []

objectList = []
objectsNumber = 0

# list of local priorities
localPriorities = list([])

globalPriorities = []

bestChoice = 0


# Ініціалізація вікна програми
root = Tk()
root.title("Entry Boxes")
root.geometry("720x480")

# Пояснення для поля введення кількості альтернатив
labelObjectsText = StringVar()
labelObjectsText.set("Введіть кількість альтернатив: ")
labelObjects = Label(root, textvariable=labelObjectsText, height=4)
labelObjects.grid(row=0, column=0)

# Пояснення для поля введення кількості критеріїв
labelParametersText = StringVar()
labelParametersText.set("Введіть кількість критеріїв: ")
labelParameter = Label(root, textvariable=labelParametersText, height=4)
labelParameter.grid(row=1, column=0)

# Поле вводу кількості альтернатив
entryNumberOfObjects = Entry(root)
entryNumberOfObjects.grid(row=0, column=1, pady=20, padx=5)

# Поле вводу кількості критеріїв
entryNumberOfParameters = Entry(root)
entryNumberOfParameters.grid(row=1, column=1, pady=20, padx=5)

# Генерація елементів вводу приоритетів
def criteriaPriorityFieldsGenerator():
	parametersNumber = int(entryNumberOfParameters.get())

	labelParametersText = StringVar()
	labelParametersText.set("Матриця критеріїв: ")
	labelParameter = Label(root, textvariable=labelParametersText, height=4)
	labelParameter.grid(row=DEFAULT_PRIORITY_TABLE_ROW_START-1, column=0)

	for x in range(parametersNumber):
		for y in range(parametersNumber):
			criteriaEntry = Entry(root)
			criteriaEntry.grid(row=DEFAULT_PRIORITY_TABLE_ROW_START+x, column=y, pady=2)
			criteriaValues.append(criteriaEntry)

		MATRIX_RAW_START = DEFAULT_PRIORITY_TABLE_ROW_START+x

	enterCriteriaPriorityValues = Button(
		root, text="STEP 2", width=15, command=betweenStep12
	)
	enterCriteriaPriorityValues.grid(row=MATRIX_RAW_START+1, column=0, pady=2)
	MATRIX_RAW_START += 2

def objectsCriteriaMatrixGenerator(caption, cord, numberOfObjects):
	line = []
	matrix = []
	
	labelParametersText = StringVar()
	labelParametersText.set("Критерій " + str(caption) + ": ")
	labelParameter = Label(root, textvariable=labelParametersText, height=2)
	labelParameter.grid(row=cord, column=0, pady=2, padx=2)
	cord += 1

	for x in range(numberOfObjects):
		for y in range(numberOfObjects):
			value = Entry(root)
			value.grid(row=cord+x, column=y, pady=2)
			matrix.append(value)
	return matrix


def objectsPriorityFieldsGenerator():
	global criteriaNumber, objectsNumber
	myIterator = 0

	for i in range(criteriaNumber):
		inputValues.append(
			objectsCriteriaMatrixGenerator(
				i, myIterator, objectsNumber
			)
		)
		myIterator += objectsNumber + 1
	enterCapacityButton = Button(root, text="STEP 3", command=betweenStep23)
	if myIterator > 10:
		enterCapacityButton.grid(row=0, column=12, pady=2, padx=15)
	else:
		enterCapacityButton.grid(row=myIterator+1, column=0, pady=2, padx=15)


def windowClear():
	for element in root.winfo_children():
		element.destroy()

def readValues(objects):
	values = list()
	for object in objects:
		if (len(object.get()) == 1):
			values.append(float(object.get()))
		else:
			elem = float(object.get()[0]) / int(object.get()[2])
			values.append(elem)
	return values

def betweenStep12():
	global criteriaNumber, objectsNumber 
	criteriaNumber = int(entryNumberOfParameters.get())
	objectsNumber = int(entryNumberOfObjects.get())
	# Read values
	criteriaMatrix.fromArray(readValues(criteriaValues), criteriaNumber)
	consoleOutput(criteriaMatrix)
	for rowNum in range(objectsNumber):
		row = list()
		for column in range(objectsNumber): # ТУТ МОЖНО ЧЁТ ПОМЕНЯТЬ ДЛЯ РЕШЕНИЯ ТРАБЛА С ВЫХОДОМ ЗА ПРЕДЕЛЫ МАССИВА
			row.append(0.0)
		localPriorities.append(row)

	# Clear previous
	windowClear()
	objectsPriorityFieldsGenerator()


def betweenStep23():
	global criteriaNumber, objectsNumber
	for criteria in range(criteriaNumber):
		matrix = Matrix()
		matrix.fromArray(readValues(inputValues[criteria]), objectsNumber)
		objectList.append(matrix)
	startCalculation()
	
def consoleOutput(matrix):
	for row in range(matrix.getLineSize()):
		outputStr = ""
		for column in range(matrix.getLineSize()):
			outputStr += (", " if outputStr else "") + str(matrix.getValue(row, column))
		print(outputStr)

def theBestChoice(array):
	theBiggestValue = 0
	theBestChoiceNumber = 0
	iterator = 0
	for value in array:
		if value > theBiggestValue:
			theBiggestValue = value
			theBestChoiceNumber = iterator
		iterator += 1
	return "Оптимальним варіантом є об'єкт під номером " + str(theBestChoiceNumber) + " із значенням: " + str(theBiggestValue)

def resultOutput():
	global localPriorities
	output = "Local priorities: \n"
	for row in localPriorities:
		output += str(row) + "\n"
	# output += "Global priorities: \n" + theBestChoice(array)
	return output


def startCalculation():
	global criteriaNumber, objectsNumber
	
	# Розрахування приоритетів матриці критеріїв
	sum = getSum(criteriaMatrix)
	for row in range(criteriaMatrix.getLineSize()):
		lineMulti = 1.0
		for column in range(criteriaMatrix.getLineSize()):
			lineMulti *= criteriaMatrix.getValue(row, column)
		criteriaPriorities.append(math.pow(lineMulti, (1.0/criteriaMatrix.getLineSize())) / sum)

	# Розрахування локальних приоритетів матриць
	for objIndex in range(criteriaNumber):
		sizeOfLine = objectList[objIndex].getLineSize()
		sum = getSum(objectList[objIndex])
		for row in range(sizeOfLine):
			lineMulti = 1.0
			for column in range(sizeOfLine):
				lineMulti *= objectList[objIndex].getValue(row, column)
			localPriorities[row][objIndex] = math.pow(lineMulti, 1.0/sizeOfLine) / sum

  # Розрахування глобальних приоритетів матриць
	for indexAlt in range(len(localPriorities)):
		sum = 0.0
		for criteriaIndex in range(len(localPriorities[indexAlt])):
			sum += localPriorities[indexAlt][criteriaIndex] * criteriaMatrix.getMatrix()[criteriaIndex]
		globalPriorities.append(sum)
	print(globalPriorities)
	result = resultOutput()
	print(result)
	labelParametersText = StringVar()
	labelParametersText.set(result)
	labelParameter = Label(root, textvariable=labelParametersText, height=2)
	labelParameter.grid(row=0, column=15, pady=2, padx=2)
	theBestChoiceLabelText = StringVar()
	theBestChoiceLabelText.set(theBestChoice(globalPriorities))
	theBestChoiceLabel = Label(
		root, textvariable=theBestChoiceLabelText, height=2)
	theBestChoiceLabel.grid(row=2, column=15, pady=2, padx=2)

enterCapacityButton = Button(
	root, text="STEP 1", command=criteriaPriorityFieldsGenerator)

enterCapacityButton.grid(row=1, column=2, pady=2, padx=3)
root.mainloop()
