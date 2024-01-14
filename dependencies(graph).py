'''
Уязвимые зависимости
Реализуйте вывод всех путей до уязвимых библиотек для проекта.

Формат входных данных
Данные передаются через стандартный поток ввода.
Первая строка содержит идентификаторы уязвимых библиотек, разделенные пробелом.
Вторая строка содержит идентификаторы прямых зависимостей проекта, разделенные пробелом.
Каждая последующая строка содержит идентификатор зависимости и идентификаторы библиотек, от которых она зависит, разделенные пробелом.

Формат результата
Результат работы программы выводится в стандартный поток вывода.
Каждая строка должна содержать путь (набор идентификаторов, разделенный пробелом) к уязвимой зависимости.
Начало пути — прямая зависимость проекта, конец — уязвимая библиотека.
Порядок строк не имеет значения.
'''
import fileinput

ans=list(set(list(input().split())))
arr=set(list(input().split()))
hashtable={}
for line in fileinput.input():
    splited=list(line.split())
    if len(splited)>0 :
        for i in range(1, len(splited)) :
            if splited[i] in hashtable :
                hashtable[splited[i]].append(splited[0])
            else :
                hashtable[splited[i]]=[]
                hashtable[splited[i]].append(splited[0])
    
def find(path, curr_node, above, printed, hashtable) :
    #print(path, curr_node)
    global arr
    if curr_node in arr :
        if tuple(path) not in printed :
            for i in range(len(path)-1, 0, -1) :
                print(path[i], end=' ') 
            print(path[0])
            printed.add(tuple(path))
    if curr_node in hashtable:
        for k in range(len(hashtable[curr_node])) :
            new_node=hashtable[curr_node][k]
            if new_node not in above :
                above.add(new_node)
                path.append(new_node)
                find(path, new_node, above, printed, hashtable)
    if len(path) :
        path.pop()
        above.remove(curr_node)
    
for m in range(len(ans)) :
    above=set()
    above.add(ans[m])
    path=[]
    path.append(ans[m])
    printed=set()
    find(path, ans[m], above, printed, hashtable)
