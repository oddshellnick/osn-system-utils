# osn_system_utils: A comprehensive cross-platform library for system process and network management.

This library provides a high-level API for managing system processes, discovering network ports, and executing OS-specific commands like shutdown or socket statistics on both Linux and Windows.

## Technologies

| Name           | Badge                                                                                                                                               | Description                                                               |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| Python         | [![Python](https://img.shields.io/badge/Python%2DPython?style=flat&logo=python&color=%231f4361)](https://www.python.org/)                           | The core language used for implementing the wrappers and logic.           |
| Psutil         | [![Psutil](https://img.shields.io/badge/psutil%2Dpsutil?style=flat&color=%230f90a1)](https://pypi.org/project/psutil/)                              | Used for retrieving network connection details and mapping PIDs to ports. |
| Subprocess     | [![Subprocess](https://img.shields.io/badge/subprocess%2Dsubprocess?style=flat&color=%23a3c910)](https://docs.python.org/3/library/subprocess.html) | Used to execute the underlying system shell commands.                     |
| Socket         | [![Socket](https://img.shields.io/badge/socket%2Dsocket?style=flat&color=%230f53b5)](https://docs.python.org/3/library/socket.html)                 | Used for binding checks to identify free ports on localhost.              |

## Key Features

*   **Network Management**
    *   Find free ports on localhost using various strategies (min, max, random).
    *   Map PIDs to active ports or formatted addresses.
    *   Check for busy and free ports within specific ranges.
*   **Process Management**
    *   Kill processes by name or PID with support for process trees.
    *   Query process tables with advanced filtering (regex, equality, numeric ranges).
    *   Cross-platform check for process existence.
*   **OS-Specific Wrappers**
    *   **Linux:** High-level wrappers for `pkill`, `kill`, `shutdown`, and `ss` (socket statistics).
    *   **Windows:** High-level wrappers for `taskkill`, `shutdown`, and `netstat`.

## Installation

1. Install library:
    *   **With pip:**
        ```bash
        pip install osn_system_utils
        ```

        **With pip (beta versions):**
        ```bash
        pip install -i https://test.pypi.org/simple/ osn_system_utils
        ```

    *   **With git:**
        ```bash
        pip install git+https://github.com/oddshellnick/osn_system_utils.git
        ```
        *(Ensure you have git installed)*

2. **Install the required Python packages using pip:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Here are some examples of how to use `osn_system_utils`:

### Network Port Discovery

```python
from osn_system_utils.api.network import get_localhost_free_port_of

# Find the first available free port in the default range
port = get_localhost_free_port_of(on_candidates="min")
print(f"Available port: {port}")

# Find a random free port from a specific list
specific_port = get_localhost_free_port_of(ports_to_check=[8080, 8081, 9000], on_candidates="random")
```

### Advanced Process Filtering

```python
from osn_system_utils.api.process import get_process_table
import re

# Get all python processes using more than 100MB of memory
filters = {
    "memory_info.rss": 100 * 1024 * 1024
}
for proc in get_process_table(above_filter=filters):
    print(proc)
```

### Linux Socket Statistics (ss)

```python
from osn_system_utils.linux.ss import run_ss

# Get a summary of all listening TCP sockets
output = run_ss(mode="list", scope="listening", protocols=["tcp"])
print(output)
```

## Classes and Functions

### General Utilities (`osn_system_utils.utils`)
*   `validate_parameter(...)`: Validates that a value exists within a sequence of allowed values.
*   `run_command(...)`: Executes a shell command and returns the stdout.
*   `deduplicate_list(...)`: Removes duplicates from an iterable while maintaining order.
*   `CommandExecutionError`: Exception raised when a system command fails.

### Network API (`osn_system_utils.api.network`)
*   `get_random_localhost_free_port()`
*   `get_localhost_pids_with_ports()`
*   `get_localhost_pids_with_addresses()`
*   `get_localhost_busy_ports()`
*   `get_localhost_free_ports()`
*   `get_localhost_free_port_of(...)`

### Process API (`osn_system_utils.api.process`)
*   `kill_processes_by_name(...)`
*   `kill_process_by_pid(...)`
*   `get_process_table(...)`
*   `check_process_exists_by_pid(...)`
*   `check_process_exists_by_name(...)`

### Linux System Wrappers (`osn_system_utils.linux`)
*   `kill`:
    *   `run_pkill(...)`: Execute Linux `pkill`.
    *   `run_kill(...)`: Execute Linux `kill` for specific PIDs.
*   `shutdown`:
    *   `run_shutdown(...)`: Manage system power (reboot, poweroff, etc.).
*   `ss`:
    *   `run_ss(...)`: Execute socket statistics command.

### Windows System Wrappers (`osn_system_utils.windows`)
*   `netstat`:
    *   `run_netstat(...)`: Execute Windows `netstat` with various flags.
*   `shutdown`:
    *   `run_shutdown(...)`: Manage Windows system power and restart behavior.
*   `taskkill`:
    *   `run_taskkill(...)`: Terminate tasks by PID or Image Name.

## Future Notes

*   Implementation of MacOS specific command wrappers.
*   Asynchronous versions of command execution functions.
*   Wrappers for many other commands.
*   Integration with remote command execution via SSH.