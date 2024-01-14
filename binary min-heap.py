from sys import stdin
class heap() :
    def __init__ (self):
        self.arr=[] #массив, в котором будут храниться ключи
        self.length=0 #количество элементов в куче
        self.hashtable={} #словарь, в котором будут храниться пары ключ-значение(поскольку в python словарь реализован хэш-таблицей,операция добавления происходит за амортизированную O(1), а доступ к элементу за O(n).
    def add(self, k, v) :
        #Добавляем ключ в конец кучи и вызываем просеивание вверх. Также добавляем значение по новуму ключу в словарь. Итоговая сложность O(log(n)).
        if k in self.hashtable :
            raise ValueError
        else :
            self.length+=1 
            self.arr.append(k)
            self.hashtable[k]=[0]*2
            self.hashtable[k][0]=v
            self.hashtable[k][1]=self.length-1
            pointer=self.length-1
            while pointer>0 and self.arr[(pointer-1)//2]>self.arr[pointer] :
                self.arr[(pointer-1)//2], self.arr[pointer]= self.arr[pointer], self.arr[(pointer-1)//2]
                self.hashtable[self.arr[(pointer-1)//2]][1], self.hashtable[self.arr[pointer]][1]=self.hashtable[self.arr[pointer]][1], self.hashtable[self.arr[(pointer-1)//2]][1]
                pointer=(pointer-1)//2
            return 0
    def set(self, k, v) :
        #Устанавливаем значение по ключу. Сложность O(1).
        if k in self.hashtable :
            self.hashtable[k][0]=v
            return 0
        else :
            raise ValueError
    def search(self, k) :
        #Возвращаем значение по ключу. Сложность O(1).
        if  k in self.hashtable :
            return self.hashtable[k][1], self.hashtable[k][0]
        else :
            raise ValueError
    def min(self) :
        # Возвращаем значение по ключу в вершине. Сложность O(1).
        if self.length!=0 :
            return self.arr[0], self.hashtable[self.arr[0]][0]
        else :
            raise ValueError
    def max(self) :
        # Возвращаем значение по наибольшему ключу. Учитывая, что  узлы без дочерних узлов не могут быть максимумом, достаточно проверить лишь половину элементов, вместо прохода по всем. Тем не менее в точки зрения O-нотации сложность все равно O(n). 
        if self.length!=0 : 
            ans=self.arr[self.length-1]
            n=int(round(self.length/2,0))
            for i in range(self.length-n, self.length) :
                if self.arr[i]>ans :
                    ans=self.arr[i]
            return ans, self.hashtable[ans][1], self.hashtable[ans][0]
        else :
            raise ValueError
    def extract(self) :
        #Возвращаем и удаляем вершину кучи. После этого копируем наибольший  элемент в вершину и вызываем просеивание вниз. Сложность O{log(n)).
        if self.length!=0 :
            ans=[self.arr[0], self.hashtable[self.arr[0]][0]]
            self.hashtable.pop(self.arr[0])
            self.arr[0]=self.arr[self.length-1]
            self.hashtable[self.arr[self.length-1]][1]=0
            pointer=0 
            while pointer*2+1<self.length-1 :
                min_index=pointer*2+1
                if self.arr[pointer*2+2]<self.arr[min_index] :
                    min_index=pointer*2+2
                if self.arr[pointer]>self.arr[min_index] :
                    self.arr[pointer], self.arr[min_index]=self.arr[min_index], self.arr[pointer]
                    self.hashtable[self.arr[pointer]][1], self.hashtable[self.arr[min_index]][1]=self.hashtable[self.arr[min_index]][1], self.hashtable[self.arr[pointer]][1]
                    pointer=min_index
                else :
                    break
            self.arr.pop()
            self.length-=1
            return ans[0], ans[1]
        else :
            raise ValueError
    def delete(self, k) :
        #Удаляем ключ из кучи, копируем на его место максимальный элемент и вызываем просеивание вниз и вверх. Сложность O(log(n)).
        if k in self.hashtable :
            if self.hashtable[k][1]==self.length-1 :
                self.hashtable.pop(k)
                self.arr.pop()
                self.length-=1
            else :
                self.arr[self.hashtable[k][1]]=self.arr[self.length-1]
                self.hashtable[self.arr[self.length-1]][1]=self.hashtable[k][1]
                pointer=self.hashtable[self.arr[self.length-1]][1]
                self.hashtable.pop(k)
                while pointer*2+1<self.length-1 :
                    min_index=pointer*2+1
                    if self.arr[pointer*2+2]<self.arr[min_index] :
                        min_index=pointer*2+2
                    if self.arr[pointer]>self.arr[min_index] :
                        self.arr[pointer], self.arr[min_index]=self.arr[min_index], self.arr[pointer]
                        self.hashtable[self.arr[pointer]][1], self.hashtable[self.arr[min_index]][1]=self.hashtable[self.arr[min_index]][1], self.hashtable[self.arr[pointer]][1]
                        pointer=min_index
                    else :
                        break
                self.arr.pop()
                self.length-=1
                while pointer>0 and self.arr[(pointer-1)//2]>self.arr[pointer] :
                    self.arr[(pointer-1)//2], self.arr[pointer]= self.arr[pointer], self.arr[(pointer-1)//2]
                    self.hashtable[self.arr[(pointer-1)//2]][1], self.hashtable[self.arr[pointer]][1]=self.hashtable[self.arr[pointer]][1], self.hashtable[self.arr[(pointer-1)//2]][1]
                    pointer=(pointer-1)//2
            return 0
        else :
            raise ValueError


def print_heap(hp) :
        if hp.length==0 :
            return ['_']
        elif hp.length==1 :
            return ['['+str(hp.arr[0])+' '+str(hp.hashtable[hp.arr[0]][0])+']']
        else :
            ans=[]
            ans.append('['+str(hp.arr[0])+' '+str(hp.hashtable[hp.arr[0]][0])+']')
            j=2
            i=1
            while True :
                string=''
                for k in range(j) :
                    if i<hp.length :
                        string+='['+str(hp.arr[i])+' '+str(hp.hashtable[hp.arr[i]][0])+' '+str(hp.arr[(i-1)//2])+']'
                        if k<j-1 :
                            string+=' '
                    else :
                        string+='_'
                        if k<j-1 : 
                            string+=' '
                    i+=1
                ans.append(string)
                j*=2
                if i>=hp.length :
                    break
            return ans








                
hp=heap()
for line in stdin:
    splited=list(line.split())
    length=len(splited)
    if length==3 :
        if splited[0]=='set' :
                if splited[1].lstrip('-').isdigit() :
                    try :
                        a = hp.set(int(splited[1]), splited[2])
                    except ValueError as e:
                        print('error')
                else :
                    print('error')
        elif splited[0]=='add' :
            if splited[1].lstrip('-').isdigit() :
                try :
                    a=hp.add(int(splited[1]), splited[2])
                except ValueError as e:
                    print('error')
            else :
                print('error')
        else :
            print('error')
    elif length==2 :
        if splited[0]=='delete' :
            if splited[1].lstrip('-').isdigit() :
                try :
                    a=hp.delete(int(splited[1]))
                except ValueError as e:
                    print('error')
            else :
                print('error')
        elif splited[0]=='search' :
            if splited[1].lstrip('-').isdigit() :
                try:
                    a, b=hp.search(int(splited[1]))
                    print('1 '+str(a)+' '+str(b))
                except ValueError as e:
                    print('0')
            else :
                print('error')
        else :
            print('error')
    elif length==1 :
        if splited[0]=='min' : 
            try:
                a, b=hp.min()
                print(str(a)+' 0 '+str(b))
            except ValueError as e:
                print('error')
        elif splited[0]=='max' : 
            try :
                a, b, c=hp.max()
                print(str(a)+' '+str(b)+' '+str(c))
            except ValueError as e:
                print('error')
        elif splited[0]=='extract' : 
            try :
                a, b=hp.extract()
                print(str(a)+' '+str(b))
            except ValueError as e:
                print('error')
        elif splited[0]=='print' : 
            a = print_heap(hp)
            for x in a :
                print(x)
        else :
            print('error')
    elif length>3 :
        print('error')
