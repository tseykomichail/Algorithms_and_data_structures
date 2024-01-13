from sys import stdin
import re

'''
Двусторонняя очередь реализована на основе кольцевого буфера.
Поэтому сложность операций добавления и удаления в начале и в конце дэка равна O(1).
'''
class deque() :
    def __init__(self, length) :
        if length<0:
            print('error')
        self.arr=[0]*length
        self.left=None
        self.right=None
        self.max_len=length
    def push_right(self, num) :
        if self.max_len<0 :
            print('error')
        elif self.max_len==0 : 
            print('overflow')
        else :
            if self.right==None :
                self.right=0
                self.left=0
                self.arr[0]=num
            elif self.right-self.left+1==self.max_len :
                print("overflow")
            else :
                self.right+=1
                self.arr[self.right%self.max_len]=num
    def push_left(self, num) :
        if self.max_len<0 :
            print('error')
        elif self.max_len==0 : 
            print('overflow')
        else :
            if self.left==None :
                self.right=0
                self.left=0
                self.arr[0]=num
            elif self.right-self.left+1==self.max_len :
                print("overflow")
            else :
                self.left-=1
                self.arr[self.left%self.max_len]=num
    def pop_right(self) :
        if self.max_len<0 :
            print('error')
        elif self.max_len==0 : 
            print('underflow')
        else :
            if self.left==None :
                print('underflow')
            elif self.right==self.left :
                pointer=self.right
                print (self.arr[pointer%self.max_len])
                self.right=None
                self.left=None
            else :
                self.right-=1
                print(self.arr[(self.right+1)%self.max_len])
    def pop_left(self) :
        if self.max_len<0 :
            print('error')
        elif self.max_len==0 : 
            print('underflow')
        else :
            if self.left==None :
                print('underflow')
            elif self.right==self.left :
                pointer=self.right
                self.right=None
                self.left=None
                print(self.arr[pointer%self.max_len])
            else :
                self.left+=1
                print(self.arr[(self.left-1)%self.max_len])
    def print (self) :
        if self.max_len<0 :
            print('error')
        elif self.max_len==0 : 
            print('empty')
        else :
            if self.right==None : 
                print("empty")
            else :
                a = str()
                for i in range(self.left, self.right+1) :
                    a+=str(self.arr[i%self.max_len]) + ' '
                print(a.strip())
lines = []

for line in stdin:
    lines.append(line)


flag=1
for line in lines:
    num=line.count(' ')
    arr=list(line.split())
    if len(arr)==0 :
        continue
    elif len(arr)>2 :
        print('error')
    elif len(arr)==1 :
        if arr[0]=='popf' and not flag and num==0:
            dq.pop_left()
        elif arr[0]=='popb' and not flag and num==0:
            dq.pop_right()
        elif arr[0]=='print' and not flag and num==0:
            dq.print()
        else :
            print('error')
    elif len(arr)==2 :
        if arr[0]=='set_size' and num==1:
            if flag :
                dq = deque(int(arr[1]))
                flag=0
            else :
                print('error')
        elif arr[0]=='pushf' and not flag and num==1:
            dq.push_left(arr[1])
        elif arr[0]=='pushb' and not flag and num==1:
            dq.push_right(arr[1])
        else :
            print('error')
