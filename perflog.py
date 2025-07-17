import logging
import psutil
import time
import os
from pythonjsonlogger import jsonlogger
from pynvml import *

try:
    _NVML_AVAILABLE = True
except ImportError:
    _NVML_AVAILABLE = False

class Perflog:
    def __init__(self):
        """
        Args:
            log_file_path: Incase the user does not want the CWD to create a folder called 'logs' and start writing to a file in that folder called 'log.txt'
        Initialized Vars:
            self.__handel: The universal handel for NVML to access the GPU at index 0 for single GPU systems
            self.__isnvidia: Checks the precense of NVIDIA GPU using the self.__check_nvidia() function
            self.__total_runtime:
            self.__last_lap_time: 
            self.__current_process:

        """
        # Setup the file and logging variable
        self.__steup_logger__()

        # Checking for a NVIDIA GPU
        self.__isnvidia = self.__check_nvidia__()

        # Setting up universal NVML handel if a NVIDIA GPU is detected
        if self.__isnvidia:
            nvmlInit()
            self.__handle = nvmlDeviceGetHandleByIndex(0)

        # Intializing variabls
        self.__total_runtime = 0
        self.__last_lap_time = 0

        # First initialization
        self.get_lap()

        # Creating an object for the current process
        self.__current_process = psutil.Process(os.getpid())

    def __steup_logger__(self):
        """
        Args:
            log_file_path: Incase the user does not want the CWD to create a folder called 'logs' and start writing to a file in that folder called 'log.txt'
        Initialized Vars:
            self.__logger: 
        """
        self.__logger = logging.getLogger("PerfLog")
        self.__logger.setLevel(logging.DEBUG)
        cwd = os.path.abspath(os.getcwd())
        log_dir_path = cwd + "/logs"
        log_file_path = log_dir_path + "/perflog.txt"
        if not os.path.isdir(log_dir_path):
                os.mkdir(log_dir_path)

        handler = logging.FileHandler(log_file_path)
        formatter = jsonlogger.JsonFormatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)

    def log(self, log_message):
        if self.__isnvidia:
            self.__logger.debug(log_message,
                extra={
                    'runtime' : self.__total_runtime,
                    'lap' : self.get_lap(),
                    'cpu_utilization' : self.get_cpu_util(),
                    'cpu_clockspeed' : self.get_cpu_clock(),
                    'ram' : self.get_ram_usage(),
                    'process ram' : self.get_process_ram_usage(),
                    'gpu_utilization' : self.get_gpu_util(),
                    'gpu_clockspeed' : self.get_gpu_clock(),
                    'vram' : self.get_vram_usage(),
                    'process_vram' : self.get_process_vram_usage()
                    })
        else:
            self.__logger.debug(log_message,
                extra={
                    'runtime' : self.__total_runtime,
                    'lap' : self.get_lap(),
                    'cpu_utilization' : self.get_cpu_util(),
                    'cpu_clockspeed' : self.get_cpu_clock(),
                    'ram' : self.get_ram_usage(),
                    'process_cpu_utilization' : self.get_process_cpu_util(),
                    'process_ram' : self.get_process_ram_usage()
                    })

    def get_lap(self):
        """
        Returns the time elapsed since the last call to this method (in seconds).
        If it's the first call after initialization, it returns time since instance creation.
        Returns None if an error occurs.
        """
        try:
            current_time = time.perf_counter()
            # Calculate the duration of this 'lap'
            lap_duration = current_time - self.__last_lap_time
            # Update the baseline for the next 'lap'
            self.__last_lap_time = current_time
            self.__total_runtime += lap_duration
            return lap_duration
        except Exception as e:
            self.__logger.error(f"Error getting lap time: {e}", exc_info=True)
            return None

    def get_cpu_util(self):
        """
        Returns the current system-wide CPU utilization as a percentage.
        This function does not have an interval to interrupt process
        """
        try:
            # interval is the amount of seconds the system will pause to calculate the CPU usage for efficient execution it is None
            return psutil.cpu_percent(interval = 0.01)
        except Exception as e:
            self.__logger.error(f"Error getting the CPU Utilization. {e}")
            return 0.0

    def get_cpu_clock(self):
        """
        Returns the current CPU Clock Speed in Mhz(Mega Hertz).
        """
        try:
            return psutil.cpu_freq().current
        except Exception as e:
            self.__logger.error(f"Error getting the CPU Clock Speed. {e}")
            return None

    def get_process_cpu_util(self):
        """
        Returns the CPU Utilization of the current Python process as a percentage.
        Requires calling this function twice with an interval for an accurate reading.
        The first call initializes, subsequent calls return the percentage since last call.
        For a single snapshot, it will return the percentage since process start.
        """
        try:
            # psutil.cpu_percent() for a process calculates the percentage
            # since the last call to this method, or since process start if first call.
            # For a meaningful "snapshot" after some work, call it once before and once after.
            return self.__current_process.cpu_percent(interval= 0.01)
        except Exception as e:
            self.__logger.error(f"Error getting the process CPU Utilization. {e}")
            return 0.0

    def get_ram_usage(self):
        """
        Returns the system-wide physical RAM in MB(Megabytes).
        """
        try:
            return psutil.virtual_memory().used / (1024 * 1024) # Conver the bytes into MB
        except Exception as e:
            self.__logger.error(f"Error getting RAM usage. {e}")
            return None

    def get_process_ram_usage(self):
        """
        Returns the Resident Set Size (RSS) memory usage of the current Python process in MB(MegaBytes).
        RSS is the portion of memory held in RAM.
        """
        try:
            return self.__current_process.memory_info().rss / (1024 * 1024) # Conver the bytes into MB
        except Exception as e:
            self.__logger.error(f"Error getting Process RAM usage (RSS). {e}")
            return None

    def __check_nvidia__(self):
        try:
            if not _NVML_AVAILABLE:
                return False
            else:
                nvmlInit()
                device_count = nvmlDeviceGetCount()
                if device_count > 0:
                    return True
                else:
                    return False
        except Exception as e:
                self.__logger.error(f"Eror checking for NVIDIA graphics card. So no card exists. {e}")
                return False

    def get_gpu_clock(self):
        """
        Returns the current graphics clock speed in MHz for the first detected NVIDIA GPU.
        Returns None if pynvml is not available or no NVIDIA GPU is found.
        """
        if self.__isnvidia:
            try:
                # Get graphics clock info (NVML_CLOCK_GRAPHICS) at current level (NVML_CLOCK_ID_CURRENT)
                clock_speed = nvmlDeviceGetClockInfo(self.__handle, NVML_CLOCK_GRAPHICS)
                return float(clock_speed) # Clock speed in MHz
            except Exception as e:
                self.__logger.error(f"Unexpected error getting GPU clock speed: {e}")
                return None

    def get_gpu_util(self):
        """
        Returns the GPU utilization as a percentage for the first detected NVIDIA GPU.
        Returns None if pynvml is not available or no NVIDIA GPU is found.
        """
        if self.__isnvidia:
            try:
                utilization = nvmlDeviceGetUtilizationRates(self.__handle)
                return float(utilization.gpu) # GPU utilization as a percentage
            except Exception as e:
                self.__logger.error(f"Unexpected error getting GPU utilization: {e}")
                return None

    def get_vram_usage(self):
        """
        Returns the used VRAM in Megabytes (MB) for the first detected NVIDIA GPU.
        Returns None if pynvml is not available or no NVIDIA GPU is found.
        """
        if self.__isnvidia:
            try:
                # Get handle for the first GPU (index 0)
                info = nvmlDeviceGetMemoryInfo(self.__handle)
                return info.used / (1024 * 1024) # Convert bytes to MB
            except Exception as e:
                self.__logger.error(f"Unexpected error getting VRAM usage: {e}")
                return None

    def get_process_vram_usage(self):
        """
        Attempts to return the VRAM usage of the current Python process in Megabytes (MB)
        for NVIDIA GPUs. This relies on pynvml's process listing.
        Returns None if pynvml is not available, no NVIDIA GPU, or if the process
        is not explicitly listed by NVML (e.g., due to low activity or driver specifics).
        """
        if self.__isnvidia:
            try:
                current_pid = os.getpid()
                vram_used_by_process = 0.0
                for proc_info in nvmlDeviceGetComputeRunningProcesses(self.__handle) + nvmlDeviceGetGraphicsRunningProcesses(self.__handle):
                    if proc_info.pid == current_pid:
                        vram_used_by_process += proc_info.usedGpuMemory / (1024 * 1024) # Convert bytes to MB
                        break # Found our process, no need to continue

                if vram_used_by_process > 0:
                    return vram_used_by_process
                else:
                    return 0.0 # Return 0 if not found or no VRAM used by this process
            except Exception as e:
                self.__logger.error(f"Unexpected error getting process VRAM usage: {e}")
                return None

    def close(self):
        """
        Closes the NVML at the end of the python process.
        Has to be closed manually by the user.
        """
        if _NVML_AVAILABLE:
            try:
                nvmlShutdown() # Closing the universal NVML handel
            except Exception:
                pass

    @property
    def isNvidia(self):
        return self.__isnvidia