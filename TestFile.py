import math
import time
import numpy as np
from numba import cuda
import numba.cuda.cudadrv.nvvm as nvvm

# Определяем CUDA-ядро для поиска индексов всех массивов
@cuda.jit
def find_indices_kernel(arrays, random_nums, indices):
    idx = cuda.grid(1)

    if idx < arrays.shape[0]:
        array = arrays[idx]
        random_num = random_nums[idx]

        for i in range(array.shape[0]):
            if array[i] <= random_num:
                indices[idx] = i
            else:
                break

def sequential_find_indices(arrays, random_nums):
    indices = np.zeros(arrays.shape[0], dtype=np.int32)

    for idx in range(arrays.shape[0]):
        array = arrays[idx]
        random_num = random_nums[idx]

        for i in range(array.shape[0]):
            if array[i] <= random_num:
                indices[idx] = i
            else:
                break

    return indices

# Указание полного пути к библиотеке NVVM
nvvm_path = "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.4\\nvvm\\bin\\nvvm64_40_0.dll"
# Предположим, что nvvm_path - это путь к библиотеке NVVM
nvvm_instance = nvvm.NVVM(nvvm_path)  # Создание экземпляра NVVM
# Передача экземпляра NVVM в метод data_layout
ir_module.data_layout = nvvm_instance.data_layout()
# Генерируем данные для сравнения
N = 100
num_arrays = 100
max_array_length = 50
arrays = [np.sort(np.random.rand(np.random.randint(1, max_array_length))) for _ in range(num_arrays)]
max_len = max(len(arr) for arr in arrays)
arrays_np = np.array([np.concatenate([arr, np.zeros(max_len - len(arr))]) for arr in arrays])
random_nums = np.random.rand(num_arrays)
random_nums_np = np.array(random_nums)

# Измеряем время выполнения CUDA-ядра
start_time_cuda = time.time()
indices_cuda = np.zeros(num_arrays, dtype=np.int32)
threads_per_block = 256
blocks_per_grid = (num_arrays + (threads_per_block - 1)) // threads_per_block
find_indices_kernel[blocks_per_grid, threads_per_block](arrays_np, random_nums_np, indices_cuda)
cuda_time = time.time() - start_time_cuda

# Измеряем время выполнения последовательного метода на CPU
start_time_cpu = time.time()
indices_cpu = sequential_find_indices(arrays_np, random_nums_np)
cpu_time = time.time() - start_time_cpu

print("Время выполнения CUDA-ядра на GPU: {:.6f} секунд".format(cuda_time))
print("Время выполнения последовательного метода на CPU: {:.6f} секунд".format(cpu_time))



def BenchShafferaFunctionx10(path):
    x1=path[0]*(path[1]+path[2]+path[3]+path[4]+path[5]+path[6])
    x2=path[7]*(path[8]+path[9]+path[10]+path[11]+path[12]+path[13])
    OF=1/2-(math.sin(math.sqrt(x1*x1+x2*x2))*math.sin(math.sqrt(x1*x1+x2*x2))-0.5)/(1+0.001*(x1*x1+x2*x2))
    return OF

def BenchKornFunctionx10(path):
    x1=path[0]*(path[1]+path[2]+path[3]+path[4]+path[5])
    x2=path[6]*(path[7]+path[8]+path[9]+path[10]+path[11])
    z=complex(x1, x2)
    OF=1/(1+abs(pow(z,6)-1))
    return OF

def BenchBirdFunctionx10(path):
    x1=path[0]*(path[1]+path[2]+path[3]+path[4]+path[5])
    x2=path[6]*(path[7]+path[8]+path[9]+path[10]+path[11])
    OF=-math.sin(x1)*math.exp(pow(1-math.cos(x2),2))-math.cos(x2)*math.exp(pow(1-math.sin(x1),2))-pow(x1-x2,2)
    return OF

def BenchEkliFunctionx10(path):
    x1=path[0]*(path[1]+path[2]+path[3]+path[4]+path[5]+path[6])
    x2=path[7]*(path[8]+path[9]+path[10]+path[11]+path[12]+path[13])
    OF=-math.e+20*math.exp(-math.sqrt((pow(x1,2)+pow(x2,2))/50))+math.exp(1/2*(math.cos(2*math.pi*x1)+math.cos(2*math.pi*x2)))
    return OF

path=[]
path.append(1)
path.append(9)
path.append(0)
path.append(0)
path.append(0)
path.append(0)
path.append(0)

path.append(1)
path.append(10)
path.append(0)
path.append(0)
path.append(0)
path.append(0)
path.append(0)
print(BenchEkliFunctionx10(path))

Ro=0.9
Q=1
i=0
while i<1000:
    print(i, pow((1 - Ro) * Q,i))
    i=i+1

