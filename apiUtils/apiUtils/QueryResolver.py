import re

class QueryResolver:
    def __init__(self, query):
        self.query = query

    IS_REG=re.compile('/.+/')

    def getDbFilter(self, conditionsList):
        '''Convert 'and' type conditions to db query'''
        print(str(conditionsList))
        dbFilter = {}
        metric = "" #TODO: remove metric when no longer needed in resolving data

        for condition in conditionsList:
            key = condition.split(":")[0]
            value = condition.split(":")[1]

            #TODO: remove when no longer needed
            if key == "metric_id":
                metric = value

            regex = self.IS_REG.match(value)
            if regex:
                regexStr = regex.group()[1:-1]
                dbFilter[key] = re.compile(regexStr)
            else:
                dbFilter[key] = value

        print("dbFilter: " + str(dbFilter))
        print("metric: " + metric)

        #TODO: return only dbFilter
        return [dbFilter, metric]

    def getFilters(self):
        '''Return list of db filters from owned query'''
        filtersList = []

        alternatives = self.query.split(";")
        for alt in alternatives:
            conjunctions = alt.split(",")
            filtersList.append(self.getDbFilter(conjunctions))

        return filtersList



        




