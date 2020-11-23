import pymysql
import aux_functions

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