#Simple Paging System

import sys
import math

#currently, jobs are set to suspend if not enough space -> first unfinished job should be removed
#also I think that if a job with more than 1 page tries to fill space with less frames than pages, it will fill what it can and suspend itself without clearing its frames
#but what should happen is that it suspends the longest running process to free up space for the rest of it.
#additionally should update the print function to account for internal fragmentation

def Main():
    inpf, memory_size_in_bytes, page_size_in_bytes, ft, jobs = initialize()

    for job in inpf:
        if job[0] == 'Job_ID':
            #skip first line
            pass
        elif job[0] == 'print':
            print(ft)
            pass
        elif job[0] == 'exit':
            #exit
            pass
        elif int(job[1]) == 0:
            remove_job(job[0], ft, jobs)

        elif int(job[1]) == -1:
            suspend(job[0], ft, jobs)
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
            process_job(job, page_size_in_bytes, ft, jobs)
            pass

def initialize():

    #decided to move this from main for better organization
    memory_size_in_bytes = int(sys.argv[1])
    page_size_in_bytes = int(sys.argv[2])
    filename = sys.argv[3]
    inpf = get_inp(filename)

    ft = FrameTable(memory_size_in_bytes, page_size_in_bytes)
    jobs = {}

    return inpf, memory_size_in_bytes, page_size_in_bytes, ft, jobs

def get_inp(filename):
    
    requests = []
    
    with open(filename) as file:
        for line in file:
            l = line.split()
            requests.append(l)
            
    return requests

def process_job(job, ps, ft, jobs):
    #init vars
    jid = job[0]
    jsize = int(job[1])
    required_pages = math.ceil(jsize / ps)

    #page table for each process
    pt = PageTable()

    # run the following for each page needed
    for page in range(required_pages):
        #create frame for each page
        frame = ft.map_frame(jid, page)
        #if frame is none it means no more free frames and weve run out of memory
        #subsequently, if thats the case, we suspend the process
        if frame is None:
            #print('suspending', jid)
            jobs[jid] = {'state': 's', 'pt': pt, 'size': jsize}
            return
        #otherwise create a page table for each page pointing to the frame
        pt.map_page(page, frame)

    jobs[jid] = {'state': 'a', 'pt': pt, 'size': jsize}

def remove_job(jid, ft, jobs):
    #pull process page table
    pt = jobs[jid]['pt']
    #pull occupied frame from pt
    for page, frame in pt.table.items():
        #clear frame
        ft.remove(frame)
    #delete job log
    del jobs[jid]
    #we dont have to clear the pt of jid becuase it wont have any more refrences

def suspend(jid, ft, jobs):
    #we can assume if ths func is called that the process is active and not already suspended or not there
    pt = jobs[jid]['pt']
    for page, frame in pt.table.items():
        ft.remove(frame)
    jobs[jid]['state'] = 's'

def resume(jid, ps, ft, jobs):
    #we can assume that resume will only be called on process that are already suspended
    #pulling size from list of jobs
    #recreating req pages & pt
    jsize = jobs[jid]['size']
    required_pages = math.ceil(jsize / ps)
    pt = PageTable()

    #same logic as process_job
    for page in range(required_pages):
        frame = ft.map_page(jid, page)
        if frame is None:
            #not enough current memory
            return
        pt.map_page(page, frame)

    #updating jobs
    jobs[jid]['state'] = 'a'
    jobs[jid]['pt'] = pt

class PageTable:
    def __init__(self):
        self.table = {}

    def map_page(self, page, frame):
        self.table[page] = frame


class FrameTable:
    def __init__(self, memory_size_in_bytes, page_size_in_bytes):
        self.frames = (memory_size_in_bytes // page_size_in_bytes) * [None]

    def map_frame(self, id, page):
        #find a free frame and occupy it
        for i, val in enumerate(self.frames):
            if val is None:
                self.frames[i] = (id, page)
                return i #frame number
        return None #no free frames

    def remove(self, id):
        self.frames[id] = None

    def __str__(self):
        result = []
        for i, val in enumerate(self.frames):
            if val is None:
                result.append(f"Frame {i}: free")
            else:
                jid, vpn = val
                result.append(f"Frame {i}: Job {jid}, Page {vpn}")
        return "\n".join(result)



Main()