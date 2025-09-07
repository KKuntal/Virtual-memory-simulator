#include <ctime>
#include <simInput.h>
#include <simConstants.h>
#include <bits/stdc++.h>

using namespace std;
using namespace chrono;

int pointer;
int pageSize;
int pageFault;
int pagingType;
int numProcesses;
int replacementType;
int printDetails;
int processTraceListSize;
int counter = 0;
auto start = chrono::high_resolution_clock::now();

vector<Process> processes;
vector<MemoryEntry> memory;
vector<int> pageFaultTracker;
queue<ProcessTraceEntry> processTraceList;

void fifoReplace(){

  int firstComeFrame = 0;
  long long firstComeTime = processes[memory[0].processId].pages[memory[0].pageNumber].addedTime;

  for(int i=pageSize;i<MEMORY_SIZE;i+=pageSize){

      if(processes[memory[i].processId].pages[memory[i].pageNumber].addedTime < firstComeTime){

        firstComeTime = processes[memory[i].processId].pages[memory[i].pageNumber].addedTime;
        firstComeFrame = i/pageSize;

      }
  }

  int processId = memory[firstComeFrame*pageSize].processId;
  int pageNumber = memory[firstComeFrame*pageSize].pageNumber;

  for(int i=0;i<pageSize;i++){

    memory[firstComeFrame*pageSize+i].occupied = 0;
    memory[firstComeFrame*pageSize+i].processId = -1;
    memory[firstComeFrame*pageSize+i].pageNumber = -1;

  }

  processes[processId].pageTable[pageNumber].valid = 0;
  processes[processId].pageTable[pageNumber].frame = -1;
  processes[processId].pages[pageNumber].addedTime = -1;
  processes[processId].pages[pageNumber].lastAccessedTime = -1;

}

void lruReplace(){

  int firstAccessedFrame = 0;
  long long firstAccessedTime = processes[memory[0].processId].pages[memory[0].pageNumber].lastAccessedTime;

  for(int i=pageSize;i<MEMORY_SIZE;i+=pageSize){

      if(processes[memory[i].processId].pages[memory[i].pageNumber].lastAccessedTime < firstAccessedTime){

        firstAccessedTime = processes[memory[i].processId].pages[memory[i].pageNumber].lastAccessedTime;
        firstAccessedFrame = i/pageSize;

      }
  }

  int processId = memory[firstAccessedFrame*pageSize].processId;
  int pageNumber = memory[firstAccessedFrame*pageSize].pageNumber;

  for(int i=0;i<pageSize;i++){

    memory[firstAccessedFrame*pageSize+i].occupied = 0;
    memory[firstAccessedFrame*pageSize+i].processId = -1;
    memory[firstAccessedFrame*pageSize+i].pageNumber = -1;

  }

  processes[processId].pageTable[pageNumber].valid = 0;
  processes[processId].pageTable[pageNumber].frame = -1;
  processes[processId].pages[pageNumber].addedTime = -1;
  processes[processId].pages[pageNumber].lastAccessedTime = -1;

}

void clockReplace(){

    while(memory[pointer*pageSize].usedBit != 0){
        
        for(int i=0; i<pageSize; i++){
          memory[pointer*pageSize + i].usedBit = 0;
        }

        int frame_count = MEMORY_SIZE/pageSize;
        pointer=(pointer+1)%frame_count;
    }
}

void replacement(){
  if (replacementType==FIFO){
    fifoReplace();
  }
  else if(replacementType==LRU){
    lruReplace();
  }
  else if(replacementType == CLOCK){
      clockReplace();
  }
}

bool fifoLoad(int processId, int pageNumber){

  for(int i=0;i<MEMORY_SIZE;i+=pageSize){

    if(!memory[i].occupied){

      processes[processId].pageTable[pageNumber].valid = 1;
      processes[processId].pageTable[pageNumber].frame = i/pageSize;

      auto elapsed = high_resolution_clock::now() - start;

      processes[processId].pages[pageNumber].addedTime = duration_cast<nanoseconds>(elapsed).count();
      processes[processId].pages[pageNumber].lastAccessedTime = duration_cast<nanoseconds>(elapsed).count();

      for(int j=0;j<pageSize;j++){

        memory[i+j].occupied = 1;
        memory[i+j].processId = processId;
        memory[i+j].pageNumber = pageNumber;

      }

      return true;
    }

  }

  return false;

}

bool lruLoad(int processId, int pageNumber){

  for(int i=0;i<MEMORY_SIZE;i+=pageSize){

    if(!memory[i].occupied){

      processes[processId].pageTable[pageNumber].valid = 1;
      processes[processId].pageTable[pageNumber].frame = i/pageSize;

      auto elapsed = high_resolution_clock::now() - start;

      processes[processId].pages[pageNumber].addedTime = duration_cast<nanoseconds>(elapsed).count();
      processes[processId].pages[pageNumber].lastAccessedTime = duration_cast<nanoseconds>(elapsed).count();

      for(int j=0;j<pageSize;j++){

        memory[i+j].occupied = 1;
        memory[i+j].processId = processId;
        memory[i+j].pageNumber = pageNumber;

      }

      return true;
    }

  }

  return false;

}

bool clockLoad(int processId, int pageNumber){

  if(memory[pointer*pageSize].usedBit == 0){
  
    if(memory[pointer*pageSize].occupied){

        int frame_processId = memory[pointer*pageSize].processId;
        int frame_pageNumber = memory[pointer*pageSize].pageNumber;

        for(int i=0;i<pageSize;i++){

        memory[pointer*pageSize+i].occupied = 0;
        memory[pointer*pageSize+i].processId = -1;
        memory[pointer*pageSize+i].pageNumber = -1;

        }
        
        processes[frame_processId].pageTable[frame_pageNumber].valid = 0;
        processes[frame_processId].pageTable[frame_pageNumber].frame = -1;
    }
                
    processes[processId].pageTable[pageNumber].valid = 1;
    processes[processId].pageTable[pageNumber].frame = pointer;
            
    for(int i=0;i<pageSize;i++){

      memory[pointer*pageSize+i].occupied = 1;
      memory[pointer*pageSize+i].processId = processId;
      memory[pointer*pageSize+i].pageNumber = pageNumber;
      memory[pointer*pageSize+i].usedBit = 1;

    }
    
    int frame_count = MEMORY_SIZE/pageSize;
    pointer=(pointer+1)%frame_count;
    
    return true;
  } 
  return false;
}

void load(int processId, int pageNumber){

  bool loaded;

  if(replacementType==FIFO){
    loaded = fifoLoad(processId, pageNumber);
  }
  else if(replacementType==LRU){
    loaded = lruLoad(processId, pageNumber);
  }
  else if(replacementType==CLOCK){
    loaded = clockLoad(processId, pageNumber);
  }

  if(!loaded){

    replacement();
    load(processId, pageNumber);

  }

}

int findNext(int processId,int pageNumber){

  int nextPageNumber=-1;
  int pageCount = ceil(float(processes[processId].totalMemory)/pageSize);

  for(int i=pageNumber+1;i<pageCount;i++){
    
    if(!processes[processId].pageTable[i].valid){
      nextPageNumber=i;
      return nextPageNumber;
    }

  }
  for(int i=0;i<pageNumber;i++){
    
    if(!processes[processId].pageTable[i].valid){
      nextPageNumber=i;
      return nextPageNumber;
    }

  }

  return nextPageNumber;
}

void prePaging(int processId, int pageNumber){

  load(processId,pageNumber);

  int nextPageNumber = findNext(processId,pageNumber);
  if(nextPageNumber!=-1){
    load(processId,nextPageNumber);
  }
}

void demandPaging(int processId, int pageNumber){
  load(processId, pageNumber);
}

void paging(int processId, int pageNumber){
  if(pagingType==PRE){
    prePaging(processId, pageNumber);
  }
  else if(pagingType==DEMAND){
    demandPaging(processId, pageNumber);
  }
}

void check(int processNumber, int pageNumber){
  if(!processes[processNumber].pageTable[pageNumber].valid){
    pageFault++;
    paging(processNumber,pageNumber);
  }
  else{

    auto elapsed = high_resolution_clock::now() - start;
    processes[processNumber].pages[pageNumber].lastAccessedTime = duration_cast<nanoseconds>(elapsed).count();

    int frame = processes[processNumber].pageTable[pageNumber].frame;

    for(int i=0; i<pageSize; i++){
      memory[frame*pageSize + i].usedBit = 1;
    }
  }
}

void printData(){
  cout<<numProcesses<<' '<<processTraceListSize<<' '<<pageFault;

  if(printDetails)
  {
    for(int i=0; i<pageFaultTracker.size(); i++)
    {
      cout<<' '<<pageFaultTracker[i];
    }
  }
}

int main(int argc,char* argv[]){

  string processListFilename  = argv[1];
  string processTraceFilename = argv[2];
  string replacementParam     = argv[3];
  string pagingParam          = argv[4];
  string pageSizeParam        = argv[5];
  string printDetailsParam    = argv[6];

  if(pagingParam=="DEMAND"){
    pagingType=DEMAND;
  }
  else if(pagingParam=="PRE"){
    pagingType=PRE;
  }
  else{
    pagingType=DEMAND;
  }

  if(replacementParam=="FIFO"){
    replacementType=FIFO;
  }
  else if(replacementParam=="LRU"){
    replacementType=LRU;
  }
  else if(replacementParam=="CLOCK"){
     replacementType=CLOCK;
  }
  else{
    replacementType=FIFO;
  }

  if(printDetailsParam=="1"){
    printDetails = 1;
  }
  else{
    printDetails = 0;
  }

  {
    pointer = 0;
    pageFault = 0;
    pageSize = stoi(pageSizeParam);
    processes = readProcessList(processListFilename);
    processTraceList = readProcessTrace(processTraceFilename);
    numProcesses = processes.size();
    processTraceListSize = processTraceList.size();
    memory = vector<MemoryEntry>(MEMORY_SIZE);

    for(int i=0;i<numProcesses;i++){

      int pageCount = ceil(float(processes[i].totalMemory)/pageSize);

      processes[i].pages = vector<Page>(pageCount);

      for(int j=0;j<pageCount;j++){
        processes[i].pages[j].pageNumber = j;
        processes[i].pages[j].processId = i;
      }
      
      processes[i].pageTable = vector<PageTableEntry>(pageCount);
      for(int j=0;j<pageCount;j++){
        processes[i].pageTable[j].pageNumber = j;
      }

    }
  }

  pageFaultTracker.push_back(0);

  while(!processTraceList.empty()){

    ProcessTraceEntry ptrace = processTraceList.front();
    processTraceList.pop();

    int processNumber = ptrace.processId;
    int pageNumber = ptrace.memoryLocation/pageSize;

    check(processNumber, pageNumber);

    counter++;

    if(counter % 1000 == 0)
    {
      pageFaultTracker.push_back(pageFault);
    }

  }

  if(counter % 1000 != 0)
  {
    pageFaultTracker.push_back(pageFault);
  }

  printData();

  return 0;
}
