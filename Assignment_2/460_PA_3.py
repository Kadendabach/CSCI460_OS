#CSCI 460
#Kaden Bach
#Assignment 3


def main():

    q1 = Queue()
    q2 = Queue()
    q3 = Queue()

    stream = input("Enter job stream ('<arrivalTime,JobType>')")
    EditedStream = stream[:-1]
    EditedStream = EditedStream[1:]
    dividedString = EditedStream.split('>,<')

    #queueing individual queues for different priorities
    for i in dividedString:
        print(i)
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
            #taskType 1
            t3 = Task(3, 3, vals[0])
            q3.insert(t3)

    currentTime = 0
    while not (q1.isEmpty() and q2.isEmpty() and q3.isEmpty()):
        #processing task
        if not q1.isEmpty():
            if q1.queue[0].incomeTime <= currentTime:
                q1.process()
                print('processing q1 @ time ', currentTime)
                currentTime += 1
        elif not q2.isEmpty():
            if q2.queue[0].incomeTime <= currentTime:
                q2.process()
                print('processing q2 @ time ', currentTime)
                currentTime += 1
        elif not q3.isEmpty():
            if q3.queue[0].incomeTime <= currentTime:
                q3.process()
                print('processing q3 @ time ', currentTime)
                currentTime += 1
        else:
            print('nothing at ', currentTime)
            currentTime += 1
            






class Queue():
    def __init__(self):
        self.queue = []

    def insert(self, task):
        if not self.queue:
            self.queue.append(task)
        else:
            for node in self.queue:
                if node.incomeTime >= task.incomeTime:
                    self.queue.insert(node, task)
                    
            self.queue.append(task)
                    
    def dequeue(self, task):
        self.queue.remove(task)
        

    def process(self):
        self.queue[0].process()
        if self.queue[0].timeSlice == 0:
            self.dequeue(self.queue[0])
        
    def isEmpty(self):
        if not self.queue:
            return True
        else:
            return False


        
class Task():
    def __init__(self, priority, timeSlice, incomeTime):
        self.priority = priority
        self.timeSlice = int(timeSlice)
        self.incomeTime = int(incomeTime)
        
    def process(self):
        self.timeSlice -= 1

class Buffer():
    def __init__(self):
        self.isAvail = True
        self.state = [0, 0, 0, 0]

    def occupy(self, task):
        if self.isAvail:
            if task == 'T1':
                self.state = [1, 1, 1, 1]
            elif task == 'T2':
                self.state = [2, 2, 2, 2]
            elif task == 'T3':
                self.state = [3, 3, 3, 3]
        else:
            pass
            #put task into blocked state

main()
        
