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

    def __log(self):
        pass

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