# osn-system-utils: Cross-platform system command wrappers and network utilities

This library provides a set of Python abstractions for common system administration tasks on Linux and Windows, as well as utilities for network port management. It allows developers to interact with system commands like `shutdown`, `kill`, `netstat`, and `ss` using structured, type-hinted Python functions instead of raw shell execution strings.

## Technologies

| Name           | Badge                                                                                                                                               | Description                                                               |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| Python         | [![Python](https://img.shields.io/badge/Python%2DPython?style=flat&logo=python&color=%231f4361)](https://www.python.org/)                           | The core language used for implementing the wrappers and logic.           |
| Psutil         | [![Psutil](https://img.shields.io/badge/psutil%2Dpsutil?style=flat&color=%230f90a1)](https://pypi.org/project/psutil/)                              | Used for retrieving network connection details and mapping PIDs to ports. |
| Subprocess     | [![Subprocess](https://img.shields.io/badge/subprocess%2Dsubprocess?style=flat&color=%23a3c910)](https://docs.python.org/3/library/subprocess.html) | Used to execute the underlying system shell commands.                     |
| Socket         | [![Socket](https://img.shields.io/badge/socket%2Dsocket?style=flat&color=%230f53b5)](https://docs.python.org/3/library/socket.html)                 | Used for binding checks to identify free ports on localhost.              |

## Key Features

*   **Cross-Platform Network Utilities:**
    *   Find random or minimum free ports on localhost.
    *   Map PIDs to used ports and addresses.
    *   Identify busy and free ports within specific ranges.
*   **Linux System Wrappers:**
    *   `kill` and `pkill` for process management.
    *   `shutdown` for power management.
    *   `ss` for detailed socket statistics.
*   **Windows System Wrappers:**
    *   `taskkill` for process termination.
    *   `shutdown` for power management.
    *   `netstat` for network statistics.
*   **Type Safety:**
    *   Input validation for command arguments (modes, modifiers, protocols).
    *   Custom exception handling for command execution failures.

## Installation

1. Install library:
    *   **With pip:**
        ```bash
        pip install osn-system-utils
        ```

        **With pip (beta versions):**
        ```bash
        pip install -i https://test.pypi.org/simple/ osn-system-utils
        ```

    *   **With git:**
        ```bash
        pip install git+https://github.com/oddshellnick/osn-system-utils.git
        ```
        *(Ensure you have git installed)*

2. **Install the required Python packages using pip:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Here are some examples of how to use `osn-system-utils`:

### Network Utilities

Retrieve a free port on localhost or check which ports are busy.

```python
from osn_system_utils.api.network import get_random_localhost_free_port, get_localhost_pids_with_ports

# Get a random free port
port = get_random_localhost_free_port()
print(f"Found free port: {port}")

# Get mapping of PIDs to ports
pid_map = get_localhost_pids_with_ports()
print(pid_map)
```

### Linux Process Management

Kill a process by name pattern on a Linux system.

```python
from osn_system_utils.linux.kill import run_pkill

try:
    # Kill the newest process matching "python_script"
    output = run_pkill(pattern="python_script", modifiers=["newest"])
    print("Process killed.")
except Exception as e:
    print(f"Error: {e}")
```

### Windows Task Management

Forcefully terminate a task by image name on Windows.

```python
from osn_system_utils.windows.taskkill import run_taskkill

try:
    # Force kill notepad.exe
    run_taskkill(image_names=["notepad.exe"], modifiers=["force"])
    print("Notepad closed.")
except ValueError as e:
    print(e)
```

## Classes and Functions

### Core Utilities (`osn_system_utils`)
*   **`exceptions`**
    *   `CommandExecutionError` - Exception raised when a command execution fails.
*   **`utils`**
    *   `validate_parameter(...)` - Validates that a value is present in a list of available values.
    *   `run_command(...)` - Executes a shell command provided as a list of parts.
    *   `deduplicate_list(...)` - Removes duplicate items from a list while preserving order.

### Network API (`osn_system_utils.api.network`)
*   `get_random_localhost_free_port(...)` - Finds a random free port on localhost by binding to port 0.
*   `get_localhost_pids_with_ports(...)` - Retrieves a mapping of PIDs to lists of ports they are using on localhost.
*   `get_localhost_pids_with_addresses(...)` - Retrieves a mapping of PIDs to lists of formatted addresses (IP:Port) on localhost.
*   `get_localhost_minimum_free_port(...)` - Finds the minimum free port from a specific set or the default range.
*   `get_localhost_busy_ports(...)` - Retrieves a sorted list of ports currently in use on localhost.
*   `get_localhost_free_ports(...)` - Retrieves a sorted list of all free ports in the default range on localhost.

### Linux Wrappers (`osn_system_utils.linux`)
*   **`kill`**
    *   `build_pkill(...)` - Builds the pkill command list.
    *   `run_pkill(...)` - Executes the pkill command.
    *   `build_kill(...)` - Builds the kill command list.
    *   `run_kill(...)` - Executes the kill command for specified PIDs.
*   **`shutdown`**
    *   `build_shutdown(...)` - Builds the shutdown command arguments.
    *   `run_shutdown(...)` - Executes the shutdown command.
*   **`ss`**
    *   `build_ss(...)` - Builds the ss (socket statistics) command arguments.
    *   `run_ss(...)` - Executes the ss command.

### Windows Wrappers (`osn_system_utils.windows`)
*   **`netstat`**
    *   `build_netstat(...)` - Builds the netstat command arguments.
    *   `run_netstat(...)` - Executes the netstat command.
*   **`shutdown`**
    *   `build_shutdown(...)` - Builds the shutdown command arguments (Windows specific).
    *   `run_shutdown(...)` - Executes the shutdown command.
*   **`taskkill`**
    *   `build_taskkill(...)` - Builds the taskkill command arguments.
    *   `run_taskkill(...)` - Executes the taskkill command.

## Future Notes

*   Implementation of MacOS specific command wrappers.
*   Asynchronous versions of command execution functions.
*   Wrappers for many other commands.
*   Integration with remote command execution via SSH.