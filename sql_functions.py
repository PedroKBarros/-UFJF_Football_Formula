import pymysql
import aux_functions

#Data Base constants
DB_NAME = 'UFJF_Modelo_Futebol'
DB_USER = 'Pedro Barros'
DB_PASSWORD = '712Ax2+712bx+c=0'

#constants values
VAL_INTERNO_TYPE_FATOR = 'Interno'
VAL_EXTERNO_TYPE_FATOR = 'Externo'
VAL_ON_STATUS_FATOR = 'On'
VAL_OFF_STATUS_FATOR = 'Off'
VAL_1_AS_TRUE = '1'
VAL_Y_AS_YES = 'Y'
VAL_REQUIRED = 'required'

#Data request phrases constants
PHR_NAME_NEW_TUPLE_TABLE_FATOR = 'Enter the factor name (required): '
PHR_STATUS_NEW_TUPLE_TABLE_FATOR = 'Enter the factor status (' + VAL_1_AS_TRUE + ' for \'true\' or anything for \'false\'): '
PHR_TYPE_NEW_TUPLE_TABLE_FATOR = 'Enter the factor type (' + VAL_1_AS_TRUE + ' for \'' + VAL_INTERNO_TYPE_FATOR + '\'' + ' or anything for \'' + VAL_EXTERNO_TYPE_FATOR + '\'): '
PHR_NAME_NEW_TUPLE_TABLE_PESO = 'Enter the weight name (' + VAL_REQUIRED + '): '
PHR_FACTOR_NEW_TUPLE_TABLE_PESO = 'Enter the name of the factor to which the weight will belong ('+ VAL_REQUIRED + '): '
PHR_VALUE_NEW_TUPLE_TABLE_PESO = 'Enter the value of weight (' + VAL_REQUIRED + '): '
PHR_OPTION_PRESENTATION_FACTORS = 'Show factor names only (\'' + VAL_Y_AS_YES + '\' for \'yes\' or anything to show all informations)? '
PHR_OPTION_PRESENTATION_WEIGHTS = 'Show weight names only (\'' + VAL_Y_AS_YES + '\' for \'yes\' or anything to show all informations)? '
PHR_NAME_CHANGE_FACTOR_STATUS = 'Enter the name of factor: '
PHR_STATUS_CHANGE_FACTOR_STATUS = 'Enter the factor status (' + VAL_1_AS_TRUE + ' for \'true\' or anything for \'false\'): '
PHR_NAME_NEW_TUPLE_TABLE_TIME = 'Enter the team name (required): '

#Constant output data phrases
PHROUT_HEADER_PRESENT_ALL_FACTORS = '\n__________________ FACTORS __________________'
PHROUT_TOTAL_PRESENT_ALL_TABLES = 'Total: '
PHROUT_FOOTER_PRESENT_ALL_FACTORS = "_____________________________________________"
PHROUT_STATUS_FORMAT_SHOWING_ALL_ATTRIBUTES_PRESENT_ALL_FACTORS = "    Status: "
PHROUT_TIPO_FORMAT_SHOWING_ALL_ATTRIBUTES_PRESENT_ALL_FACTORS = "    Tipo: "
PHROUT_ITEM_CHARACTER = ">"
PHROUT_HEADER_PRESENT_ALL_WEIGHTS = '__________________ WEIGHTS __________________'
PHROUT_FOOTER_PRESENT_ALL_WEIGHTS = "_____________________________________________"
PHROUT_FACTOR_NAME_FORMAT_SHOWING_ALL_ATTRIBUTES_PRESENT_ALL_WEIGHTS = "    Factor Name: "
PHROUT_VALUE_FORMAT_SHOWING_ALL_ATTRIBUTES_PRESENT_ALL_WEIGHTS = "    Value: "
PHROUT_CURRENT_VALUE_CHANGE_FACTOR_STATUS = 'Current Status: '
PHROUT_HEADER_PRESENT_ALL_TEAMS = '__________________ TEAMS __________________'
PHROUT_FOOTER_PRESENT_ALL_TEAMS = "_____________________________________________"

#constants ANSI code colors
ANSI_DEFAULT_FINAL_COLOR_CODE = '\033[0;0m'
ANSI_GREEN_INITIAL_CODE = '\033[32m'
ANSI_RED_INITIAL_CODE = '\033[31m'

def establishConnectionDB():
    conexao = pymysql.connect(db=DB_NAME, user=DB_USER, passwd=DB_PASSWORD)
    return conexao

def isAnExistingFactor(DBConnection, factorName):
    cursor = DBConnection.cursor()
    cursor.execute("SELECT NOME FROM FATOR\
                    WHERE NOME = '" + factorName + "'")
    queryResult = cursor.fetchone()
    return queryResult != None

def isAnExistingWeight(DBConnection, weightName):
    cursor = DBConnection.cursor()
    cursor.execute("SELECT NOME FROM PESO\
                    WHERE NOME = '" + weightName + "'")
    queryResult = cursor.fetchone()
    return queryResult != None

def getsAttributeNameNewTupleTableFator(DBConnection):
    name = input(PHR_NAME_NEW_TUPLE_TABLE_FATOR)
    if (name == ''):
        aux_functions.showErrorMessage(2)
        return None
    if (len(name) > 45):
        aux_functions.showErrorMessage(4)
        return None
    if (isAnExistingFactor(DBConnection, name)):
        aux_functions.showErrorMessage(12)
        return None

    return name.upper()

def getsAttributeStatusNewTupleTableFator():
    status = input(PHR_STATUS_NEW_TUPLE_TABLE_FATOR)
    if (status == VAL_1_AS_TRUE):
        statusBool = True
    else:
        statusBool = False

    return statusBool

def getsAttributeTypeNewTupleTableFator():
    factorType = input(PHR_TYPE_NEW_TUPLE_TABLE_FATOR)
    if (factorType == VAL_1_AS_TRUE):
        factorType = VAL_INTERNO_TYPE_FATOR
    else:
        factorType = VAL_EXTERNO_TYPE_FATOR 
    
    return factorType.upper()

def InsertTupleTableFator(DBConnection):
    name = ''
    status = False
    factorType = ''
    name = getsAttributeNameNewTupleTableFator(DBConnection)
    if (name == None):
        return
    status = getsAttributeStatusNewTupleTableFator()
    factorType = getsAttributeTypeNewTupleTableFator()
    cursor = DBConnection.cursor()
    cursor.execute("INSERT INTO fator(nome, status, tipo) VALUES ('" + name + "', " + str(status) + ", '" + factorType + "')")
    DBConnection.commit()
    aux_functions.showOkMessage(1)

def InsertTupleTablePeso(DBConnection):
    name = ''
    factorName = ''
    valor = 0.00

    if (not IsThereFactor(DBConnection)):
        aux_functions.showErrorMessage(3)
        return
    name = getsAttributeNameNewTupleTablePeso(DBConnection)
    if (name == None):
        return
    factorName = getsAttributeFactorNameNewTupleTablePeso(DBConnection)
    if (factorName == None):
        return
    valor = getsAttributeValueNewTupleTablePeso()
    if (valor == None):
        return

    cursor = DBConnection.cursor()
    cursor.execute("INSERT INTO peso(nome, nomefator, valor) VALUES ('" + name + "', '" + factorName + "', " + str(valor) + ")")
    DBConnection.commit()
    aux_functions.showOkMessage(2)

def getsAttributeNameNewTupleTablePeso(DBConnection):
    name = input(PHR_NAME_NEW_TUPLE_TABLE_PESO)
    if (name == ''):
        aux_functions.showErrorMessage(5)
        return None
    if (len(name) > 60):
        aux_functions.showErrorMessage(6)
        return None
    if (isAnExistingWeight(DBConnection, name)):
        aux_functions.showErrorMessage(11)
        return None
    
    
    return name.upper()

def getsAttributeFactorNameNewTupleTablePeso(DBConnection):
    factorName = input(PHR_FACTOR_NEW_TUPLE_TABLE_PESO)
    if (factorName == '' or len(factorName) > 45):
        aux_functions.showErrorMessage(7)
        return None
    if (not isAnExistingFactor(DBConnection, factorName)):
        aux_functions.showErrorMessage(8)
        return None
    
    return factorName.upper()      

def getsAttributeValueNewTupleTablePeso():
    strValue = input(PHR_VALUE_NEW_TUPLE_TABLE_PESO)
    floatValue = float(strValue)
    if (not aux_functions.isNumberInRange(floatValue, 0.00, 1.00)):
        aux_functions.showErrorMessage(9)
        return None
    
    return floatValue

def IsThereFactor(DBConnection):
    cursor = DBConnection.cursor()
    cursor.execute("SELECT COUNT(NOME) From FATOR")
    queryResult = cursor.fetchone()
    return queryResult[0] > 0

def IsThereWeight(DBConnection):
    cursor = DBConnection.cursor()
    cursor.execute("SELECT COUNT(NOME) From PESO")
    queryResult = cursor.fetchone()
    return queryResult[0] > 0

def presentsAllFactors(DBConnection):
    if (not IsThereFactor(DBConnection)):
        aux_functions.showErrorMessage(3)
        return

    option = getsOptionPresentationFactors()
    cursor = DBConnection.cursor()
    optionUpper = option.upper()
    if (optionUpper == VAL_Y_AS_YES):
        cursor.execute('SELECT NOME FROM FATOR')
        isShowOnlyName = True
    else:
        cursor.execute('SELECT * FROM FATOR')
        isShowOnlyName = False
    
    queryResult = cursor.fetchall()
    formattedResult = formatResultQueryTableFactor(queryResult, isShowOnlyName)
    print('\n' + PHROUT_HEADER_PRESENT_ALL_FACTORS)
    print(PHROUT_TOTAL_PRESENT_ALL_TABLES + str(len(queryResult)) + '\n')
    print(formattedResult)
    print(PHROUT_FOOTER_PRESENT_ALL_FACTORS)


def formatResultQueryTableFactor(queryResult, isShowOnlyName):
    if (isShowOnlyName):
        formattedResult = formatResultQueryTableFactorShowingName(queryResult)
    else:
        formattedResult = formatResultQueryTableFactorShowingAllAttributes(queryResult)
    
    return formattedResult

def formatResultQueryTableFactorShowingName(queryResult):
    formattedResult = ''
    for result in queryResult:
        formattedResult += PHROUT_ITEM_CHARACTER + result[0] + '\n'
    
    return formattedResult

def formatResultQueryTableFactorShowingAllAttributes(queryResult):    
    formattedResult = ''
    status = ''
    for result in queryResult:
        formattedResult += PHROUT_ITEM_CHARACTER + result[0] + '\n'
        status = bool(result[1])
        if (status):
            statusStr = ANSI_GREEN_INITIAL_CODE + VAL_ON_STATUS_FATOR + ANSI_DEFAULT_FINAL_COLOR_CODE
        else:
            statusStr = ANSI_RED_INITIAL_CODE + VAL_OFF_STATUS_FATOR + ANSI_DEFAULT_FINAL_COLOR_CODE
        formattedResult += PHROUT_STATUS_FORMAT_SHOWING_ALL_ATTRIBUTES_PRESENT_ALL_FACTORS + statusStr + '\n'
        formattedResult += PHROUT_TIPO_FORMAT_SHOWING_ALL_ATTRIBUTES_PRESENT_ALL_FACTORS + result[2] + '\n'

    return formattedResult

def getsOptionPresentationFactors():
    option = input(PHR_OPTION_PRESENTATION_FACTORS)
    return option
        
def presentsAllWeights(DBConnection):
    if (not IsThereWeight(DBConnection)):
        aux_functions.showErrorMessage(13)
        return

    option = getsOptionPresentationWeights()
    cursor = DBConnection.cursor()
    optionUpper = option.upper()
    if (optionUpper == VAL_Y_AS_YES):
        cursor.execute('SELECT NOME FROM PESO')
        isShowOnlyName = True
    else:
        cursor.execute('SELECT * FROM PESO')
        isShowOnlyName = False
    
    queryResult = cursor.fetchall()
    formattedResult = formatResultQueryTableWeight(queryResult, isShowOnlyName)
    print('\n' + PHROUT_HEADER_PRESENT_ALL_WEIGHTS)
    print(PHROUT_TOTAL_PRESENT_ALL_TABLES + str(len(queryResult)) + '\n')
    print(formattedResult)
    print(PHROUT_FOOTER_PRESENT_ALL_WEIGHTS)

def getsOptionPresentationWeights():
    option = input(PHR_OPTION_PRESENTATION_WEIGHTS)
    return option
    
def formatResultQueryTableWeight(queryResult, isShowOnlyName):
    if (isShowOnlyName):
        formattedResult = formatResultQueryTableWeightShowingName(queryResult)
    else:
        formattedResult = formatResultQueryTableWeightShowingAllAttributes(queryResult)
    
    return formattedResult
    
def formatResultQueryTableWeightShowingName(queryResult):
    formattedResult = ''
    for result in queryResult:
        formattedResult += PHROUT_ITEM_CHARACTER + result[0] + '\n'
    
    return formattedResult

def formatResultQueryTableWeightShowingAllAttributes(queryResult):    
    formattedResult = ''
    for result in queryResult:
        formattedResult += PHROUT_ITEM_CHARACTER + result[0] + '\n'
        formattedResult += PHROUT_FACTOR_NAME_FORMAT_SHOWING_ALL_ATTRIBUTES_PRESENT_ALL_WEIGHTS + result[1] + '\n'
        formattedResult += PHROUT_VALUE_FORMAT_SHOWING_ALL_ATTRIBUTES_PRESENT_ALL_WEIGHTS + str(result[2]) + '\n'

    return formattedResult

def changeFactorStatus(DBConnection):
    if (not IsThereFactor(DBConnection)):
        aux_functions.showErrorMessage(3)
        return

    nameFactor = getsFactorNameChangeStatus(DBConnection)
    if (nameFactor == None):
        return
    status = bool(factorStatus(DBConnection, nameFactor))
    if (status):
        statusStr = ANSI_GREEN_INITIAL_CODE + VAL_ON_STATUS_FATOR + ANSI_DEFAULT_FINAL_COLOR_CODE
    else:
        statusStr = ANSI_RED_INITIAL_CODE + VAL_OFF_STATUS_FATOR + ANSI_DEFAULT_FINAL_COLOR_CODE

    print(PHROUT_CURRENT_VALUE_CHANGE_FACTOR_STATUS + statusStr)
    newStatus = getsNewStatusChangeStatus()
    newStatusStr = str(newStatus)
    if (status == newStatus):
        aux_functions.showErrorMessage(15)
        return

    cursor = DBConnection.cursor()
    cursor.execute("UPDATE FATOR SET STATUS = " + newStatusStr + " WHERE NOME = '" + nameFactor + "'")
    DBConnection.commit()
    aux_functions.showOkMessage(3)


def getsFactorNameChangeStatus(DBConnection):
    factorName = input(PHR_NAME_CHANGE_FACTOR_STATUS)
    if (factorName == '' or len(factorName) > 45):
        aux_functions.showErrorMessage(14)
        return None
    if (not isAnExistingFactor(DBConnection, factorName)):
        aux_functions.showErrorMessage(8)
        return None
    
    return factorName

def getsNewStatusChangeStatus():
    newStatus = input(PHR_STATUS_CHANGE_FACTOR_STATUS)
    if (newStatus == VAL_1_AS_TRUE):
        statusBool = True
    else:
        statusBool = False

    return statusBool

def factorStatus(DBConnection, factorName):
    cursor = DBConnection.cursor()
    cursor.execute('SELECT STATUS FROM FATOR\
                    WHERE \
                        NOME = \'' + factorName + '\'')
    queryResult = cursor.fetchone()
    if (queryResult == None):
        return -1
    
    return queryResult[0]

def isAnExistingTeam(DBConnection, teamName):
    cursor = DBConnection.cursor()
    cursor.execute("SELECT NOME FROM TIME\
                    WHERE NOME = '" + teamName + "'")
    queryResult = cursor.fetchone()
    return queryResult != None

def getsAttributeNameNewTupleTableTime(DBConnection):
    name = input(PHR_NAME_NEW_TUPLE_TABLE_TIME)
    if (name == ''):
        aux_functions.showErrorMessage(16)
        return None
    if (len(name) > 100):
        aux_functions.showErrorMessage(17)
        return None
    if (isAnExistingTeam(DBConnection, name)):
        aux_functions.showErrorMessage(18)
        return None

    return name.upper()

def InsertTupleTableTime(DBConnection):
    name = ''
    name = getsAttributeNameNewTupleTableTime(DBConnection)
    if (name == None):
        return

    cursor = DBConnection.cursor()
    cursor.execute("INSERT INTO time(nome) VALUES ('" + name + "')")
    DBConnection.commit()
    aux_functions.showOkMessage(5)


def IsThereTeam(DBConnection):
    cursor = DBConnection.cursor()
    cursor.execute("SELECT COUNT(NOME) From TIME")
    queryResult = cursor.fetchone()
    return queryResult[0] > 0

def presentsAllTeams(DBConnection):
    if (not IsThereTeam(DBConnection)):
        aux_functions.showErrorMessage(19)
        return

    cursor = DBConnection.cursor()
    cursor.execute('SELECT * FROM TIME')    
    queryResult = cursor.fetchall()
    formattedResult = formatResultQueryTableTeam(queryResult)
    print('\n' + PHROUT_HEADER_PRESENT_ALL_TEAMS)
    print(PHROUT_TOTAL_PRESENT_ALL_TABLES + str(len(queryResult)) + '\n')
    print(formattedResult)
    print(PHROUT_FOOTER_PRESENT_ALL_TEAMS)

def formatResultQueryTableTeam(queryResult):
    formattedResult = ''
    for result in queryResult:
        formattedResult += PHROUT_ITEM_CHARACTER + result[0] + '\n'

    return formattedResult