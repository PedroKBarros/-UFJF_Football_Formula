import pymysql #biblioteca baixada para manipulação de BDs MySQL
import aux_functions
import sql_functions

#Menu Constants
MAIN_MENU_NUM_OPTION1 = '1'
MAIN_MENU_NUM_OPTION2 = '2'
MAIN_MENU_NUM_OPTION3 = '3'
MAIN_MENU_NUM_OPTION4 = '4'
MAIN_MENU_NUM_OPTION5 = '5'
MAIN_MENU_NUM_OPTION6 = '6'
MAIN_MENU_NUM_OPTION7 = '7'
MAIN_MENU_STR_OPTION1 = 'Inserir Fator'
MAIN_MENU_STR_OPTION2 = 'Inserir Peso'
MAIN_MENU_STR_OPTION3 = 'Alterar Status de Fator'
MAIN_MENU_STR_OPTION4 = 'Apresentar Fatores'
MAIN_MENU_STR_OPTION5 = 'Apresentar Pesos'
MAIN_MENU_STR_OPTION6 = 'Criar Simulação'
MAIN_MENU_STR_OPTION7 = 'Sair'

MAIN_MENU_TITLE = 'MAIN MENU'

#Other Constants
MAIN_MENU_OPTION_REQUEST_PHRASE = 'Enter an option number: '

def main():
    DBConnection = sql_functions.establishConnectionDB()
    try:
        showMainMenu()
        option = returnMainMenuOption()
        handlesSelectedMainMenuOption(option, DBConnection)
        
    finally: #Todo o código do bloco finally  será executado, caso tenha ocorrido uma exceção ou não
        DBConnection.close()

def showMainMenu():
    menu = '_____________________ ' + MAIN_MENU_TITLE + ' ____________________\n'
    menu += ' ' + MAIN_MENU_NUM_OPTION1 + '.' + MAIN_MENU_STR_OPTION1 + '\n'
    menu += ' ' + MAIN_MENU_NUM_OPTION2 + '.' + MAIN_MENU_STR_OPTION2 + '\n'
    menu += ' ' + MAIN_MENU_NUM_OPTION3 + '.' + MAIN_MENU_STR_OPTION3 + '\n'
    menu += ' ' + MAIN_MENU_NUM_OPTION4 + '.' + MAIN_MENU_STR_OPTION4 + '\n'
    menu += ' ' + MAIN_MENU_NUM_OPTION5 + '.' + MAIN_MENU_STR_OPTION5 + '\n'
    menu += ' ' + MAIN_MENU_NUM_OPTION6 + '.' + MAIN_MENU_STR_OPTION6 + '\n'
    menu += ' ' + MAIN_MENU_NUM_OPTION7 + '.' + MAIN_MENU_STR_OPTION7 + '\n'             
    menu += '___________________________________________________\n'
    print(menu)

def returnMainMenuOption():
    option = input(MAIN_MENU_OPTION_REQUEST_PHRASE)
    return option

def handlesSelectedMainMenuOption(option, DBConnection):
    if (option == MAIN_MENU_NUM_OPTION1):
        sql_functions.InsertTupleTableFator(DBConnection)
        return
    if (option == MAIN_MENU_NUM_OPTION2):
        sql_functions.InsertTupleTablePeso(DBConnection)
        return
    if (option == MAIN_MENU_NUM_OPTION3):
        return
    if (option == MAIN_MENU_NUM_OPTION4):
        sql_functions.presentsAllFactors(DBConnection)
        return
    if (option == MAIN_MENU_NUM_OPTION5):
        sql_functions.presentsAllWeights(DBConnection)
        return

    aux_functions.showErrorMessage(1)

if __name__ == '__main__':
    main()