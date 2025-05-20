import psutil   
import GPUtil
import platform
import subprocess
import logging
import pandas as pd


logging.basicConfig(
    filename=r'C:\Users\LENOVO\OneDrive\Documents\Info\error.log',
    level=logging.ERROR,
    format='%(asctime)s-%(levelname)s-%(message)s',
    filemode='a'
)
def get_info():
    #CPU info
    frequency = psutil.cpu_freq()
    p_core = psutil.cpu_count(logical = False)
    l_core = psutil.cpu_count(logical = True)
    #GPU info
    gpu_name = GPUtil.getGPUs()[0].name
    gpu_name = gpu_name.strip()
    gpu_brand = gpu_name.split(' ')[0]
    parts = gpu_name.split()
    if parts[0].lower() in ['nvidia','amd','intel']:
        parts = parts[1:]
    parts = parts[:-1]
    gpu_name = ' '.join(parts)
    vram = GPUtil.getGPUs()[0].memoryTotal
    #OS info
    system = platform.system()
    system_version = platform.version()
    os_details = platform.platform().split('-')[0] + " "+ platform.platform().split('-')[1]
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
    return frequency, p_core, l_core, ram, disc,gpu_brand, gpu_name, vram, os_details, driver_version
    
def print_info():
    try:
        frequency, p_core, l_core, ram, disc,gpu_brand, gpu_name, vram, os_details, driver_version = get_info()
    except Exception as e:
        logging.error(f"Error while extracting system information: {e}")
        return    
    print(
        "Your System Information:\n"
        f"CPU Max Frequency: {frequency.max / 1000} GHz\n"
        f"Physical Cores: {p_core}\n"
        f"Logical Cores: {l_core}\n"
        f"RAM: {ram} GB\n"
        f"Free Storage: {disc} GB\n"
        f"GPU: {gpu_brand} {gpu_name}\n"
        f"VRAM: {round(vram / 1024)} GB\n"
        f"OS: {os_details}\n"
        f"Driver Version: {driver_version}"
    )
def main():
    try:
        print_info()
    except Exception as e:
        logging.error(f"Error: {e}")
    in_game = input("Do you want to check the game requirements? (y/n): ")
    if in_game.lower() == 'y':
        game_name = input("Enter the game name: ")
        try:
            requirements(game_name)  
        except FileNotFoundError:
            logging.error("The CSV file was not found. Please check the file path.") 
        except Exception as e:
            logging.error(f"An error occurred: {e}")
    else:
        print("Exiting the program.")
    
def requirements(game_name):
    Run = True
    reqram = 0
    try:
        frequency, p_core, l_core, ram, disc,gpu_brand, gpu_name, vram, os_details, driver_version = get_info()
    except Exception as e:
        logging.error(f"Error while extracting system information: {e}")
        return
    g_n = game_name.lower()
    # Read the CSV file
    df = pd.read_csv(r"C:\Users\LENOVO\OneDrive\Documents\Info\game1.csv")
    matches = df[df['name'].str.lower().str.contains(g_n,na = False)]
    if matches.empty:
        print("No matching games found.")
        return
    print(f"Search results for {game_name}: \n")
    n = 0
    for match in matches['name'].to_list():
        n+=1
        print(f"{n}. {match} \n")
    selected_game = input("Select the game number:😭 ") 
    selected = int(selected_game) - 1
    if not selected_game.isdigit() or int(selected_game) < 1 or int(selected_game) > len(matches):
        print("Invalid selection. Please enter a valid game number.")
        return
    print (f"Selected game: {matches['name'].to_list()[selected]}")
    requirements = {"CPU":matches['CPU:'].to_list()[selected],
                    "RAM":matches['Memory:'].to_list()[selected],
                    "Disc":matches['File Size:'].to_list()[selected],
                    "GPU":matches['Graphics Card:'].to_list()[selected],
                    "OS":matches['OS:'].to_list()[selected]
                    }
    if "MB" in requirements["RAM"]:                
        reqram = int(requirements["RAM"].strip("MB"))
        reqram= reqram/1024
    elif "GB" in requirements["RAM"]:
        reqram = int(requirements["RAM"].strip("GB"))
    print("\nGame Requirements:")
    print(
        f"CPU: {requirements["CPU"]}or higher\n"
        f"RAM: {requirements["RAM"]}\n"
        f"Storage: {requirements["Disc"]}\n"
        f"GPU: {requirements["GPU"]} or higher\n"
        f"Operating System: {requirements["OS"]}"
        )

    
    again = input("Do you want to check another game? (y/n): ")
    if again.lower() == 'y':
        game_name = input("Enter the game name: ")
        requirements(game_name)
    else:
        print("Exiting the program.")
    


if __name__ == "__main__":
    main()