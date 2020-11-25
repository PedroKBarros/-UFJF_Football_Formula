import pymysql
import aux_functions

def establishConnectionDB():
    conexao = pymysql.connect(db='UFJF_Modelo_Futebol', user='Pedro Barros', passwd='712Ax2+712bx+c=0')
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
    name = input('Enter the factor name (required): ')
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
    status = input('Enter the factor status (1 for \'true\' or anything for \'false\'): ')
    if (status == '1'):
        statusBool = True
    else:
        statusBool = False

    return statusBool

def getsAttributeTypeNewTupleTableFator():
    factorType = input('Enter the factor type (1 for \'Interno\' or anything for \'externo\'): ')
    if (factorType == '1'):
        factorType = 'Interno'
    else:
        factorType = 'Externo'  
    
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
    name = input('Enter the weight name (required): ')
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
    factorName = input('Enter the name of the factor to which the weight will belong (required): ')
    if (factorName == '' or len(factorName) > 45):
        aux_functions.showErrorMessage(7)
        return None
    if (not isAnExistingFactor(DBConnection, factorName)):
        aux_functions.showErrorMessage(8)
        return None
    
    return factorName.upper()      

def getsAttributeValueNewTupleTablePeso():
    strValue = input('Enter the value of weight (required): ')
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
        if (status == True):
            statusStr = '\033[32m' + 'On' + '\033[0;0m'
        else:
            statusStr = '\033[31m' + 'Off' + '\033[0;0m'
        formattedResult += "    Status: " + statusStr + '\n'
        formattedResult += "    Tipo: " + result[2] + '\n'

    return formattedResult

def getsOptionPresentationFactors():
    option = input('Show factor names only (\'y\' for \'yes\' or anything to show all informations)? ')
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
    option = input('Show weight names only (\'y\' for \'yes\' or anything to show all informations)? ')
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