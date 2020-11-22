import pymysql #biblioteca baixada para manipulação de BDs MySQL

def main():
    conexao = establishConnectionDB()
    try:
        showMainMenu()
        option = returnMainMenuOption()
        cursor = conexao.cursor()
        
    finally: #Todo o código do bloco finally  será executado, caso tenha ocorrido uma exceção ou não
        conexao.close()
    
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

def handlesSelectedMainMenuOption():
    

if __name__ == '__main__':
    main()