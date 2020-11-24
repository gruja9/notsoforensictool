import utils

def print_results(finput):
    for item in finput:
        print(item)

def main():
    allfiles = dict()
    specificfiles = dict()
    infofiles = dict()
    datefiles = dict()
    match_hashset = list()

    while True:
        print("\n")
        print("################################################")
        print("# [1]Search  [2]Encryption  [3]File Difference #")
        print("# [4]System Info [5]Generate report            #")
        print('#  q or "exit" to exit                         #')
        print("################################################")
        ch = input("$ ")
        
        # Search in files
        if ch == "1":
            while True:
                print("\n")
                print("##########################################")
                print("# [1] Find all files [2] File Extension  #")
                print("# [3] By date        [4] Search in files #")
                print('#  q or "back" to go back                #')
                print("##########################################")
                ch2 = input("$ ")

                if ch2 == "1":
                    path = input("$ Path to folder: ")
                    if path == "q" or path == "back":
                        break
                    list_tmp = utils.find_all_files(path)
                    utils.create_dict(path, allfiles, list_tmp)
                    match_hashset += utils.verify_files(list_tmp)
                    print_results(list_tmp)

                if ch2 == "2":
                    ext = input("$ Extension: ")
                    if ext == "q" or ext == "back":
                        break

                    folder = input("$ Path to folder: ")
                    if folder == "q" or folder == "back":
                        break
                    list_tmp = utils.find_specific_files(folder, ext)
                    utils.create_dict(ext, specificfiles, list_tmp)
                    match_hashset += utils.verify_files(list_tmp)
                    print_results(list_tmp)
                
                if ch2 == "3":
                    folder = input("$ Path to folder: ")
                    if folder == "q" or folder == "back":
                        break

                    date = input("$ Date (Ex format: 2020-03-03): ")
                    if date == "q" or date == "back":
                        break
                    list_tmp = utils.find_modified_files(folder, date)
                    utils.create_dict(date, datefiles, list_tmp)
                    match_hashset = utils.verify_files(list_tmp)
                    print_results(list_tmp)

                if ch2 == "4":
                    folder = input("$ Path to folder: ")
                    if folder == "q" or folder == "back":
                        break

                    ext = input("$ Extension: ")
                    if ext == "q" or ext == "back":
                        break

                    keyword = input("$ Keyword: ")
                    if keyword == "q" or keyword == "back":
                        break
                    list_tmp = utils.search_files(folder, ext, keyword)
                    utils.create_dict(keyword, infofiles, list_tmp)
                    match_hashset = utils.verify_files(list_tmp)
                    print_results(list_tmp)
                
                if ch2 == "q" or ch2 == "back":
                    break

        #Encryption         
        if ch == "2":
            while True:
                print("\n")
                print("###########################")
                print("# [1] Encrypt [2] Decrypt #")
                print('#  q or "back" to go back #')
                print("###########################")
                ch2 = input("$ ")
                    
                if ch2 == "1":
                    filename = input("$ Path to file: ")
                    if filename == "q" or filename == "back":
                        break
                    
                    utils.encrypt_file(filename)
                    print(filename + " has been encrypted.")
                
                if ch2 == "2":
                    filename = input("$ Path to file: ")
                    if filename == "q" or filename == "back":
                        break

                    utils.decrypt_file(filename)
                    print(filename + "has been decrypted.")


                if ch2 == "q" or ch2 == "back":
                    break


        # File Difference
        if ch == "3":
            while True:
                print("\n")
                print(' q or "back" to go back')
                file1 = input("$ File 1: ")
                if file1 == "q" or file1 == "back":
                    break

                file2 = input("$ File 2: ")
                if file2 == "q" or file2 == "back":
                    break

                file1_diff, file2_diff = utils.word_difference(file1, file2)
                print()
                print("Words in file 1, but not in file 2:")
                print_results(file1_diff)
                print("Words in file 2, but not in file 1:")
                print_results(file2_diff)
        
        # System info
        if ch == "4":
            print_results(utils.system_information())
        
        if ch == "5":
            dictionary = dict()
            dictionary['sys'] = utils.system_information()
            dictionary['hashset'] = match_hashset
            dictionary['allfiles'] = allfiles
            dictionary['extfiles'] = specificfiles
            dictionary['infofiles'] = infofiles
            dictionary['datefiles'] = datefiles
            utils.gen_report(dictionary)
            print("The report has been generated!")

        if ch == "q" or ch == "exit":
            print("\n")
            print(" Cya! ")
            print("\n")
            break


if __name__ == '__main__':
	print('Detta är en modul och ska inte köras självständigt!')
	exit()
