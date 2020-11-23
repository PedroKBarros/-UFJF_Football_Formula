import pymysql #biblioteca baixada para manipulação de BDs MySQL
import aux_functions
import sql_functions

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
        sql_functions.InsertTupleTableFator(DBConnection)
        return
    if (option == '2'):
        sql_functions.InsertTupleTablePeso(DBConnection)
        return
    if (option == '3'):
        return
    if (option == '4'):
        return

    aux_functions.showErrorMessage(1)

if __name__ == '__main__':
    main()