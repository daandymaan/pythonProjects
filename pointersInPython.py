#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#
#  Just a class to store the item and the next pointer
#
class Node:
    def __init__(self, item, next):
        self.item = item
        self.next = next

# Note, these are methods "A method is a function that is stored as a class attribute"
class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, item):
        self.head = Node(item, self.head)

    def remove(self):
        if self.is_empty():
            return None
        else:
            item = self.head.item
            self.head = self.head.next    # remove the item by moving the head pointer
            return item

    def is_empty(self):
        return self.head == None
        
    def __str__(self):
        tmp_str = ""
        ptr = self.head
        while ptr != None:
            tmp_str += " " + ptr.item
            ptr = ptr.next
            
        return tmp_str
    def rotate(self):
        #Two new pointers l for last f for front
        lptr = self.head
        fptr = self.head
        #Then using a similar thing to the print yoke go through the linkedlist till you find the last element
        #NOTICE
        #ptr.next and not ptr !=None
        #This is because you dont want a null pointer you want the next attribute to be null
        while lptr.next != None:
            lptr = lptr.next
        #Then you exit out of the while loop
        #Now you set the head to the 
        self.head = fptr.next
        fptr.next = None
        
        lptr.next = fptr
        
        #The you set the head to point the next thing in the list
        
        


# In[ ]:




