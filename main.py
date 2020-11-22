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
    return name

def getsAttributeStatusNewTupleTableFator():
    status = input('Enter the factor status (1 for true or anything for false): ')
    if (status == '1'):
        statusBool = True
    else:
        statusBool = False

    return statusBool

def getsAttributeTypeNewTupleTableFator():
    factorType = input('Enter the factor type (required): ')
    if (factorType == ''):
        showErrorMessage(3)
        return None
    return factorType

def InsertTupleTableFator(DBConnection):
    name = ''
    status = False
    factorType = ''
    name = getsAttributeNameNewTupleTableFator()
    if (name == None):
        return
    status = getsAttributeStatusNewTupleTableFator()
    factorType = getsAttributeTypeNewTupleTableFator()
    if (factorType == None):
        return
    cursor = DBConnection.cursor()
    cursor.execute("INSERT INTO fator(nome, status, tipo) VALUES ('" + name + "', " + str(status) + ", '" + factorType + "')")
    DBConnection.commit()
        

def showErrorMessage(msgCode):
    errMsg = '__________________ ERROR __________________\n'
    if (msgCode == 1):
        errMsg += 'Invalid option.\n'
    if (msgCode == 2):
        errMsg += 'The factor name is required.\n'
    if (msgCode == 3):
        errMsg += 'The factor type is required.\n'

    errMsg += '___________________________________________\n'
    print(errMsg)


if __name__ == '__main__':
    main()