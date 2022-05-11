lumVersion = '1.0'
from audioop import rms
import requests
import sys
import os
import progressbar
import os.path
import zipfile
def mybackup(arch, folder_list, mode):
    # Счетчики
    num = 0
    num_ignore = 0
    
    z = zipfile.ZipFile(arch, mode, zipfile.ZIP_DEFLATED, True)
    # Получаем папки из списка папок.
    for add_folder in folder_list:
        # Список всех файлов и папок в директории add_folder
        for root, dirs, files in os.walk(add_folder):
            for file in files:
                if file in ignore_file:  # Исключаем лишние файлы
                    print("Исключен! ", str(file))
                    num_ignore += 1
                    continue
                # Создание относительных путей и запись файлов в архив
                path = os.path.join(root, file)
                z.write(path)
                print(num, path)
                num += 1



def download_file(url):
    local_filename = 'main.zip'
    r = requests.get(url, stream=True)
    f = open(local_filename, 'wb')
    file_size = int(r.headers['Content-Length'])
    chunk = 1
    num_bars = file_size / chunk
    bar =  progressbar.ProgressBar(maxval=num_bars).start()
    i = 0
    for chunk in r.iter_content():
        f.write(chunk)
        bar.update(i)
        i+=1
    f.close()
    return
















def sync(url):
    local_filename = '/sync.dd'
    r = requests.get(url, stream=True)
    f = open(local_filename, 'wb')
    file_size = int(r.headers['Content-Length'])
    chunk = 1
    num_bars = file_size / chunk
    bar =  progressbar.ProgressBar(maxval=num_bars).start()
    i = 0
    for chunk in r.iter_content():
        f.write(chunk)
        bar.update(i)
        i+=1
    f.close()
    return


def char_code(c):
    return c.decode('utf-8')





if __name__ == "__main__":
    if len (sys.argv) > 1:
        print
    else:
        print("Укажите хотя бы первый аргумент.")
        exit()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
if sys.argv[1] == 'sync':


    if len (sys.argv) > 2:
        link = sys.argv[2] + '/.dd'
        sync(link)
    else: 
        sync('https://raw.githubusercontent.com/110000110000/lum/repo/.dd')
    exit()
    
    
    
    
    
    
    
    
    
    
elif sys.argv[1] == 'install':

    if os.path.exists('/sync.dd') == False:
        exit('Локальная база данных не обнаружена пожалуйства используйте: sudo lum sync')

    if len (sys.argv) > 2:

        f = open('/sync.dd', 'r')
        cont = f.read()
        rek = sys.argv[2]
        rek = ':' + rek + ':'
        lili = len(rek)
        rekek = cont[cont.find(rek) + lili:]
        link = rekek.partition(';')[0]
        print('Пакет найден:')
 
        print('Получение пакета:')
 
 
        download_file(link)
    
 
 
 
        os.system("mkdir main")
        os.system("mv main.zip main")
        os.system("cd main; unzip main.zip; rm main.zip")
        os.system("cd main; sh main.sh;")
        os.system("rm -rf main")
    exit()
    
    
    
    
elif sys.argv[1] == 'req': 
     if len (sys.argv) > 2:
        print()
        f = open(sys.argv[2], 'r')
        cont = f.read()
        req = cont.split(',')
        [os.system('sudo lum install '+ i) for i in req]
        print(req)
    
    
    
elif sys.argv[1] == 'remove':

    if len (sys.argv) > 2:
        com = '/lumRm/' + sys.argv[2]
        if os.path.exists(com) == False:
            exit('Пакет или скрипты удаления не найдены')
        os.system('sudo sh ' + com)
        os.system('sudo rm ' + com)
    exit()
    
    
    
elif sys.argv[1] == 'make':
    print
    packageName = input('Имя пакета: ')
    installScript = input('Скрипт установки: ')
    rmScript = input('Скрипт для удаления: ')
    makeFile = packageName + ';' + installScript + ';' + rmScript
    f = open('makefile', 'w')
    f.write(makeFile)
    f.close()
    
elif sys.argv[1] == 'build':
    print
    if os.path.exists('makefile') == False:
        exit('Используйте lum make')
    f = open('makefile', 'r')
    cont = f.read()
    makeData = cont.split(';')


    packageName = makeData[0]
    installScript = makeData[1]
    rmScript = makeData[2]





    main ='sudo chmod +x ' + installScript + ' ; ' + 'sudo sh ' + installScript + ' ; '
    main = main + 'sudo chmod +x ' + rmScript + ' ; ' + 'sudo mv ' + rmScript + ' /lumRm/' + packageName



    f = open('main.sh', 'w')
    f.write(main)
    f.close()


    filePackageName = packageName + '.zip'
    ignore_file = [filePackageName]
    mybackup(filePackageName, os.curdir, 'w')
    os.remove('main.sh')


elif sys.argv[1] == '--version':
    print(lumVersion)
    
    
else:
    print('sync or install or remove or req')
    exit()

