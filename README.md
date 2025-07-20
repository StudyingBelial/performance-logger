# sb_perflog

## Table of Content
* [Project Overview](#project-overview)
* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)
* [Configuration](#configuration)
* [License](#license)

## Project Overview
After having to write a substantial amount of code relating to AI, while at the same time trying to make it performant; I realized that I had little to no idea of how much performance impact any of my code had. So this is just a tool I developed for me to be able to log system perfomance and utilization in a single GPU environment. Specifically single GPU because that's all I have at the moment and that's also what is only availaible in the free version of Google Colab.

## Features
- Logs system-wide CPU utilization and clock speed.
- Logs system-wide RAM usage.
- Logs CPU and RAM usage of the current Python process.
- If an NVIDIA GPU is present, logs GPU utilization, clock speed, VRAM usage, and process VRAM usage.
- Tracks and logs the time elapsed since the last log (lap time).
- Easy-to-use API for integrating into your Python applications.

## Requirements
- Python 3.x
- psutil library for system and process metrics.
- pynvml library for NVIDIA GPU metrics (optional, but required for GPU logging).
- pythonjsonlogger library for JSON-formatted logging.
- NVIDIA GPU and appropriate drivers (for GPU metrics).

## Installation
To use Perflog, include the Perflog class in your Python project by copying the code into your project or importing it if part of a package.
Install the required libraries using pip:
```bash
pip install psutil pynvml pythonjsonlogger
```
Note: pynvml is optional but required for GPU metrics. If not installed or no NVIDIA GPU is present, GPU metrics will be omitted.

## Usage
Here’s a basic example of how to use Perflog in your Python code:

```python
from perflog import Perflog

# Initialize Perflog
perf = Perflog()

# Your code here
# ...

# Log a message with metrics
perf.log("This is a log message")

# More code
# ...

# Log another message
perf.log("Another log message")

# Close Perflog (important to release resources)
perf.close()
```

The log file is written to logs/perflog.txt in the current working directory. If the logs directory does not exist, it will be created automatically.

The Perflog Object has to be closed at the end of the program to ensure all that NVML is shutdown correctly.

## Configuration
By default, Perflog writes logs to logs/perflog.txt in the current working directory. To specify a different log file path, modify the __setup_logger__ method in the Perflog class.

## Notes
- **Resource Cleanup**: Call the close method when done with Perflog to shut down NVML and release resources, especially if using GPU metrics.
- **No NVIDIA GPU**: If no NVIDIA GPU is detected or pynvml is unavailable, Perflog will log only CPU and RAM metrics.
- **Lap Time**: The get_lap method tracks time between logs and is called automatically within log.
- **Process CPU Utilization**: For accurate process CPU utilization, call get_process_cpu_util multiple times with intervals, as it calculates usage since the last call.

## License
This project is licensed under the [MIT License](LICENSE)