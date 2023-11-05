import platform
import psutil
import pynvml
import sys, os
import csv
import pandas as pd

def cpuName():
    cpu_name = platform.processor()
    return cpu_name

def cpuCurrUse() : # cpu 현재 사용량을 가져오는 함수.
    cpu_use = str(psutil.cpu_percent()) + "%"

    return cpu_use # return type ; String 

def gpuName() : # gpu 장치 이름을 가져오는 함수. 
    try:
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        gpu_name = pynvml.nvmlDeviceGetName(handle)
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
pc_cpu_curr_use = f"'CPU 현재 사용량 : {cpuCurrUse()}"
print(pc_cpu_name)
print(pc_cpu_curr_use)

pc_gpu_name = 'GPU 명 : ' + gpuName()
pc_gpu_curr_use = f"'GPU 현재 사용량 : {gpuCurrUse()}"
print(pc_gpu_name)
print(pc_gpu_curr_use)

pc_ram_size = 'RAM 크기 : ' + ramSize()
pc_ram_curr_use = f"'RAM 현재 사용량 : {ramCurrUse()}"
print(pc_ram_size)
print(pc_ram_curr_use)


pc_info = ["CPU name", "CPU useing", "GPU name", "GPU useing", "RAM size", "RAM useing"] 

# 데이터와 열 이름 정의
data = [[cpuName(), cpuCurrUse(), gpuName(), gpuCurrUse(), ramSize(), ramCurrUse()]]

# DataFrame 생성 (인덱스 없음)
df = pd.DataFrame(columns=pc_info, data=data)

print(df)

# DataFrame을 JSON 파일로 저장
json_data = df.to_json(orient='records')

# JSON 파일로 저장
with open('data.json', 'w') as json_file:
    json_file.write(json_data)
