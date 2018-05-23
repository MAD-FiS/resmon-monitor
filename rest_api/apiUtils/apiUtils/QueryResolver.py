import re

class QueryResolver:
    '''This class transforms rest queries into mongo DB usable filters'''

    def __init__(self, query):
        self.query = query

    '''This regexp captures regexes in query'''
    IS_REG=re.compile('/.+/')

    '''Left boundary of pattern matched by regexp'''
    FROM_L_SLASH = 1

    '''Right boundary of pattern matched by regexp'''
    TO_R_SLASH = -1

    '''Means 'or' for separated parts'''
    OR_SEPARATOR=';'

    '''Means 'and' for separated parts'''
    AND_SEPARATOR=',' 

    '''Means 'key value' for separated parts '''
    K_V_SEPARATOR=':'

    
    def getDbFilter(self, conditionsList):
        '''Convert 'and' type conditions to db query'''
        print(str(conditionsList))
        dbFilter = {}

        for condition in conditionsList:
            key, value = condition.split(self.K_V_SEPARATOR)

            regex = self.IS_REG.match(value)
            if regex:
                regexStr = regex.group()[self.FROM_L_SLASH:self.TO_R_SLASH]
                dbFilter[key] = re.compile(regexStr)
            else:
                dbFilter[key] = value

        print("dbFilter: " + str(dbFilter))

        return dbFilter

    def getFilters(self):
        '''Return list of db filters from owned query'''
        filtersList = []
        if not self.query:
            return {}

        alternatives = self.query.split(self.OR_SEPARATOR)
        for alt in alternatives:
            conjunctions = alt.split(self.AND_SEPARATOR)
            filtersList.append(self.getDbFilter(conjunctions))

        return filtersList

