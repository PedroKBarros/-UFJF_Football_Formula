import pymysql #biblioteca baixada para manipulação de BDs MySQL

def main():
    DBConnection = establishConnectionDB()
    try:
        showMainMenu()
        option = returnMainMenuOption()
        handlesSelectedMainMenuOption(option, DBConnection)
        
    finally: #Todo o código do bloco finally  será executado, caso tenha ocorrido uma exceção ou não
        DBConnection.close()
    
def establishConnectionDB():
    conexao = pymysql.connect(db='UFJF_Modelo_Futebol', user='Pedro Barros', passwd='712Ax2+712bx+c=0')
    return conexao

def showMainMenu():
    menu = '__________________ MENU PRINCIPAL __________________\n'
    menu += '|1. Inserir Fator                                  |\n'
    menu += '|2. Inserir Peso                                   |\n'
    menu += '|3. Alterar Status de Fator                        |\n'
    menu += '|4. Criar Simulação                                |\n'
    menu += '___________________________________________________\n'
    print(menu)

def returnMainMenuOption():
    option = input('Enter an option number: ')
    return option

def handlesSelectedMainMenuOption(option, DBConnection):
    if (option == '1'):
        InsertTupleTableFator(DBConnection)
        return
    if (option == '2'):
        InsertTupleTablePeso(DBConnection)
        return
    if (option == '3'):
        return
    if (option == '4'):
        return

    showErrorMessage(1)

def getsAttributeNameNewTupleTableFator():
    name = input('Enter the factor name (required): ')
    if (name == ''):
        showErrorMessage(2)
        return None
    if (len(name) > 45):
        showErrorMessage(4)
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
    name = getsAttributeNameNewTupleTableFator()
    if (name == None):
        return
    status = getsAttributeStatusNewTupleTableFator()
    factorType = getsAttributeTypeNewTupleTableFator()
    cursor = DBConnection.cursor()
    cursor.execute("INSERT INTO fator(nome, status, tipo) VALUES ('" + name + "', " + str(status) + ", '" + factorType + "')")
    DBConnection.commit()
    showOkMessage(1)

def InsertTupleTablePeso(DBConnection):
    name = ''
    factorName = ''
    valor = 0.00

    if (not IsThereFactor(DBConnection)):
        showErrorMessage(3)
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
    showOkMessage(2)

def getsAttributeNameNewTupleTablePeso(DBConnection):
    name = input('Enter the weight name (required): ')
    if (name == ''):
        showErrorMessage(5)
        return None
    if (len(name) > 60):
        showErrorMessage(6)
        return None
    if (isAnExistingWeight(DBConnection, name)):
        showErrorMessage(11)
        return None
    
    
    return name.upper()

def getsAttributeFactorNameNewTupleTablePeso(DBConnection):
    factorName = input('Enter the name of the factor to which the weight will belong (required): ')
    if (factorName == '' or len(factorName) > 45):
        showErrorMessage(7)
        return None
    if (not isAnExistingFactor(DBConnection, factorName)):
        showErrorMessage(8)
        return None

    return factorName.upper()

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
        

def getsAttributeValueNewTupleTablePeso():
    strValue = input('Enter the value of weight (required): ')
    floatValue = float(strValue)
    if (not isNumberInRange(floatValue, 0.00, 1.00)):
        showErrorMessage(9)
        return None
    
    return floatValue
        

def isNumberInRange(number, min, max):
    if (min > max):
        return false
    
    return number >= min and number <= max
    

def IsThereFactor(DBConnection):
    cursor = DBConnection.cursor()
    cursor.execute("SELECT COUNT(NOME) From FATOR")
    queryResult = cursor.fetchone()
    return queryResult[0] > 0

def showErrorMessage(msgCode):
    errMsg = '__________________ ERROR __________________\n'
    if (msgCode == 1):
        errMsg += 'Invalid option.\n'
    if (msgCode == 2):
        errMsg += 'The factor name is required.\n'
    if (msgCode == 3):
        errMsg += 'There is not at least one factor registered.\n'
    if (msgCode == 4):
        errMsg += 'The factor name has exceeded 45 characters.\n'
    if (msgCode == 5):
        errMsg += 'The weight name is required.\n'
    if (msgCode == 6):
        errMsg += 'The weight name has exceeded 60 characters.\n'
    if (msgCode == 7):
        errMsg += 'Name of the factor to which the weight will belong is invalid.\n'
    if (msgCode == 8):
        errMsg += 'This factor does not correspond to any registered factor.\n'
    if (msgCode == 9):
        errMsg += 'The weight value is invalid.\n'
    if (msgCode == 11):
        errMsg += 'The name of the new weight already exists.\n'

    errMsg += '___________________________________________\n'
    print(errMsg)

def showOkMessage(msgCode):
    okMsg = '__________________ OK! __________________\n'
    if (msgCode == 1):
        okMsg += 'Factor inserted successfully!\n'
    if (msgCode == 2):
        okMsg += 'Weight inserted successfully!\n'
    
    okMsg += '_________________________________________\n'
    print(okMsg)


if __name__ == '__main__':
    main()