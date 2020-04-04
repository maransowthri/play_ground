class Node:

def __init__(self, data):

self.data = data

self.left = None

self.right = None

def insert(self, data):

if self.data:

if data > self.data:

if self.right is None:

self.right = Node(data)

else:

self.right.insert(data)

else:

if self.left is None:

self.left = Node(data)

else:

self.left.insert(data)

else:

self.data = data

def find_val(self, val):

if val > self.data:

if self.right is None:

print("Value not found")

else:

self.right.find_val(val)

elif val < self.data:

if self.left is None:

print("Value not found")

else:

self.left.find_val(val)

else:

print("Value found")

def in_order(self, root):

if root:

self.in_order(root.left)

print(root.data)

self.in_order(root.right)

list_in = [3, 2, 5, 7, 9, 6]

root = Node(list_in[0])

for i in range(1, len(list_in)):

root.insert(list_in[i])

root.in_order(root)

root.find_val(10)
