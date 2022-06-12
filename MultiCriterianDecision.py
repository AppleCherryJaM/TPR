import math

#Функція для вихначення суми нормованих значень матриці
def getSum (matrix):
	sum = 0.0
	for x in range(matrix.getLineSize()):
		lineMulti = 1.0
		for y in range(matrix.getLineSize()):
			lineMulti *= matrix.getValue(x, y)
		sum += math.pow(lineMulti, 1.0/matrix.getLineSize())
	return sum

#Функція для визначення ставлення узгодженості
def getInconsistency(matrix, priorities):
	sum = 0.0
	for column in range(matrix.getLineSize()):
		columnSum = 0.0
		for row in range(matrix.getLineSize()):
			columnSum += matrix.getValue(row, column)
		sum += priorities[column] * columnSum
	return (((sum - matrix.getLineSize()) / (matrix.getLineSize - 1)) / getRand(matrix.getLineSize))

def getRand(dimension):
	if (dimension == 1):
		return 0.0
	if (dimension == 2):
		return 0.0
	if (dimension == 3):
		return 0.58
	if (dimension == 4):
		return 0.9
	if (dimension == 5):
		return 1.12
	if (dimension == 6):
		return 1.24
	if (dimension == 7):
		return 1.32
	if (dimension == 8):
		return 1.41
	if (dimension == 9):
		return 1.45
	else:
		return 1.49