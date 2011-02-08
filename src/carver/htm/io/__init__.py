
def updateMatrix(dataHolder, newData):
    for x in xrange(len(newData)):
        for y in xrange(len(newData[x])):
            dataHolder[x][y] = newData[x][y]
