def file_deletion():
    file_to_delete = input('File to delete: ')
    print(f'Deleting <{file_to_delete}>\n')
    input('Push enter to retun to menu')

def file_creation():
    pass

def show_menu():
    print ("\nGCP for DBs in a hurry-UP Menu")
    print ("-----------------")
    print ("1) Projects")
    print ("2) CloudSQLs")
    print ("3) Databases")
    print ("4) Users")
    print ("5) Export")
    print ("Q) Exit\n")

def menu():
    while True:
        show_menu()
        choice = input('Enter your choice: ').lower()
        if choice == '1':
            cloudsqlprojects()
        elif choice == '2':
            cloudsql()
        elif choice == '3':
            cloudsql_databases()
        elif choice == '4':
            cloudsql_users()
        elif choice == 'q':
            return
        else:
            print(f'Not a correct choice: <{choice}>,try again')

if __name__ == '__main__':
    menu()
