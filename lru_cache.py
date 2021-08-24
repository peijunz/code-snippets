from dataclasses import dataclass 

@dataclass
class ListNode:
    key: any
    val: any
    prev: 'ListNode'
    next: 'ListNode'

class LinkedList:
    def __init__(self):
        self.head = ListNode(None, None, None, None)
        self.head.prev = self.head.next = self.head # null.next should be the most recent
    
    def insert(self, node):
        next_node = self.head.next
        self.head.next, node.next = node, next_node
        node.prev, next_node.prev = self.head, node
    
    def extract(self, node):
        # print(node.val)
        assert node != self.head
        prev, next = node.prev, node.next
        prev.next, next.prev = next, prev
        node.prev = node.next = None
        return node

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cnt = 0
        self.nodemap = {}
        self.linkedlist = LinkedList()

    def get(self, key: int) -> int:
        if key in self.nodemap:
            node = self.nodemap.get(key)
            self.linkedlist.extract(node)
            self.linkedlist.insert(node)
            return node.val
        else:
            return -1

    def put(self, key: int, value: int) -> None:
        if key in self.nodemap:
            node = self.nodemap.get(key)
            self.linkedlist.extract(node)
            self.linkedlist.insert(node)
            node.val = value
        else:
            if self.cnt == self.capacity:
                lru_node = self.linkedlist.head.prev
                self.linkedlist.extract(lru_node)
                del self.nodemap[lru_node.key]
                self.cnt -= 1
            node = ListNode(key, value, None, None)
            self.nodemap[key] = node
            self.linkedlist.insert(node)
            self.cnt += 1
