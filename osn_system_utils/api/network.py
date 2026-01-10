import random
import socket
import psutil
from collections import defaultdict
from osn_system_utils.utils import validate_parameter
from osn_system_utils.api._utils import (
	ALL_PORTS_RANGE,
	LOCALHOST_IPS
)
from typing import (
	Dict,
	List,
	Literal,
	Optional,
	Sequence,
	TYPE_CHECKING,
	Union
)


if TYPE_CHECKING:
	from psutil._common import sconn


def get_random_localhost_free_port() -> int:
	"""
	Finds a random free port on localhost by binding to port 0.

	Returns:
		int: A free port number.
	"""
	
	with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
		s.bind(("127.0.0.1", 0))
	
		return s.getsockname()[1]


def _is_localhost(connection: "sconn") -> bool:
	"""
	Checks if a connection object represents a localhost connection.

	Args:
		connection ("sconn"): A psutil connection object.

	Returns:
		bool: True if the local address IP is in the localhost set.
	"""
	
	return hasattr(connection, "laddr") and connection.laddr.ip in LOCALHOST_IPS


def get_localhost_pids_with_ports() -> Dict[int, List[int]]:
	"""
	Retrieves a mapping of PIDs to lists of ports they are using on localhost.

	Returns:
		Dict[int, List[int]]: A dictionary where keys are PIDs and values are lists of ports.
	"""
	
	result = defaultdict(list)
	
	connections = [
		connection
		for connection in psutil.net_connections(kind="inet")
		if connection.pid
		and _is_localhost(connection=connection)
	]
	
	for connection in connections:
		port = connection.laddr.port
		p_list = result[connection.pid]
	
		if port not in p_list:
			p_list.append(port)
	
	return dict(result)


def get_localhost_pids_with_addresses() -> Dict[int, List[str]]:
	"""
	Retrieves a mapping of PIDs to lists of formatted addresses (IP:Port) on localhost.

	Returns:
		Dict[int, List[str]]: A dictionary where keys are PIDs and values are lists of address strings.
	"""
	
	result = defaultdict(list)
	
	connections = [
		connection
		for connection in psutil.net_connections(kind="inet")
		if connection.pid
		and _is_localhost(connection=connection)
	]
	
	for connection in connections:
		addr_str = f"{connection.laddr.ip}:{connection.laddr.port}"
		p_list = result[connection.pid]
	
		if addr_str not in p_list:
			p_list.append(addr_str)
	
	return dict(result)


def get_localhost_busy_ports() -> List[int]:
	"""
	Retrieves a sorted list of ports currently in use on localhost.

	Returns:
		List[int]: A sorted list of busy ports.
	"""
	
	ports = {
		connection.laddr.port
		for connection in psutil.net_connections(kind="inet")
		if _is_localhost(connection=connection)
	}
	
	return sorted(list(ports))


def get_localhost_free_ports() -> List[int]:
	"""
	Retrieves a sorted list of all free ports in the default range on localhost.

	Returns:
		List[int]: A sorted list of free ports.
	"""
	
	busy_ports = set(get_localhost_busy_ports())
	free_ports = ALL_PORTS_RANGE - busy_ports
	
	return sorted(list(free_ports))


def _is_port_free(port: int) -> bool:
	"""
	Checks if a specific port is free on localhost.

	Args:
		port (int): The port number to check.

	Returns:
		bool: True if the port is free, False otherwise.
	"""
	
	try:
		with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
			s.bind(("127.0.0.1", port))
	
			return True
	
	except OSError:
		return False


def get_localhost_free_port_of(
		ports_to_check: Optional[Union[int, Sequence[int]]] = None,
		on_candidates: Literal["min", "max", "random"] = "min",
) -> int:
	"""
	Finds a free port among candidates or the global range.

	Args:
		ports_to_check (Optional[Union[int, Sequence[int]]]): Specific port(s) to check.
		on_candidates (Literal["min", "max", "random"]): Strategy to select from candidates.

	Returns:
		int: A free port number.

	Raises:
		TypeError: If ports_to_check is invalid type.
		RuntimeError: If no free ports are found.
	"""
	
	validate_parameter(
			value=on_candidates,
			value_name="on_candidates",
			available_values=["min", "max", "random"]
	)
	
	if isinstance(ports_to_check, int):
		candidates_iterator = [ports_to_check]
	elif isinstance(ports_to_check, Sequence):
		valid_ports = [p for p in ports_to_check if isinstance(p, int)]
	
		if on_candidates == "min":
			valid_ports.sort()
		elif on_candidates == "max":
			valid_ports.sort(reverse=True)
		elif on_candidates == "random":
			random.shuffle(valid_ports)
	
		candidates_iterator = valid_ports
	elif ports_to_check is None:
		if on_candidates == "min":
			candidates_iterator = ALL_PORTS_RANGE
		elif on_candidates == "max":
			candidates_iterator = reversed(ALL_PORTS_RANGE)
		elif on_candidates == "random":
			candidates_list = list(ALL_PORTS_RANGE)
			random.shuffle(candidates_list)
	
			candidates_iterator = candidates_list
	else:
		raise TypeError("ports_to_check must be an integer or a sequence of integers")
	
	for port in candidates_iterator:
		if _is_port_free(port):
			return port
	
	source_msg = "provided ports" if ports_to_check is not None else "global range"
	raise RuntimeError(f"No free ports found in {source_msg}")
