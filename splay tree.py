'''
Задача про косое дерево
Реализуйте косое дерево (splay tree).
Реализация самой структуры данных должна быть инкапуслирована, т.е. не зависеть от форматов входных/выходных данных и непосредственно ввода/вывода.
Тесты предполагают "левостороннюю" реализацию, т.е. если действие можно реализовать двумя симметричными способами, надо делать тот, который больше использует левую сторону.

Формат входных данных
На стандартном потоке ввода задаётся последовательность команд. Пустые строки игнорируются.
Каждая строка содержит ровно одну команду: add K V, set K V, delete K, search K, min, max или print, где K - целое число (64 бита вам хватит), ключ, V - произвольная строка без пробелов (значение).

Формат результата
Команда add добавляет значение V в дерево по ключу K, set - изменяет данные по ключу, команда delete удаляет данные.
Команда search выводит либо "1 V", либо "0", где V - значение для найденного ключа.
Команды min и max выводят "K V", где K - минимальный или максимальный ключ дерева соответственно, V - значение по этому ключу.
Команда print выводит все дерево целиком. Она не изменяет дерево.
Дерево выводится строго по уровням, слева направо, 1 строка - 1 уровень. Первая строка содержит только корень дерева в формате "[K V]" или "_", если дерево пустое.
Каждая последующая строка содержит один уровень дерева. Вершины выводятся в формате "[K V P]", где P - ключ родительской вершины. Если вершина отсутствует, ставится "_". Вершины разделены пробелом.
В любой непонятной ситуации результатом работы любой команды будет "error".
Результат работы программы выводится в стандартный поток вывода.
'''
import queue
from sys import stdin

class TreeNode :
    def __init__(self) :
        self.left_child=None
        self.right_child=None
        self.parent=None 
        self.key=None 
        self.value=None 
 
class SplayTree :
    def __init__(self) :
        self.tree=None
    def set(self, key, value) :
        if self.tree!=None :
            curr_node=self.tree
            while True :
                if key<curr_node.key :
                    if curr_node.left_child!=None :
                        curr_node=curr_node.left_child
                    else :
                        self._splay(curr_node)
                        raise ValueError
                elif key>curr_node.key:
                    if curr_node.right_child!=None :
                        curr_node=curr_node.right_child
                    else :
                        self._splay(curr_node)
                        raise ValueError
                else :
                    curr_node.value=value
                    break
            self._splay(curr_node)
            return 1
        else :
            raise ValueError
    def add(self, key, value) :
        if self.tree!=None :
            curr_node=self.tree
            while True :
                if key<curr_node.key :
                    if curr_node.left_child!=None :
                        curr_node=curr_node.left_child
                    else :
                        new_node=TreeNode()
                        new_node.parent=curr_node
                        new_node.key=key
                        new_node.value=value
                        curr_node.left_child=new_node
                        break
                elif key>curr_node.key:
                    if curr_node.right_child!=None :
                        curr_node=curr_node.right_child
                    else :
                        new_node=TreeNode()
                        new_node.parent=curr_node
                        new_node.key=key
                        new_node.value=value
                        curr_node.right_child=new_node
                        break
                else :
                    self._splay(curr_node)
                    raise ValueError
            self._splay(new_node)
        else :
            self.tree=TreeNode()
            self.tree.key=key
            self.tree.value=value
        return 1
    def _zig(self, node) :
        parent=node.parent
        parent.left_child=node.right_child
        if parent.left_child!=None :
            parent.left_child.parent=parent
        node.right_child=parent
        parent.parent=node
        node.parent=None
        return node
    def _zag(self, node) :
        parent=node.parent
        parent.right_child=node.left_child
        if parent.right_child!=None :
            parent.right_child.parent=parent
        node.left_child=parent
        parent.parent=node
        node.parent=None
        return node
    def _zig_zig(self, node) :
        parent=node.parent
        self._zig(parent)
        ans=self._zig(node)
        return ans
    def _zag_zag(self, node) :
        parent=node.parent
        self._zag(parent)
        ans=self._zag(node)
        return ans
    def _zig_zag(self, node) :
        parent=node.parent
        grandparent=parent.parent 
        ans=self._zig(node)
        grandparent.right_child=ans
        ans.parent=grandparent
        answer=self._zag(ans)
        return answer
    def _zag_zig(self, node) :
        parent=node.parent
        grandparent=parent.parent 
        ans=self._zag(node)
        grandparent.left_child=ans
        ans.parent=grandparent
        answer=self._zig(ans)
        return answer
    def _splay(self, node) :
        if node.parent!=None :
            while True :
                parent=node.parent
                grandparent=parent.parent 
                if grandparent!=None :
                    flag=0
                    if grandparent.parent!=None :
                        root=grandparent.parent
                        if root.left_child==grandparent :
                            flag=1
                        else :
                            flag=2
                    if node==parent.left_child :
                        if parent==grandparent.left_child :
                            node=self._zig_zig(node)
                        else :
                            node=self._zig_zag(node)
                    else :
                        if parent==grandparent.left_child :
                            node=self._zag_zig(node)
                        else :
                            node=self._zag_zag(node)
                    if flag==0 :
                        self.tree=node
                        break
                    else :
                        if flag==1 :
                            root.left_child=node
                            node.parent=root
                        else :
                            root.right_child=node
                            node.parent=root
                else :
                    if parent.left_child==node :
                        node=self._zig(node)
                        self.tree=node
                        break
                    else :
                        node=self._zag(node)
                        self.tree=node
                        break
        else :
            self.tree=node
    def min(self) :
        if self.tree==None :
            raise ValueError
        else :
            node=self.tree 
            while node.left_child!=None :
                node=node.left_child
            self._splay(node)
            return node.key, node.value
    def max(self) :
        if self.tree==None :
            raise ValueError
        else :
            node=self.tree 
            while node.right_child!=None :
                node=node.right_child
            self._splay(node)
            return node.key, node.value
    def search(self, key) :
        if self.tree!=None :
            curr_node=self.tree
            while True :
                if key<curr_node.key :
                    if curr_node.left_child!=None :
                        curr_node=curr_node.left_child
                    else :
                        self._splay(curr_node)
                        raise ValueError
                elif key>curr_node.key:
                    if curr_node.right_child!=None :
                        curr_node=curr_node.right_child
                    else :
                        self._splay(curr_node)
                        raise ValueError
                else :
                    to_return=curr_node.value
                    break
            self._splay(curr_node)
            return to_return
        else :
            raise ValueError
    def delete(self, key) :
        if self.tree!=None :
            curr_node=self.tree
            while True :
                if key<curr_node.key :
                    if curr_node.left_child!=None :
                        curr_node=curr_node.left_child
                    else :
                        self._splay(curr_node)
                        raise ValueError
                elif key>curr_node.key:
                    if curr_node.right_child!=None :
                        curr_node=curr_node.right_child
                    else :
                        self._splay(curr_node)
                        raise ValueError
                else :
                    break
            self._splay(curr_node)
            tree1=self.tree.left_child
            tree2=self.tree.right_child
            if tree1!=None and tree2!=None :
                tree1.parent=None
                tree2.parent=None
                node=tree1 
                while node.right_child!=None :
                    node=node.right_child
                self._splay(node)
                self.tree.right_child=tree2
                tree2.parent=self.tree
            elif tree1!=None :
                tree1.parent=None
                self.tree=tree1
            elif tree2!=None :
                tree2.parent=None
                self.tree=tree2
            else :
                self.tree=None
            return 1
        else :
            raise ValueError
        
        
        
def print_recursive(node, position_node, current_level, ans):
    if current_level == len(ans):
        ans.append(["_"] * (2 ** current_level))
    node_str = f"[{node.key} {node.value}"
    if node.parent is not None:
        node_str += f" {node.parent.key}]"
    else:
        node_str += "]"
    ans[current_level][position_node] = node_str
    if node.left_child is not None:
        print_recursive(node.left_child, 2 * position_node, current_level + 1, ans)
    if node.right_child is not None:
        print_recursive(node.right_child, 2 * position_node +1, current_level + 1, ans)
def print_(tr):
    ans = []
    if tr.tree is None:
        raise ValueError
    print_recursive(tr.tree, 0, 0, ans)
    result = ""
    for level in ans:
        result += ' '.join(level) + "\n"
    return result     
        
          
        
tree=SplayTree()
for line in stdin :
    splited=line.split()
    if len(splited)==3 :
        if splited[0]=='add' :
            try :
                tree.add(int(splited[1]), splited[2])
            except ValueError as e :
                print('error')
        elif splited[0]=='set' :
            try :
                ans=tree.set(int(splited[1]), splited[2])
            except ValueError as e:
                print('error')
        else :
            if splited[0]!='delete' and splited[0]!='search' and splited[0]!='min' and splited[0]!='max' and splited[0]!='print' :
                print('error')
    elif len(splited)==2 :
        if splited[0]=='delete' :
            try :
                tree.delete(int(splited[1]))
            except ValueError as e:
                print('error')
        elif splited[0]=='search' :
            try :
                a=tree.search(int(splited[1]))
                print('1 '+str(a))
            except ValueError as e :
                print('0')
        else :
            if splited[0]=='min' or splited[0]=='max' or splited[0]=='print'  :
                continue
            elif splited[0]=='add'  or splited[0]=='set' :
                num=line.count(' ')
                if num>1 :
                    if splited[0]=='add' :
                        try :
                            ans=tree.add(int(splited[1]), ''+" "*(num-2))
                        except ValueError as e:
                            print('error')
                    elif splited[0]=='set' :
                        try :
                            ans=tree.set(int(splited[1]), ''+" "*(num-2))
                        except ValueError as e:
                            print('error')
                else :
                    print('error')
            else :
                print('error')
    elif len(splited)==1 :
        if splited[0]=='min' :
            try :
                a, b=tree.min()
                print(str(a)+' '+str(b))
            except ValueError as e:
                print('error')
        elif splited[0]=='max' :
            try :
                a, b=tree.max()
                print(str(a)+' '+str(b))
            except ValueError as e:
                print('error')
        elif splited[0]=='print' :
            try :
                print(print_(tree), end='')
            except ValueError as e:
                print("_")
        else :
            print('error')
            #if splited[0]!='delete' and splited[0]!='search'  and splited[0]!='add'  and splited[0]!='set' :
                
    else :
        print('error')
