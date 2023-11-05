import platform
import psutil
import pynvml
import sys, os
import csv


def cpuName() : # cpu 장치 이름을 불러오는 함수.
    cpu_name = platform.machine() 
    
    return cpu_name # retrun type ; string

def cpuCurrUse() : # cpu 현재 사용량을 가져오는 함수.
    cpu_use = str(psutil.cpu_percent() + '%')

    return cpu_use # return type ; String 

def gpuName() : # gpu 장치 이름을 가져오는 함수. 
    try:
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        gpu_name = pynvml.nvmlDeviceGetName(handle).decode('utf-8')
        pynvml.nvmlShutdown()
        return gpu_name
    except Exception as e:
        return str(e)

def gpuCurrUse() : # gpu 현재 사용량을 가져오는 함수.
    try:
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        memory_used = memory_info.used / (1024 ** 2)  # 메가바이트 단위로 변환
        pynvml.nvmlShutdown()

        return memory_used
    except Exception as e:
        return str(e)

def ramSize() :
    ram_size = str(round(psutil.virtual_memory().total / (1024.0 **3)))+"(GB)"

    return ram_size # return type ; String 

def ramCurrUse() : # RAM 현재 사용량을 가져오는 함수. 
    pid = os.getpid()
    curr_process = psutil.Process(pid)
    curr_process_ram_use = curr_process.memory_info()[0] / 2**20

    return curr_process_ram_use # return type ; float

pc_cpu_name = 'CPU 명 : ' + cpuName()
pc_cpu_curr_use = 'CPU 현재 사용량 : ' + gpuCurrUse()

pc_gpu_name = 'GPU 명 : ' + gpuName()
pc_gpu_curr_use = 'GPU 현재 사용량 : ' + gpuCurrUse()

pc_ram_size = 'RAM 크기 : ' + ramSize()
pc_ram_curr_use = 'RAM 현재 사용량 : ' + ramCurrUse()

pc_info = [pc_cpu_name, pc_cpu_curr_use, pc_gpu_name, pc_ram_size, pc_ram_curr_use] 

write = csv.write('/home/suya/learning-passage/learning-passage/pc_resource_data.csv').write(pc_info)
