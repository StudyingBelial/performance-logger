from imports import *

class Perflog():
    def __init__(self):
        self.__steup_logger()

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
                    'cpu_utilization' : self.get_cpu_util(),
                    'cpu_clockspeed' : self.get_cpu_clock(),
                    'ram' : self.get_ram_usage(),
                    'process ram' : self.get_process_ram_usage(),
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
                    'cpu_utilization' : self.get_cpu_util(),
                    'cpu_clockspeed' : self.get_cpu_clock(),
                    'ram' : self.get_ram_usage(),
                    'process_cpu_utilization' : self.get_process_cpu_util(),
                    'process_ram' : self.get_process_ram_usage(),
                    'gpu_utilization' : "None",
                    'gpu_clockspeed' : "None",
                    'vram' : "None",
                    'process_vram' : "None"
                    })

    def __get_lap(self):
        pass

    def __check_nvidia(self):
        pass

    def __get_cpu_util(self):
        pass

    def __get_cpu_clock(self):
        pass

    def __get_process_cpu_util(self):
        pass

    def __get_ram_usage(self):
        pass

    def __get_process_ram_usage(self):
        pass

    def __get_gpu_clock(self):
        pass

    def __get_gpu_util(self):
        pass

    def __get_vram_usage(self):
        pass

    def __get_process_vram_usage(self):
        pass

    @property
    def isNvidia(self):
        pass