import requests
import sys
import os
import progressbar
import os.path

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
    
    
    
    
    
    
    
    
    
    
    
    
elif sys.argv[1] == 'remove':

    if len (sys.argv) > 2:
        com = '/lumRm/' + sys.argv[2]
        if os.path.exists(com) == False:
            exit('Пакет или скрипты удаления не найдены')
        os.system('sudo sh ' + com)
        os.system('sudo rm ' + com)
    exit()
    
    
    
    
    
    
else:
    print('sync or install or remove')
    exit()

