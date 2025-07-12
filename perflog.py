from imports import *

try:
    import pynvml
    _NVML_AVAILABLE = True
except ImportError:
    _NVML_AVAILABLE = False

class Perflog():
    def __init__(self):
        self.__steup_logger()
        self.__isnvidia = self.__check_nvidia()

        self.__total_runtime = 0
        self.__last_lap_time = 0

        # First initialization
        self.__get_lap()

        # Creating an object for the current process
        self.__current_process = psutil.Process(os.getpid())

        # Initilization step to start counting 
        self.__get_cpu_util()
        self.__get_process_cpu_util()

    def __steup_logger(self):
        self.__logger = logging.getLogger("PerfLog")
        self.__logger.setLevel(logging.DEBUG)
        cwd = os.path.abspath(os.getcwd())
        log_dir_path = cwd + "/log"
        log_file_path = log_dir_path + "/log.txt"

        if not os.path.isdir(log_dir_path):
            os.mkdir(log_dir_path)

        handler = logging.FileHandler(log_file_path)
        formatter = jsonlogger.JsonFormatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)

    def __log(self, log_message : str):
        if self.__isnvidia:
            self.__logger.debug(log_message,
                extra={
                    'runtime' : self.__total_runtime,
                    'lap' : self.__get_lap(),
                    'cpu_utilization' : self.__get_cpu_util(),
                    'cpu_clockspeed' : self.__get_cpu_clock(),
                    'ram' : self.__get_ram_usage(),
                    'process ram' : self.__get_process_ram_usage(),
                    'gpu_utilization' : self.__get_gpu_util(),
                    'gpu_clockspeed' : self.__get_gpu_clock(),
                    'vram' : self.__get_vram_usage(),
                    'process_vram' : self.__get_process_vram_usage()
                    })
        else:
            self.__logger.debug(log_message,
                extra={
                    'runtime' : self.__total_runtime,
                    'lap' : self.__get_lap(),
                    'cpu_utilization' : self.__get_cpu_util(),
                    'cpu_clockspeed' : self.__get_cpu_clock(),
                    'ram' : self.__get_ram_usage(),
                    'process_cpu_utilization' : self.__get_process_cpu_util(),
                    'process_ram' : self.__get_process_ram_usage(),
                    'gpu_utilization' : "None",
                    'gpu_clockspeed' : "None",
                    'vram' : "None",
                    'process_vram' : "None"
                    })

    def __get_lap(self):
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

    def __get_cpu_util(self):
        """
        Returns the current system-wide CPU utilization as a percentage.
        This function does not have an interval to interrupt process
        """
        try:
            # interval is the amount of seconds the system will pause to calculate the CPU usage for efficient execution it is None
            return psutil.cpu_percent(interval = None)
        except Exception as e:
            self.__logger.error(f"Error getting the CPU Utilization. {e}")
            return None

    def __get_cpu_clock(self):
        """
        Returns the current CPU Clock Speed in Mhz(Mega Hertz).
        """
        try:
            return psutil.cpu_freq().current
        except Exception as e:
            self.__logger.error(f"Error getting the CPU Clock Speed. {e}")
            return None

    def __get_process_cpu_util(self):
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
            return self.__current_process.cpu_percent(interval= None)
        except Exception as e:
            self.__loggger.error("Error getting the process CPU Utilization. {e}")

    def __get_ram_usage(self):
        """
        Returns the system-wide physical RAM in MB(Megabytes).
        """
        try:
            return psutil.virtual_memory().used / (1024 * 1024) # Conver the bytes into MB
        except Exception as e:
            self.__logge.error(f"Error getting RAM usage. {e}")
            return None

    def __get_process_ram_usage(self):
        """
        Returns the Resident Set Size (RSS) memory usage of the current Python process in MB(MegaBytes).
        RSS is the portion of memory held in RAM.
        """
        try:
            return self.__current_process.memory_info().rss / (1024 / 1024) # Conver the bytes into MB
        except Exception as e:
            self.__logge.error(f"Error getting Process RAM usage (RSS). {e}")
            return None

    def __check_nvidia(self):
        try:
            if not _NVML_AVAILABLE:
                return False
            else:
                nvmlInit()
                device_count = nvmlDeviceGetCount()
                nvmlShutdown()
                if device_count > 0:
                    return True
                else:
                    return False
        except Exception as e:
                self.__logger.error(f"Eror checking for NVIDIA graphics card. So no card exists. {e}")
                return False

    def __get_gpu_clock(self):
        """
        Returns the current graphics clock speed in MHz for the first detected NVIDIA GPU.
        Returns None if pynvml is not available or no NVIDIA GPU is found.
        """
        if self.__check_nvidia:
            try:
                nvmlInit()
                handel = nvmlDeviceGetHandleByIndex(0) # Get handle for the first GPU (index 0)
                # Get graphics clock info (NVML_CLOCK_GRAPHICS) at current level (NVML_CLOCK_ID_CURRENT)
                clock_speed = nvmlDeviceGetClockInfo(handel, NVML_CLOCK_GRAPHICS, NVML_CLOCK_ID_CURRENT)
                nvmlShutdown()
                return float(clock_speed) # Clock speed in MHz
            except Exception as e:
                self.__logger.error(f"Unexpected error getting GPU clock speed: {e}")
                return None

    def __get_gpu_util(self):
        """
        Returns the GPU utilization as a percentage for the first detected NVIDIA GPU.
        Returns None if pynvml is not available or no NVIDIA GPU is found.
        """
        if self.__isnvidia:
            try:
                nvmlInit()
                handle = nvmlDeviceGetHandleByIndex(0) # Get handle for the first GPU (index 0)
                utilization = nvmlDeviceGetUtilizationRates(handle)
                nvmlShutdown()
                return float(utilization.gpu) # GPU utilization as a percentage
            except Exception as e:
                self.__logger.error(f"Unexpected error getting GPU utilization: {e}")
                return None

    def __get_vram_usage(self):
        """
        Returns the used VRAM in Megabytes (MB) for the first detected NVIDIA GPU.
        Returns None if pynvml is not available or no NVIDIA GPU is found.
        """
        if self.__isnvidia:
            try:
                nvmlInit()
                handle = nvmlDeviceGetHandleByIndex(0) # Get handle for the first GPU (index 0)
                info = nvmlDeviceGetMemoryInfo(handle)
                nvmlShutdown()
                return info.used / (1024 * 1024) # Convert bytes to MB
            except Exception as e:
                self.__logger.error(f"Unexpected error getting VRAM usage: {e}")
                return None

    def __get_process_vram_usage(self):
        """
        Attempts to return the VRAM usage of the current Python process in Megabytes (MB)
        for NVIDIA GPUs. This relies on pynvml's process listing.
        Returns None if pynvml is not available, no NVIDIA GPU, or if the process
        is not explicitly listed by NVML (e.g., due to low activity or driver specifics).
        """
        if self.__isnvidia:
            try:
                nvmlInit()
                current_pid = os.getpid()
                vram_used_by_process = 0.0

                device_count = nvmlDeviceGetCount()
                for i in range(device_count):
                    handle = nvmlDeviceGetHandleByIndex(i)
                    # Get compute and graphics processes running on this GPU
                    # Some processes might not be listed, or might be listed under graphics/compute
                    for proc_info in nvmlDeviceGetComputeRunningProcesses(handle) + nvmlDeviceGetGraphicsRunningProcesses(handle):
                        if proc_info.pid == current_pid:
                            vram_used_by_process += proc_info.usedGpuMemory / (1024 * 1024) # Convert bytes to MB
                            break # Found our process on this GPU, move to next GPU

                nvmlShutdown()
                if vram_used_by_process > 0:
                    return vram_used_by_process
                else:
                    self.__logger.error(f"Process {current_pid} not explicitly listed by NVML for VRAM usage, or 0 VRAM used.")
                    return 0.0 # Return 0 if not found or no VRAM used by this process
            except Exception as e:
                self.__logger.error(f"Unexpected error getting process VRAM usage: {e}")
                return None

    @property
    def isNvidia(self):
        return self.__isnvidia