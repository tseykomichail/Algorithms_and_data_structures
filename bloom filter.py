'''
Фильтр Блума
Реализуйте фильтр Блума, позволяющий дать быстрый, но вероятностный ответ, присутствует ли объект в коллекции.
Реализация самой структуры данных должна быть инкапуслирована, т.е. не зависеть от форматов входных/выходных данных и непосредственно ввода/вывода.
Реализация битового массива также должна быть инкапсулирована. Массив битов должен быть эффективно расположен в памяти.
Параметрами структуры данных являются n - приблизительное количество элементов (целое), P - вероятность ложноположительного ответа.
Размер структуры, m, вычисляется как -n log2 P / ln 2, а количество хэш-функций - как -log2 P. Оба значения округляются до ближайшего целого.
В качестве семейства функций используйте семейство хэш-функций вида
hi(x) = (((i + 1)*x + pi+1) mod M) mod m,
где - x - ключ, i - номер хэш-функции, i∈[0; k-1], pj - j-тое по счету простое число, а M - 31ое число Мерсенна.

Формат входных данных
На стандартном потоке ввода задаётся последовательность команд. Пустые строки игнорируются.
Первая строка содержит команду вида set n P.
Каждая последующая строка содержит ровно одну команду: add K, search K или print, где K - неотрицательное число (64 бита вам хватит), ключ.

Формат результата
Команда set инициализирует структуру и выводит вычисленные параметры в формате "m k".
Команда add добавляет в структуру ключ K.
Команда search выводит либо "1", если элемент возможно присутствует в структуре, либо "0", если он там отсутствует.
Команда print выводит внутреннее состояние струтуры - последовательность из 0 и 1, не разделенную пробелами.
В любой непонятной ситуации результатом работы любой команды будет "error".
Результат работы программы выводится в стандартный поток вывода.
'''

from math import log
from sys import stdin

class BitArray :
    def __init__(self, length) :
        self.bits_arr=0
        self.length=length
    def add_bit(self, bit) :
        num=1 
        num<<=bit
        self.bits_arr|=num
    def check_bit(self, bit) :
        num=self.bits_arr>>bit
        return  num&1
    def print(self) :
        ans=''
        num=self.bits_arr
        for i in range(self.length) :
            ans+=str(num&1)
            num>>=1
        return ans
class BloomFilter :
    def set(self, n, P) :
        if n.isdigit() and P.replace('.', '', 1).isdigit() :
            n=int(n)
            P=float(P)
            if n>=0 and 0<=P<=1 :
                self.m=round(-n*log(P)/log(2)**2)
                self.k=round(-log(P)/log(2))
                if self.m<1 or self.k<1 : 
                    return ['error']
                else :
                    self.bit_arr=BitArray(self.m)
                    self.Mersen=2**31-1
                    self.primes=self._generateprime(self.k)
                    return [self.m, self.k]
            else :
                return ['error']
        else :
            return ['error']
    def _generateprime(self, N):
        primes = [2]  
        num = 3  
        while len(primes) < N :  
            is_prime = True  
            for i in range(len(primes)) :
                if num % primes[i] == 0 :  
                    is_prime = False  
                    break  
            if is_prime:  
                primes.append(num)  
            num += 2  
        return primes
    def add (self, num) :
        if self.m<1 or self.k<1 : 
            return 'error'
        else :
            if num.isdigit() :
                num=int(num)
                if num>=0 :
                    for i in range(self.k) :
                        bit=(((i+1)*num+self.primes[i])%self.Mersen)%self.m
                        self.bit_arr.add_bit(bit)
                    return 1
                else :
                    return 'error'
            else :
                return 'error'
    def search (self, num) :
        if self.m<1 or self.k<1 : 
            return 'error'
        else :
            if num.isdigit() :
                num=int(num)
                if num>=0 :
                    for i in range(self.k) :
                        bit=(((i+1)*num+self.primes[i])%self.Mersen)%self.m
                        if not self.bit_arr.check_bit(bit) :
                            return 0
                    return 1
                else :
                    return 'error'
            else :
                return 'error'
    def print(self) :
        if self.m<1 or self.k<1 : 
            return 'error'
        else :
            return self.bit_arr.print()
        
flag=0
for line in stdin :
    splited=list(line.split())
    if len(splited)>0 :
        if len(line.strip())==len(line.replace("\n", "")) :
            if len(splited)==3 :
                if splited[0]=='set' and not flag:
                    bf=BloomFilter()
                    ans=bf.set(splited[1], splited[2])
                    if len(ans)==1 :
                        print(ans[0])
                    else :
                        flag=1
                        print(str(ans[0])+' '+str(ans[1]))
                else :
                    print('error')
            elif len(splited)==2 :
                if splited[0]=='add' and flag :
                    ans=bf.add(splited[1])
                    if ans!=1 :
                        print(ans)
                elif splited[0]=='search' and flag :
                    ans=bf.search(splited[1])
                    print(ans)
                else :
                    print('error')
            elif len(splited)==1 :
                if splited[0]=='print' and flag:
                    print(bf.print())
                else :
                    print('error')
            else :
                print('error')
        else :
            print('error')
