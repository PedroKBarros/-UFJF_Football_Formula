import pymysql

def isNumberInRange(number, min, max):
    if (min > max):
        return False
    
    return number >= min and number <= max

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
    if (msgCode == 12):
        errMsg += 'The name of the new factor already exists.\n'

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