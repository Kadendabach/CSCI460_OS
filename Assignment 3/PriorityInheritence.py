#CSCI 460
#Kaden Bach
#Assignment 3

#After looking back on the assignment requirements i notice that i dont specifically use variables
#for a semaphore or priority but my code still implements the logic behind them.
#The priority based scheduling is based on an if/else statement where the task with the highest priority
#is checked first. Originally I had the input via cli using an input function; later redacted in
#favor of a set of inputs per assignment requirements.
#The only major problem with this implementation is how I print the output of q2, the end format seems
#to be correct but the actual code seems a little sloppy.

#This specific implementation compared to the PriorityInversion file features a seperation of processing
#queues, and when the PriorityInheretence variable is triggered inside of q1, instead of processing q1,
#it processes q3 assuming q3 is the only other process that the queue can be occupied by.

def main():
    #initializing queues, buffer, and out file
    q1 = Queue()
    q2 = Queue()
    q3 = Queue()
    b = Buffer()

    f = open("out2.txt", "w", encoding='utf-8')

    #processes tasks for each stream of inputs
    for i in range(6):
        print('Input', str(i+1)+':', file=f)
        quequeue(q1, q2, q3, i)
        currentTime = 0
        processTask(q1, q2, q3, b, currentTime, f)
        print(file=f)
        
     

def processTask(q1, q2, q3, b, currentTime, f):
    #processing task
    while not (q1.isEmpty() and q2.isEmpty() and q3.isEmpty()):
        #while there are still tasks in any queue:
        if (not q1.isEmpty()) and (q1.queue[0].incomeTime <= currentTime):
            #if q1 has a process to run
            currentTime, PI = processq1(q1, q2, q3, b, currentTime, f)

            #if the priority inversion variable (PI) is true,
            #process q3 instead without incrementing currentTime
            #I didnt see limitations on whether we can assume its p3 or not so thats what were doing.
            if PI:
                 currentTime = processq3(q1, q2, q3, b, currentTime, f)

        elif not q2.isEmpty() and q2.queue[0].incomeTime <= currentTime:
            currentTime = processq2(q1, q2, q3, b, currentTime, f)

        elif (not q3.isEmpty()) and (q3.queue[0].incomeTime <= currentTime):
            #if q3 has a process to run
            currentTime = processq3(q1, q2, q3, b, currentTime, f)

        else:
            print('Nothing at time', currentTime, file=f)
            currentTime += 1
    
def processq1(q1, q2, q3, b, currentTime, f):
    if b.isAvail or b.state == [1, 1, 1, 1]:
        #if buffer is avail or occupied by t1
        if b.isAvail:
            #occupy buffer if not already
            b.occupy(q1.queue[0])
            #print('q1 has occupied the buffer')
        else:
            pass
            #print('buffer is already occupied by t1')
            

        if len(q2.twoString) != 0:
            #this if statement asks if q1 preempted q2
            print(q2.pts(currentTime), file=f)

        q1.process(currentTime)
        ps = b.process(currentTime)
        if ps is not None:
            print(ps, file=f)
        #print('processed q1 & b @ time ', currentTime)
            
        currentTime += 1
        #pause = input()
        PI = False
        return currentTime, PI
    else:
        #if buffer is not avail, return PI = True
        PI = True
        return currentTime, PI

def processq2(q1, q2, q3, b, currentTime, f):
    #if the queue has at least one task 
    #and that task's income time is at or less than the current time:
    ps = q2.process(currentTime)
    if ps is not None:
        print(ps, file=f)
        #print('processing q2 @ time ', currentTime)
    currentTime += 1
    return currentTime

def processq3(q1, q2, q3, b, currentTime, f):
    if b.isAvail or b.state == [3, 3, 3, 3]:
        #if buffer is available or occupied by t3:
        if b.isAvail:
            #occupy the buffer if not already
            b.occupy(q3.queue[0])
            #print('q3 has occupied the buffer')
        else:
            pass
            #print('buffer is already occupied by t3')
        q3.process(currentTime)
        ps = b.process(currentTime)
        if ps is not None:
            print(ps, file=f)
        #print('processed q3 & b @ time ', currentTime)
        
                
        currentTime += 1
        #pause = input()
        return currentTime



def quequeue(q1, q2, q3, inp):
    #input list
    input1 = '< 1,1 >, < 3,2 >, < 6,3 >'
    input2 = '< 0,2 >, < 3,2 >, < 6,3 >'
    input3 = '< 0,3 >, < 1,1 >, < 2,2 >'
    input4 = '< 0,3 >, < 1,3 >, < 2,2 >, < 3,1 >, < 8,3 >'
    input5 = '< 0,3 >, < 1,1 >, < 2,2 >, < 3,2 >, < 8,3 >'
    input6 = '< 0,2 >, < 1,1 >, < 2,1 >, < 3,1 >, < 4,2 >, < 7,3 >'
    inps = [input1, input2, input3, input4, input5, input6]

    stream = inps[inp]
    
    #cli input for testing
    #stream = input("Enter task stream ('< arrivalTime,JobType >, < arrivalTime,JobType >')")

    #parsing tasks
    EditedStream = stream[:-2]
    EditedStream = EditedStream[2:]
    dividedString = EditedStream.split(' >, < ')

    #queueing individual queues for different priorities
    for i in dividedString:
        #print(i)
        vals = i.split(',')
        if vals[1] == '1':
            #taskType 1
            t1 = Task(1, 3, vals[0])
            q1.insert(t1)
        elif vals[1] == '2':
            #taskType 2
            t2 = Task(2, 10, vals[0])
            q2.insert(t2)
        if vals[1] == '3':
            #taskType 3
            t3 = Task(3, 3, vals[0])
            q3.insert(t3)            


class Queue():
    #queue class to hold tasks
    def __init__(self):
        #inititalizing queue, a 'before process' variaable (bp), and a string variable specifivally for q2 (twoString)
        self.queue = []
        self.bp = True
        self.twoString = ''

    def insert(self, task):
        #a method to insert into the queue
        if not self.queue:
            #if its the first task
            self.queue.append(task)
        else:
            #otherwise compare incomeTime's to sort
            for node in self.queue:
                if node.incomeTime >= task.incomeTime:
                    self.queue.insert(node, task)
                    
            self.queue.append(task)
                    
    def dequeue(self, task, currentTime):
        #method to remove task from queue
        if self.queue[0].priority == 2:
            #this if statement is specifically for q2 string
            ps = f"Time {currentTime}: {self.twoString}"
            self.twoString = ''
            self.queue.remove(task)
            self.bp = True
            return ps
        self.queue.remove(task)
        self.bp = True

    def process(self, currentTime):
        #method to simulate a task processing
        if self.queue[0].priority == 2:
            #for q2 string
            if self.bp == True:
                self.twoString += 'T2⋅'
            self.twoString += 'N'
        
        self.queue[0].process()
        self.bp = False

        if self.queue[0].timeSlice == 0:
            #to dequeue when process is finished (timeSlice = 0)
            if self.queue[0].priority == 2:
                #also for q2 string
                self.twoString += '⋅T2'
            return self.dequeue(self.queue[0], currentTime)
        
    def isEmpty(self):
        if not self.queue:
            return True
        else:
            return False        

    def pts(self, currentTime):
        #this method is for printing q2 string
        if len(self.twoString) != 0:
            ps = f"Time {currentTime}: {self.twoString}"
            self.twoString = ''
            return ps
        self.twoString = ''



class Task():
    #task class to hold info about a class
    def __init__(self, priority, timeSlice, incomeTime):
        self.priority = priority
        self.timeSlice = int(timeSlice)
        self.incomeTime = int(incomeTime)
        
    def process(self):
        #method to deincrement time.Slice
        self.timeSlice -= 1



class Buffer():
    #Buffer Class to hold buffer stuff
    def __init__(self):
        self.isAvail = True #this is the binary semaphore represented with booleans
        self.state = [0, 0, 0, 0]
        self.task = None

    def occupy(self, task):
        #method to occupy the buffer
        if self.isAvail:
            #if buffer is avail, set state based on task priority
            if task.priority == 1:
                self.state = [1, 1, 1, 1]
                self.isAvail = False
            elif task.priority == 3:
                self.state = [3, 3, 3, 3]
                self.isAvail = False
            else:
                print('this should never get here')
                pass

            self.task = task

        elif task.priority == 1 and self.state == [1, 1, 1, 1]:
            #if its already occupied by t1
            pass
        elif task.priority == 3 and self.state == [3, 3, 3, 3]:
            #if its already occupied by t3
            pass
        else:
            #if buffer isnt available it wont be called so this shouldnt ever get here
            pass
    
    def process(self, currentTime):
        #process the buffer based on self.task
        #print('task timeSlice is: ', self.task.timeSlice)
        if self.task.timeSlice == 0:
            #if process is finished we can print
            if self.state[0] == 1:
                #if state is 1, task is t1 so print:
                ps = f"Time {currentTime + 1}: T1⋅{self.state}⋅T1"
                #reset buffer
                self.state = [0, 0, 0, 0]
                self.isAvail = True
                return ps
            else:
                #if else, task is t3 so print:
                ps = f"Time {currentTime + 1}: T3⋅{self.state}⋅T3"
                #reset buffer
                self.state = [0, 0, 0, 0]
                self.isAvail = True
                return ps
            



main()