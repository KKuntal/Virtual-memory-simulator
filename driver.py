import os
import subprocess

# Running GUI 1- MenuGUI
def runGUI1():
    print('\n[INFO] Running GUI 1...')

    process_info = ['python3', 'menuGUI.py']

    process   = subprocess.Popen(process_info, stdout=subprocess.PIPE)
    dataBytes = process.communicate()[0]
    dataStr   = dataBytes.decode('utf-8')
    data = list(dataStr.split(' '))

    if data == ['']:
        print('No input given!')
        exit()

    print('Data received after running GUI 1: ', data)
    return data


# Generating results
def genResults(data):
    print('\n[INFO] Generating results...')

    process_info = ['python3', 'generateResults.py']
    process_info.extend(data)

    process = subprocess.Popen(process_info, stdout=subprocess.PIPE)
    dataBytes = process.communicate()[0]
    dataStr   = dataBytes.decode('utf-8')
    genData = list(dataStr.split(' '))

    print('Data received after generating results: ', genData)
    return genData


# Showing results in GUI 2- ResultsGUI
def runGUI2(data):
    print('\n[INFO] Displaying results...')

    process_info = ['python3', 'resultsGUI.py']
    process_info.extend(data)

    process = subprocess.Popen(process_info, stdout=subprocess.PIPE)
    process.wait()

    print('\n[INFO] Simulation Completed!')    


if __name__ == '__main__':
    data = runGUI1()
    data = genResults(data)
    runGUI2(data)