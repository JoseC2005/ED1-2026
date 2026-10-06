# models/structures.py

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def remove(self, data):
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev

                self._size -= 1
                return True
            current = current.next
        return False

class PriorityQueue:
    def __init__(self):
        self.head = None
        self._size = 0

    def enqueue(self, data, priority):
        """Añade un elemento según su prioridad (mayor número = mayor prioridad)"""
        new_node = Node({"data": data, "priority": priority})
        if not self.head or priority > self.head.data["priority"]:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next and current.next.data["priority"] >= priority:
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self._size += 1

    def dequeue(self):
        if not self.head:
            return None
        value = self.head.data["data"]
        self.head = self.head.next
        self._size -= 1
        return value
