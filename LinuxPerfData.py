
# Program to get linux & Windows system performance data
# Only some of the main system performance counters are being collected
# It can be used as a model to collect othe process specific parameters as well

import psutil
import schedule
import time

global statsDict

def collectStats():

    statsDict = {}
    
    statsDict['CPU_Usage_%'] = psutil.cpu_percent()
    statsDict['VirtualMemory_Usage_%'] = psutil.virtual_memory()[2]
    statsDict['SwapMemory_Usage_%'] = psutil.swap_memory()[3]
    statsDict['Battery_Remaining_%'] = psutil.sensors_battery()[0]
    statsDict['Curr_Users_Count'] = len(psutil.users())
    statsDict['Curr_Process_Count'] = len(psutil.pids())
    
    for i in range(len(psutil.disk_partitions())):
        statsDict[psutil.disk_partitions()[i][1]+'_Usage_%'] = psutil.disk_usage(psutil.disk_partitions()[i][1])[3]
        i += 1

    return statsDict

statsDict = collectStats()

def printStats(statsDict):
    for k,v in statsDict.items():
        print(str(time.ctime())+","+k+","+str(v))
        
def job():
    printStats(statsDict)

# Code can be used for schgeduling the job

'''
schedule.every(5).seconds.do(job)
#schedule.every().hour.do(job)
#schedule.every().day.at("10:30").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
'''
