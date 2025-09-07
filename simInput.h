#include <simClass.h>
#include <bits/stdc++.h>

using namespace std;

vector<Process> readProcessList(string inputFileName){

    vector<Process>processes;

    ifstream file;
    file.open(inputFileName);

    int processId, totalMemory;

    while(file>>processId>>totalMemory){

        Process process;
    
        process.processId = processId;
        process.totalMemory = totalMemory;

        processes.push_back(process);

    }
  
    file.close();

    return processes;

}


queue<ProcessTraceEntry> readProcessTrace(string inputFileName){
  
    queue<ProcessTraceEntry>processTraceList;

    ifstream file;
    file.open(inputFileName);

    int processId, memoryLocation;

    while(file>>processId>>memoryLocation){

        ProcessTraceEntry processTraceEntry;

        processTraceEntry.processId = processId;
        processTraceEntry.memoryLocation = memoryLocation-1;

        processTraceList.push(processTraceEntry);

    }

    file.close();

    return processTraceList;

}