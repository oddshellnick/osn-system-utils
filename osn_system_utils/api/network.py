import socket
import psutil
import collections.abc
from collections import defaultdict
from typing import (
	Any,
	Dict,
	List,
	Optional,
	Sequence,
	Union
)


def get_random_localhost_free_port() -> int:
	"""
	Finds a random free port on localhost by binding to port 0.

	Returns:
		int: A free port number.
	"""
	
	with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
		s.bind(("127.0.0.1", 0))
	
		return s.getsockname()[1]


def _is_localhost(conn: Any) -> bool:
	"""
	Checks if a connection object represents a localhost connection.

	Args:
		conn (Any): A psutil connection object.

	Returns:
		bool: True if the local address IP is in the localhost set.
	"""
	
	return hasattr(conn, 'laddr') and conn.laddr.ip in _LOCALHOST_IPS


def get_localhost_pids_with_ports() -> Dict[int, List[int]]:
	"""
	Retrieves a mapping of PIDs to lists of ports they are using on localhost.

	Returns:
		Dict[int, List[int]]: A dictionary where keys are PIDs and values are lists of ports.
	"""
	
	result = defaultdict(list)
	
	connections = [
		c
		for c in psutil.net_connections(kind="inet")
		if c.pid
		and _is_localhost(c)
	]
	
	for conn in connections:
		port = conn.laddr.port
		p_list = result[conn.pid]
	
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
		c
		for c in psutil.net_connections(kind="inet")
		if c.pid
		and _is_localhost(c)
	]
	
	for conn in connections:
		addr_str = f"{conn.laddr.ip}:{conn.laddr.port}"
		p_list = result[conn.pid]
	
		if addr_str not in p_list:
			p_list.append(addr_str)
	
	return dict(result)


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


def get_localhost_minimum_free_port(ports_to_check: Optional[Union[int, Sequence[int]]] = None) -> int:
	"""
	Finds the minimum free port from a specific set or the default range.

	Args:
		ports_to_check (Optional[Union[int, Sequence[int]]]): A specific port or sequence of ports to check.
			If None, checks the global range.

	Returns:
		int: The minimum free port found.

	Raises:
		RuntimeError: If no free ports are found in the range.
	"""
	
	if ports_to_check is not None:
		if isinstance(ports_to_check, int):
			if _is_port_free(port=ports_to_check):
				return ports_to_check
	
		if isinstance(ports_to_check, collections.abc.Sequence):
			available_candidates = [
				port
				for port in ports_to_check
				if isinstance(port, int)
				and _is_port_free(port=port)
			]
	
			if available_candidates:
				return min(available_candidates)
	
	for port in _ALL_PORTS_RANGE:
		if _is_port_free(port=port):
			return port
	
	raise RuntimeError(f"No free ports found in range {_PORT_RANGE_START}-{_PORT_RANGE_END}")


def get_localhost_busy_ports() -> List[int]:
	"""
	Retrieves a sorted list of ports currently in use on localhost.

	Returns:
		List[int]: A sorted list of busy ports.
	"""
	
	ports = {
		c.laddr.port
		for c in psutil.net_connections(kind="inet")
		if _is_localhost(c)
	}
	
	return sorted(list(ports))


def get_localhost_free_ports() -> List[int]:
	"""
	Retrieves a sorted list of all free ports in the default range on localhost.

	Returns:
		List[int]: A sorted list of free ports.
	"""
	
	busy_ports = set(get_localhost_busy_ports())
	free_ports = _ALL_PORTS_RANGE - busy_ports
	
	return sorted(list(free_ports))


_LOCALHOST_IPS = frozenset({'127.0.0.1', '::1', '0.0.0.0', '::'})

_PORT_RANGE_START = 1024
_PORT_RANGE_END = 49151
_ALL_PORTS_RANGE = frozenset(range(_PORT_RANGE_START, _PORT_RANGE_END))
