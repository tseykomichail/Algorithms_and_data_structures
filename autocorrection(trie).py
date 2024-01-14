'''
Автокоррекция
Реализуйте программу, которая предлагает варианты замены слова, в котором допущена одна ошибка.
Для решения этой задачи реализуйте сжатое префиксное дерево.
Регистр букв для программы коррекции не имеет значения (слова в словаре хранятся в нижнем регистре).
Варианты ошибок - как в алгоритме Дамерау-Левенштейна: вставка лишнего символа, удаление символа, замена символа или транспозиция соседних символов.
Реализация алгоритма должна быть инкапсулирована. В комментариях напишите сложность ключевых алгоритмов с пояснением.
Обход детей узла можно и нужно реализовать в среднем за время, линейно зависящее от длины подходящего префикса. Соответственно, проверка наличия слова в префиксном дереве — это в среднем линейная операция, зависящая только от длины слова.

Формат входных данных
Данные подаются на стандартный поток ввода. Пустые строки игнорируются.
Первая строка содержит число N - количество слов в словаре.
Последующие N строк содержат слова из словаря, по одному в строке.
Остальные строки - слова, которые надо проверять.

Формат результата
Каждая строка выхода содержит предложение для исправления слова. Слова обрабатываются в порядке их появления.
Если слово не содержит ошибок, то выводится "%слово% - ok".
Если слово содержит одну ошибку, то выводится "%слово% -> %слово_в_словаре%". Если вариантов несколько, то они сортируются лексикографически и разделяются запятой с пробелом.
Если слово содержит более одной ошибки, то выводится "%слово% -?"
Результат работы программы выводится в стандартный поток вывода.
'''

from sys import stdin
class node :
    def __init__(self) :
        self.flag=0
        self.prefix=''
        self.children={}
class tree :
    def __init__(self) :
        self.top=node()
    def _find_biggest_prefix(self, word1, word2) :
        '''
        # Функция находит наибольший общий префикс двух слов
        # сложность операции О(n), где n - длина наименьшего слова из двух
        '''
        length1=len(word1)
        length2=len(word2)
        for i in range(min(length1, length2)) :
            if word1[i]!=word2[i] :
                return i
        return min(length1, length2)  
    def _add_recursive(self, prefix, curr_node) :
        '''
        # В зависимости от длины наибольшего общего префикса слов prefix и части слова, хранящейся в узле curr_node, 
        # функция либо рекурсивно вызывает саму себя, либо производит ограниченное количество операций и заканчивает работу.
        # Таким образом, сложность функции О(n), где n - длина наибольшего общего префикса
        '''
        big_pref=self._find_biggest_prefix(prefix, curr_node.prefix)
        if big_pref==len(curr_node.prefix) :
            if big_pref==len(prefix) :
                curr_node.flag=1
            else :
                suffix=prefix[big_pref:]
                if suffix[0] in curr_node.children :
                    self._add_recursive(suffix, curr_node.children[suffix[0]])
                else :
                    new_node=node()
                    new_node.flag=1
                    new_node.prefix=suffix
                    curr_node.children[suffix[0]]=new_node
        else :
            suffix=curr_node.prefix[big_pref:]
            new_node=node()
            new_node.prefix=suffix
            new_node.flag=curr_node.flag
            new_node.children=curr_node.children
            curr_node.children={}
            curr_node.children[suffix[0]]=new_node
            if big_pref==len(prefix) :
                curr_node.flag=1
            else :
                curr_node.flag=0
                new_suffix=prefix[big_pref:]
                new_node=node()
                new_node.flag=1
                new_node.prefix=new_suffix
                curr_node.children[new_suffix[0]]=new_node
            curr_node.prefix=curr_node.prefix[:big_pref]
    def add(self, word) :
        '''
        # Функция добавляет слово в префиксное дерево. 
        # Поскольку за счет использования словаря для хранения дочерних узлов нужный узел находится за константу,
        # время работы функции линейно зависит от длины слова, т.е. равна О(n)
        '''
        word=word.lower()
        if word[0] in self.top.children :
            self._add_recursive(word, self.top.children[word[0]])
        else :
            new_node=node()
            new_node.flag=1
            new_node.prefix=word
            self.top.children[word[0]]=new_node
    def _damerau_levenshtein_distance(self, prefix, word_to_check):
        '''
        # Cложность вычисления расстояния - O(n*m), где n - длина слова prefix, а m - длина слова word_to_check
        '''
        len_pref = len(prefix)
        len_word = len(word_to_check)
        start_symbol=len(self.d)
        for i in range(len_pref-start_symbol+1) :
            self.d.append([None for j in range(len_word+1)])
        for i in range(start_symbol, len_pref+1):
            self.d[i][0]=i
            for j in range(1, len_word+1):
                if prefix[i-1] == word_to_check[j-1]:
                    cost = 0
                else:
                    cost = 1
                self.d[i][j] = min(
                               self.d[i-1][j] + 1, 
                               self.d[i][j-1] + 1, 
                               self.d[i-1][j-1] + cost, 
                              )
                if i>1 and j>1 and prefix[i-1] == word_to_check[j-1-1] and prefix[i-1-1] == word_to_check[j-1]:
                    self.d[i][j] = min(self.d[i][j], self.d[i-2][j-2] + 1) 
        return self.d[len_pref][len_word]
    def check(self, word_to_check) :
        '''
        # Оценка сверху сложности равна O(n*(m1+m2+...+mk)), где n - длина word_to_check,
        # а mi - длина i-го слова, хранящегося в префиксном дереве.
        # Если n - количество узлов в префиксном дереве, то сложность равна O(n)
        '''
        word_to_check_original=word_to_check
        word_to_check=word_to_check.lower()
        self.for_print=[]
        self.d=[]
        self.d.append([i for i in range(len(word_to_check)+1)])
        for k, v in self.top.children.items() :
            word_pref=''
            self._check_recursive(word_pref, v, word_to_check)
        if len(self.for_print)>0 :
            self.for_print.sort()
            ans=''
            ans+=word_to_check_original
            ans+=' -> '
            for i in range(len(self.for_print)-1) :
                ans+=self.for_print[i]
                ans+=', '
            ans+=self.for_print[len(self.for_print)-1]
            return ans
        else :
            return word_to_check_original+' -?'
    def _check_recursive(self, word_pref, curr_node, word_to_check) :
        '''
        # Cложность вычисления - O(n*m+k), где n - длина слова, хранящегося в узле curr_node,
        #  m - длина word_to_check, а k - число детей узла curr_node
        '''
        word_pref+=curr_node.prefix
        dist=self._damerau_levenshtein_distance(word_pref, word_to_check) 
        if curr_node.flag==1 :
            if dist==1 :
                self.for_print.append(word_pref)
        for k, v in curr_node.children.items() :
             self._check_recursive(word_pref, v, word_to_check)
        word_pref.removesuffix(curr_node.prefix)
        for i in range(len(curr_node.prefix)) :
            self.d.pop()
    
class dictionary :
    def __init__(self) :
        '''
        # Будем хранить слова в словаре
        '''
        self.correct_words=set()
    def add(self, word) :
        '''
        # Так как в питоне словарь реализован через хеш-таблицу, добавление элемента осуществляется за амортизированную O(1)
        '''
        self.correct_words.add(word.lower())
    def check(self, word) :
        '''
        # Эта операция будет выполняться за О(1), поскольку поиск элемента в хеш-таблице осуществляется за константу
        '''
        if word.lower() in self.correct_words :
            return word+' - ok'
        else :
            return 0

tr=tree()
dic=dictionary()
num_input=int(input())
while num_input :
    line=input()
    if line!='' :
        tr.add(line)
        dic.add(line)
        num_input-=1

for line in stdin:
    new_line=line.rstrip("\n")
    if new_line!='' :
        request=dic.check(new_line)
        if request !=0 :
            print(request)
        else :
            print(tr.check(new_line))
