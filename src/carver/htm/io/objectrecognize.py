'''
Created on Feb 1, 2011

@author: Jason
'''
from carver.htm.ui.excite_history import ExciteHistory

class ObjectRecognize(object):
    'assumes always equal matrix dimensions'
    
    def __init__(self):
        self.dataSets = {}
        
    def label(self, name, dataSet):
        'store this dataSet as the canonical example'
        self.dataSets[name] = dataSet
        
    def match(self, name, dataSet):
        'what is the percentage match to the canonical example?'
        canonical = self.dataSets[name]
        
        success_total = 0
        total = 0
        for x in xrange(len(canonical)):
            if canonical[x] == ExciteHistory.ACTIVE:
                if dataSet[x] == ExciteHistory.ACTIVE:
                    success_total += 1
                total += 1
                
        return float(success_total)/total
    
    def _percentMatch(self, name, dataSet):
        return '%.1f%%' % (100*self.match(name, dataSet))
    
    def getMatchData(self, nameList, dataSets):
        datamatrix = []
        for name in nameList:
            datarow = map(lambda data: self.match(name, data), dataSets)
            datamatrix.append(datarow)
        return datamatrix
    
    def getMatchText(self, nameList, dataSets):
        info = ["Data dataSets in columns, tested against named labels in rows:"]
        datamatrix = self.getMatchData(nameList, dataSets)
        for idx, row in enumerate(datamatrix):
            datarow = '\t'.join(map(lambda percent: '%.1f%%' % (100*percent), row))
            info.append("%s:\t%s" % (nameList[idx], datarow))
            
        return '\n'.join(info)
