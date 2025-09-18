#Simple Paging System

import sys
import math

def Main():
    memory_size_in_bytes = int(sys.argv[1])
    page_size_in_bytes = int(sys.argv[2])
    filename = sys.argv[3] 

    frames = memory_size_in_bytes//page_size_in_bytes
    print('frame # =:', frames)
    
    inp = Get_inp(filename)
    #print(inp)
    #print()
    fm = FrameManager(memory_size_in_bytes, page_size_in_bytes, frames)

    for job in inp:
        if job[0] == 'Job_ID':
            #skip first line
            pass
        elif job[0] == 'print':
            #print progress
            pass
        elif job[0] == 'exit':
            #exit
            pass
        elif int(job[1]) == 0:
            #remove job[0]
            pass
        elif int(job[1]) == -1:
            #suspend job[0]
            #move job to secondary memory
            pass
        elif int(job[1]) == -2:
            #resume suspended job[0]
            #move back to main memory
            #suspend different job if not enough space
            pass
        else:
            #process job[0]
            #if job[0] already exists then reject this job req
            process_job(job, memory_size_in_bytes, page_size_in_bytes, frames, fm)
            pass

def Get_inp(filename):
    
    requests = []
    
    with open(filename) as file:
        for line in file:
            l = line.split()
            requests.append(l)
            
    return requests

def process_job(job, ms, ps, f, fm):
    num_of_pages = math.ceil(int(job[1]) / ps)
    if (fm.check_free_frames() >= num_of_pages):
        for page in num_of_pages:
            fm.add_page_to_frame(page)
        else:
            #remove oldest process
            pass
    #check if job already in memory, if not:
    #check if free frame, add to main memory
    #if not, suspend oldest process & add newest to main memory
    #update page table
    pass

class FrameManager:
    def __init__(self, ms, ps, f):
        self.framenum = f
        for frame in range(f):
            self.freeframes += '0'
        

    def check_free_frames(self):
        for i in self.freeframes:
            if self.freeframes[i] == '0':
                placeholder += 1
        free_frames = placeholder
        placeholder = 0
        return free_frames
    
    def add_page_to_frame(self, page):
        for i in self.freeframes:
            if self.freeframes[i] == '0':
                self.freeframes[i] == '1'
                return i #page number
            else:
                print("error, tried to add page to frame when there wasnt any free frames")
    




Main()