import pymysql
import aux_functions

#Data Base constants
DB_NAME = 'UFJF_Modelo_Futebol'
DB_USER = 'Pedro Barros'
DB_PASSWORD = '712Ax2+712bx+c=0'

#Data request phrases constants
PHR_NAME_NEW_TUPLE_TABLE_FATOR = 'Enter the factor name (required): '
PHR_STATUS_NEW_TUPLE_TABLE_FATOR = 'Enter the factor status (1 for \'true\' or anything for \'false\'): '
PHR_TYPE_NEW_TUPLE_TABLE_FATOR = 'Enter the factor type (1 for \'Interno\' or anything for \'externo\'): '
PHR_NAME_NEW_TUPLE_TABLE_PESO = 'Enter the weight name (required): '
PHR_FACTOR_NEW_TUPLE_TABLE_PESO = 'Enter the name of the factor to which the weight will belong (required): '
PHR_VALUE_NEW_TUPLE_TABLE_PESO = 'Enter the value of weight (required): '
PHR_OPTION_PRESENTATION_FACTORS = 'Show factor names only (\'y\' for \'yes\' or anything to show all informations)? '
PHR_OPTION_PRESENTATION_WEIGHTS = 'Show weight names only (\'y\' for \'yes\' or anything to show all informations)? '
PHR_NAME_CHANGE_FACTOR_STATUS = 'Enter the name of factor: '
PHR_STATUS_CHANGE_FACTOR_STATUS = 'Enter the factor status (1 for \'true\' or anything for \'false\'): '

#constants values
VAL_INTERNO_TYPE_FATOR = 'Interno'
VAL_EXTERNO_TYPE_FATOR = 'Externo'
VAL_ON_STATUS_FATOR = 'On'
VAL_OFF_STATUS_FATOR = 'Off'

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
    if (status == '1'):
        statusBool = True
    else:
        statusBool = False

    return statusBool

def getsAttributeTypeNewTupleTableFator():
    factorType = input(PHR_TYPE_NEW_TUPLE_TABLE_FATOR)
    if (factorType == '1'):
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
    if (optionUpper == 'Y'):
        cursor.execute('SELECT NOME FROM FATOR')
        isShowOnlyName = True
    else:
        cursor.execute('SELECT * FROM FATOR')
        isShowOnlyName = False
    
    queryResult = cursor.fetchall()
    formattedResult = formatResultQueryTableFactor(queryResult, isShowOnlyName)
    print("\n__________________ FACTORS __________________")
    print('Total: ' + str(len(queryResult)) + '\n')
    print(formattedResult)
    print("_____________________________________________")


def formatResultQueryTableFactor(queryResult, isShowOnlyName):
    if (isShowOnlyName):
        formattedResult = formatResultQueryTableFactorShowingName(queryResult)
    else:
        print("oi\n")
        formattedResult = formatResultQueryTableFactorShowingAllAttributes(queryResult)
    
    return formattedResult

def formatResultQueryTableFactorShowingName(queryResult):
    formattedResult = ''
    for result in queryResult:
        formattedResult += ">" + result[0] + '\n'
    
    return formattedResult

def formatResultQueryTableFactorShowingAllAttributes(queryResult):    
    formattedResult = ''
    status = ''
    for result in queryResult:
        formattedResult += ">" + result[0] + '\n'
        status = bool(result[1])
        if (status):
            statusStr = ANSI_GREEN_INITIAL_CODE + VAL_ON_STATUS_FATOR + ANSI_DEFAULT_FINAL_COLOR_CODE
        else:
            statusStr = ANSI_RED_INITIAL_CODE + VAL_OFF_STATUS_FATOR + ANSI_DEFAULT_FINAL_COLOR_CODE
        formattedResult += "    Status: " + statusStr + '\n'
        formattedResult += "    Tipo: " + result[2] + '\n'

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
    if (optionUpper == 'Y'):
        cursor.execute('SELECT NOME FROM PESO')
        isShowOnlyName = True
    else:
        cursor.execute('SELECT * FROM PESO')
        isShowOnlyName = False
    
    queryResult = cursor.fetchall()
    formattedResult = formatResultQueryTableWeight(queryResult, isShowOnlyName)
    print("\n__________________ WEIGHTS __________________")
    print('Total: ' + str(len(queryResult)) + '\n')
    print(formattedResult)
    print("_____________________________________________")

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
        formattedResult += ">" + result[0] + '\n'
    
    return formattedResult

def formatResultQueryTableWeightShowingAllAttributes(queryResult):    
    formattedResult = ''
    for result in queryResult:
        formattedResult += ">" + result[0] + '\n'
        formattedResult += "    nome: " + result[0] + '\n'
        formattedResult += "    nome do fator: " + result[1] + '\n'
        formattedResult += "    valor: " + str(result[2]) + '\n'

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

    print('Current Status: ' + statusStr)
    newStatus = getsNewStatusChangeStatus()
    newStatusStr = str(newStatus)
    print("NOVO STATUS = " + newStatusStr + "\n")
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
    if (newStatus == '1'):
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