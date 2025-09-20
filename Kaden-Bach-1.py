#Simple Paging System

import sys
import math
#https://www.geeksforgeeks.org/python/deque-in-python/
#got this deque module from geeksforgeeks, didnt see any limitation on weather we can use queue modules
from collections import deque

#currently, jobs are set to suspend if not enough space -> first unfinished job should be removed
#also I think that if a job with more than 1 page tries to fill space with less frames than pages, it will fill what it can and suspend itself without clearing its frames
#but what should happen is that it suspends the longest running process to free up space for the rest of it.
#additionally should update the print function to account for internal fragmentation
#finnally 

def Main():
    inpf, memory_size_in_bytes, page_size_in_bytes, ft, jobs, fifo = initialize()

    for job in inpf:
        if job[0] == 'Job_ID':
            #skip first line
            pass
        elif job[0] == 'print':
            print(ft)
            print_jobs(jobs)
            
        elif job[0] == 'exit':
            #exit
            break
        elif int(job[1]) == 0:
            remove_job(job[0], ft, jobs, fifo)

        elif int(job[1]) == -1:
            suspend(job[0], ft, jobs, fifo)
            #move job to secondary memory
            pass
        elif int(job[1]) == -2:
            resume(job[0], page_size_in_bytes, ft, jobs, fifo)
            #resume suspended job[0]
            #move back to main memory
            #suspend different job if not enough space
        else:
            #process job[0]
            #if job[0] already exists then reject this job req
            process_job(job, page_size_in_bytes, ft, jobs, fifo)
            pass

def initialize():

    #decided to move this from main for better organization
    memory_size_in_bytes = int(sys.argv[1])
    page_size_in_bytes = int(sys.argv[2])
    filename = sys.argv[3]
    inpf = get_inp(filename)

    ft = FrameTable(memory_size_in_bytes, page_size_in_bytes)
    jobs = {}
    fifo = deque()

    return inpf, memory_size_in_bytes, page_size_in_bytes, ft, jobs, fifo

def get_inp(filename):
    
    requests = []
    
    with open(filename) as file:
        for line in file:
            l = line.split()
            requests.append(l)
            
    return requests

def process_job(job, ps, ft, jobs, fifo):
    #init vars
    jid = job[0]
    jsize = int(job[1])
    required_pages = math.ceil(jsize / ps)

    #rejecting duplicate jobs
    if jid in jobs:
        print("rejected", jid, ", it already exists")
        return

    #rejecting if job is too big for memory
    if required_pages > len(ft.frames):
        print("rejected", jid, ", its too big for memory")
        return
    
    #page table for each process
    pt = PageTable()
    allocated = []

    # run the following for each page needed
    for page in range(required_pages):
        #create frame for each page
        #free up frames if needed (suspend oldest)
        suspend_oldest(required_pages - page, ft, jobs, fifo, exclude=jid)
        #if frame is none it means no more free frames and weve run out of memory
        #subsequently, if thats the case, we suspend the process
        frame = ft.map_frame(jid, page)
        if frame is None:
            for f in allocated:
                ft.remove(f)
            #updating jobs
            jobs[jid] = {'state': 's', 'pt': pt, 'size': jsize,'frag': (required_pages * ps) - jsize}
            return
        #otherwise create a page table for each page pointing to the frame
        pt.map_page(page, frame)
        allocated.append(frame)

    jobs[jid] = {'state': 'a', 'pt': pt, 'size': jsize,'frag': (required_pages * ps) - jsize}
    fifo.append(jid)

def remove_job(jid, ft, jobs, fifo):
    #pull process page table
    pt = jobs[jid]['pt']
    #pull occupied frame from pt
    for page, frame in pt.table.items():
        #clear frame
        ft.remove(frame)
    #updating queue
    if jid in fifo:
        fifo.remove(jid)
    #delete job log
    del jobs[jid]
    #we dont have to clear the pt of jid becuase it wont have any more refrences.
    #but a full stack implementation would include freeing that memory space

def suspend(jid, ft, jobs, fifo):
    
    pt = jobs[jid]['pt']
    for page, frame in pt.table.items():
        if frame is not None:
            ft.remove(frame)
            pt.table[page] = None
    #changing state of jid in jobs
    jobs[jid]['state'] = 's'
    if jid in fifo:
        fifo.remove(jid)

def resume(jid, ps, ft, jobs, fifo):
    #we can assume that resume will only be called on process that are already suspended
    #pulling size from list of jobs
    #recreating req pages & pt
    jsize = jobs[jid]['size']
    required_pages = math.ceil(jsize / ps)
    pt = PageTable()

    suspend_oldest(required_pages, ft, jobs, fifo, exclude=jid)
    allocated = [] 

    #same logic as process_job
    for page in range(required_pages):
        frame = ft.map_frame(jid, page)
        if frame is None:
            #not enough current memory
            for f in allocated:
                ft.remove(f)
            return
        pt.map_page(page, frame)

    #updating jobs
    frag = jobs[jid].get('frag', (required_pages * ps) - jsize)
    jobs[jid]['state'] = 'a'
    jobs[jid]['pt'] = pt
    jobs[jid]['frag'] = frag
    fifo.append(jid)

def suspend_oldest(required_pages, ft, jobs, fifo, exclude=None):
    while ft.frames.count(None) < required_pages and fifo:
        #using deque to remove oldest
        oldest = fifo.popleft()
        if oldest == exclude:
            fifo.append(oldest)  #this jid is the process were adding so we dont want to remove it
            continue
        suspend(oldest, ft, jobs, fifo)

def print_jobs(jobs):
    #formatting to look good
    for jid, info in jobs.items():
        state = info['state']
        frag = info.get('frag', 0)
        print(f"Job {jid}: state={state}, size={info['size']} bytes, frag={frag} bytes")
        for page, frame in info['pt'].table.items():
            if frame is None:
                print(f"  Page {page} -> SWAPPED")
            else:
                print(f"  Page {page} -> Frame {frame}")

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