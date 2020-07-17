import numpy as np
from graphviz import Digraph
import random as rand
# NOTE: DELETEについては後で実装できたらな
class Node:
    def __init__(self,key):
        self.key=key
        self.parent=None
        self.size=1
        self.left=None
        self.right=None
        self.color=None

    def __iter__(self):
        if self.left:
            yield from self.left
        yield self
        if self.right:
            yield from self.right

class Tree:
    def __init__(self,nodes):
        self.root=None
        self.nil=Node(None)
        self.nil.left=self.nil
        self.nil.right=self.nil
        self.nil.parent=self.nil
        self.color='b'
        self.size=0
        for node in nodes:
            #print(node.key)
            self.insert(node)
    def __iter__(self):
        if self.root:
            yield from self.root

    def insert(self,node):
        if self.root is None:
            node.color= 'b'
            self.root=node
        else:
            y=None
            x=self.root

            while not(x is None):
                x.size=x.size+1

                y=x
                if node.key<x.key:
                    x=x.left
                else:
                    x=x.right

            node.parent=y
            if node.key<y.key:
                y.left=node
            else:
                y.right=node
            node.left=None
            node.right=None
            node.color='r'
            self.insert_fix_up(node)
            #print(self.root.color)
    def insert_fix_up(self,node):
        while node.parent.color=='r':
            if node.parent is node.parent.parent.left:
                y=node.parent.parent.right
                if (not(y is None)) :
                    if y.color=='r':
                        node.parent.color='b'
                        y.color='b'
                        node.parent.parent.color='r'
                        node=node.parent.parent
                    else:
                        if node is node.parent.right:
                            node=node.parent
                            self.left_rotate(node)
                        node.parent.color='b'
                        node.parent.parent.color='r'
                        self.right_rotate(node.parent.parent)
                else:
                    if node is node.parent.right:
                        node=node.parent
                        self.left_rotate(node)
                    node.parent.color='b'
                    node.parent.parent.color='r'
                    self.right_rotate(node.parent.parent)
            else:
                y=node.parent.parent.left
                if not(y is None):
                    if y.color=='r':
                        node.parent.color='b'
                        y.color='b'
                        node.parent.parent.color='r'
                        node=node.parent.parent
                    else:
                        if node is node.parent.left:
                            node=node.parent
                            self.right_rotate(node)
                        node.parent.color='b'
                        node.parent.parent.color='r'
                        self.left_rotate(node.parent.parent)
                else:
                    if node is node.parent.left:
                        node=node.parent
                        self.right_rotate(node)
                    node.parent.color='b'
                    node.parent.parent.color='r'
                    self.left_rotate(node.parent.parent)
            if node.parent is None:
                break

        self.root.color='b'
    def left_rotate(self,x):
        y=x.right
        x.right=y.left
        if not(y.left is None):
            y.left.parent=x
        y.parent=x.parent
        if x.parent is None:
            self.root=y
        elif x is x.parent.left:
            x.parent.left=y
        else:
            x.parent.right=y
        y.left=x
        x.parent =y
        y.size=x.size
        leftsize=0
        rightsize=0
        if not(x.left is None):
            leftsize=x.left.size
        if not(x.right is None):
            rightsize=x.right.size
        x.size=leftsize+rightsize+1


## NOTE: ここでミスっているかもしれない
    def right_rotate(self,x):
        y=x.left
        x.left=y.right
        if not(y.right is None):
            y.right.parent=x
        y.parent=x.parent
        if x.parent is None:
            self.root=y
        elif x is x.parent.right:
            x.parent.right=y
        else:
            x.parent.left=y
        y.right=x
        x.parent =y
        y.size=x.size
        leftsize=0
        rightsize=0
        if not(x.left is None):
            leftsize=x.left.size
        if not(x.right is None):
            rightsize=x.right.size
        x.size=leftsize+rightsize+1
    def view_graph(self,NAME):
        graph = Digraph(format="png")
        for node in self:
            name = f"{node.key} of {node.size}"
            if node.color=='r':
                graph.node(name, str(node.key)+"/"+str(node.size),color="red",style="filled")
            elif node.color=='y':
                graph.node(name, str(node.key)+"/"+str(node.size),color="green",style="filled")
            else:
                graph.node(name, str(node.key)+"/"+str(node.size),color="black")
            if node.left:
                child = f"{node.left.key} of {node.left.size}"
                graph.edge(name, child,label='L')
            if node.right:
                child = f"{node.right.key} of {node.right.size}"
                graph.edge(name, child,label='R')
        graph.view(NAME)
    def OS_RANK(self,x):
        leftsize=0
        if not(x.left is None):
            leftsize=x.left.size
        r=leftsize+1
        y=x
        while not(y is self.root):
            if y is y.parent.right:
                leftsize=0
                if not(y.parent.left is None):
                    leftsize=y.parent.left.size
                r=r+leftsize+1
            y=y.parent
        return r
# NOTE:

    def OS_SELECT(self,x,i,name):
        leftsize=0
        if not(x.left is None):
            leftsize=x.left.size
        r=leftsize+1

        if i==r:
            color=x.color
            x.color='y'
            self.view_graph(name)
            x.color=color
            return x
        elif i<r:
            return self.OS_SELECT(x.left,i,name)
        else:
            return self.OS_SELECT(x.right,i-r,name)

A=np.arange(1,20)
rand.shuffle(A)
print(A)
nodes=[]
for a in A:
    nodes=nodes+[Node(a)]
T=Tree(nodes)

#グラフの様子が見れる
T.view_graph("view")
i=rand.choice(A)
# n番目の順序統計量を緑色のノードにして返す
T.OS_SELECT(T.root,i,str(i)+"th order")
x=rand.choice(nodes)
i=T.OS_RANK(x)
print(x.key)
print(i)
