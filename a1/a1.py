# Implementation of stack using linked list
class Stack:
    class Node:
        __slots__ = ['element', 'next']
        def __init__(self, element, next):
            self.element = element
            self.next = next
 
    # Initializing a stack.
    # Use a dummy node, which is
    # easier for handling edge cases.
    def __init__(self):
        self.head = None
        self.size = 0

    # Get the current size of the stack
    def getSize(self):
        return self.size
 
    # Check if the stack is empty
    def isEmpty(self):
        return self.size == 0
  
    # Push a value into the stack.
    def push(self, value):
        self.head = self.Node(value,self.head)
        self.size += 1
 
    # Remove a value from the stack and return.
    def pop(self):
        # return None when stack is empty
        if self.isEmpty():
            return None
        remove = self.head.element
        self.head = self.head.next
        self.size -= 1
        return remove


# from bottom to top

# helper function to perform calculation(increment or decrement whichever required)
def helper(sub):
    x,y,z,d = 0,0,0,0
    closed = False
    # loop is ended if we get either of closing bracket, integer(hints starting of new bracket) or None(stack empty)
    toDo = '' # stores that what operation is needed to be done
    while not closed:
        # next element of stack has been accesed
        nex_t = sub.pop()
        if nex_t==')':
            sub.push(nex_t)
            closed = True
        elif nex_t==None:
            closed = True
        elif nex_t.isdigit():
            sub.push(nex_t)
            closed = True
        else:
            # toDo is concatenated to get required operation, checked and done
            toDo += nex_t
            if toDo == '+X':
                x+=1
                d+=1
                toDo =''
            elif toDo == '+Y':
                y+=1
                d+=1
                toDo =''
            elif toDo == '+Z':
                z+=1
                d+=1
                toDo =''
            elif toDo == '-X':
                x-=1
                d+=1
                toDo =''
            elif toDo == '-Y':
                y-=1
                d+=1
                toDo =''
            elif toDo == '-Z':
                z-=1
                d+=1
                toDo =''
    
    return x,y,z,d


# returning our required output using stack as a parameter

def findPosandDistanceUsingStack(s1):
    # initialializes value of x,y,z,d whose final value will be our output
    x,y,z,d = 0,0,0,0
    m=''                # to store integer value in front of any open bracket
    end = False         # will check whether we have reached end of stack or not
    while not end:
        nex_t = s1.pop() # accessing next element in stack
        
        # if next is none that means we have nothing left in our stack, loop end
        if nex_t==None:
            end =True
            
        # if bracket will be closing then we will end loop with returning value
        # corresponding to that bracket
        elif nex_t ==')':
            s1.push(nex_t)
            end = True
        
        # if next will be any digit then we will be storing that value in m
        elif nex_t.isdigit():
            m+=nex_t
            
        # if bracket is opening then we will call the function on stack again(with element popped upto '(')
        # Recursion
        elif nex_t == '(':
            x1,y1,z1,d1=findPosandDistanceUsingStack(s1)
            ###### I am not handling bracket without any integer preceding(because it has been denied on teams) but that can also be done
            int_m = int(m)
            x,y,z,d = x+int_m*x1,y+int_m*y1,z+int_m*z1,d+int_m*d1
            # new value of position and distance is previous plus integer value of m multiplied with values in bracket
            n=s1.pop()
            
            # if bracket is closed(this is why I have pushed the closing bracket in function) then make value of m empty 
            if n==')':
                m=''
                
            # if bracket isn't closing(may be new one strating), preserve value of m
            else:
                s1.push(n)
                
        # finally if our next value is start of something which need to be evaluated, push it and send it to helper function
        # and add up the final return value in ongoing pos and distance
        else:
            s1.push(nex_t)
            x1,y1,z1,d1 = helper(s1)
            x,y,z,d = x+x1,y+y1,z+z1,d+d1
    return [x,y,z,d]
            
def findPositionandDistance(P):
    s1= Stack()
    # pushed each character of P in a stack in reverse order
    for i in range (len(P)-1,-1,-1):
        s1.push(P[i])
    return findPosandDistanceUsingStack(s1)

#P=input()
#findPositionandDistance(P)
