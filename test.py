import unittest
from perflog import Perflog

class TestPerflog(unittest.TestCase):
    def setUp(self):
        self.test = Perflog()
        self.test.log("damn")

    def test_gpu(self):
        # Testing to check for an NVIDIA GPU which is installed in my current system
        self.assertTrue(self.test.isNvidia)
    
    def test_lap(self):
        # Checking for lap time under 10 seconds
        self.assertLess(self.test.get_lap(), 10)

    def test_cpu_util(self):
        # CPU utilization should be between 0 (exclusive) and 100 (inclusive)
        # Doing some work to generate CPU usage
        for i in range(100000):
            _ = i ** 2
        cpu_util = self.test.get_cpu_util()
        self.assertGreaterEqual(cpu_util, 0.0)
        self.assertLessEqual(cpu_util, 100.0)

    def test_process_cpu_util(self):
        # Process CPU utilization should be between 0 (exclusive) and 100 (inclusive)
        # Doing some work to generate CPU usage
        for i in range(100000):
            _ = i ** 2
        process_cpu_util = self.test.get_process_cpu_util()
        self.assertGreaterEqual(process_cpu_util, 0.0)
        self.assertLessEqual(process_cpu_util, 100.0)

    def test_cpu_clock(self):
        # Maximum attained CPU clock speed is 6.2 GHz and the base frequency of my cpu is 3.8 GHz
        cpu_clock = self.test.get_cpu_clock()
        self.assertLessEqual(cpu_clock, 6200)
        self.assertGreaterEqual(cpu_clock, 3800)

    def test_ram(self):
        # Global RAM utilization between 5GB and 32GB(max capacity)
        self.assertGreater(self.test.get_ram_usage(), 5000)
        self.assertLess(self.test.get_ram_usage(), 32000)

    def test_process_ram(self):
        # Doing some work to generate RAM usage
        test_list = [i for i in range(10000000)]
        process_ram_usage = self.test.get_process_ram_usage()
        self.assertGreater(process_ram_usage, 250)
        self.assertLess(process_ram_usage, 32000)
        # Setting it back to None to clear memory
        test_list = None

    def test_vram(self):
        # Setting it for 250 as the GPU is responsible for my screen out put. Max 8000 because that is my VRAM capacity
        vram_usage = self.test.get_vram_usage()
        self.assertGreater(vram_usage, 250)
        self.assertLess(vram_usage, 8000)

    def test_process_vram(self):
        # No VRAM use by default
        self.assertEqual(self.test.get_process_vram_usage(), 0.0)

    def test_gpu_clock(self):
        # Setting min of 200 MHz and max of 3800 MHz for the GPU
        gpu_clock = self.test.get_gpu_clock()
        self.assertGreaterEqual(gpu_clock, 200)
        self.assertLessEqual(gpu_clock, 3800)

    def test_gpu_util(self):
        # Process CPU utilization should be between 0 (exclusive) and 100 (inclusive)
        gpu_util = self.test.get_gpu_util()
        self.assertGreaterEqual(gpu_util, 0.0)
        self.assertLessEqual(gpu_util, 100.0)

    def tearDown(self):
        self.test.close()

if __name__ == "__main__":
    unittest.main()
