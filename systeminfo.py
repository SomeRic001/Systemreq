import psutil   
import GPUtil
import platform
import subprocess
try:
    def get_info():
        #CPU info
        frequency = psutil.cpu_freq()
        p_core = psutil.cpu_count(logical = False)
        l_core = psutil.cpu_count(logical = True)
        #GPU info
        gpu_name = GPUtil.getGPUs()[0].name
        vram = GPUtil.getGPUs()[0].memoryTotal
        #OS info
        system = platform.system()
        system_version = platform.version()
        os_details = platform.platform()
        #Driver info
        if system =="Windows":
            driver_version_raw = subprocess.check_output("wmic path win32_videocontroller get driverversion", shell = True).decode('utf-8').strip()
            driver_version = driver_version_raw.split('\n')[1].strip()
        if system =="Linux":
            driver_version_raw = subprocess.check_output("lsmod -v | grep nvidia", shell = True).decode('utf-8').strip()
            driver_version = driver_version_raw.split()[1].strip()
        #RAM info
        ram = psutil.virtual_memory().total
        ram = round(ram / (1024 ** 3), 2)
        #Disk info
        partitions = psutil.disk_partitions()
        maximum_free =0
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            maximum_free = max(maximum_free, usage.free)

        disc = round(maximum_free / (1024 ** 3), 2)
        return frequency, p_core, l_core, ram, disc, gpu_name, vram, os_details, driver_version
    
    def print_info():
        frequency, p_core, l_core, ram, disc, gpu_name, vram, os_details, driver_version = get_info()
        print("System Information:\n")
        print(f"CPU Max Frequency: {frequency.max/1000} GHz")
        print(f"Physical Cores: {p_core}")
        print(f"Logical Cores: {l_core}")
        print(f"RAM: {ram} GB")
        print(f"Free Storage: {disc} GB")
        print(f"GPU: {gpu_name}")
        print(f"VRAM: {round(vram/1024)} GB")
        print(f"OS: {os_details}")
        print(f"Driver Version: {driver_version}")
    def main():
        print_info()
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)

if __name__ == "__main__":
    main()