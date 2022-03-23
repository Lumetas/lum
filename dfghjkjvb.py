import requests
import sys
import os
import progressbar


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



def char_code(c):
    return c.decode('utf-8')


if __name__ == "__main__":
    if len (sys.argv) > 2:
        domen = sys.argv[2]
    else:
        domen = 'f0541993.xsph.ru'

if __name__ == "__main__":
    if len (sys.argv) > 3:
        domen = sys.argv[3]
        if sys.argv[3] == '-s':
            ssl = 'https://'
    else:
        ssl = 'http://'


if __name__ == "__main__":
    if len (sys.argv) > 1:
        print()
    else:
        print("Укажите хотя бы первый аргумент.")
        exit()

url = domen + '/.dd'
url = ssl + url
r = requests.get(url)
print('Поиск пакета: ')
cont = char_code(r.content)
rek = sys.argv[1]
rek = ':' + rek + ':'
lili = len(rek)
rekek = cont[cont.find(rek) + lili:]
link = rekek.partition(';')[0]
print('Пакет найден:')

fname = 'main.zip'
print('Получение пакета:')


download_file(link)




os.system("mkdir main")
os.system("mv main.zip main")
os.system("cd main; unzip main.zip; rm main.zip")
os.system("cd main; sh main.sh;")
os.system("rm -rf main")
