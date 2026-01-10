import re
import psutil
import functools
from pandas import DataFrame
from typing import (
	Any,
	Callable,
	Dict,
	List,
	Tuple
)
from osn_system_utils.api._functions import (
	check_above,
	check_between,
	check_equal,
	check_not_equal,
	check_regex,
	check_under,
	get_nested_val
)


def _kill_proc_obj(proc: psutil.Process, force: bool = False, tree: bool = False) -> bool:
	"""
	Internal helper to kill a process object, optionally killing its children tree.

	Args:
		proc (psutil.Process): The process object to kill.
		force (bool): If True, uses kill(), else terminate().
		tree (bool): If True, kills the process tree recursively.

	Returns:
		bool: True if operation initiated successfully, False if process access failed.
	"""
	
	try:
		procs_to_kill = [proc]
	
		if tree:
			try:
				procs_to_kill.extend(proc.children(recursive=True))
			except (psutil.NoSuchProcess, psutil.AccessDenied):
				pass
	
		for p in procs_to_kill:
			try:
				if force:
					p.kill()
				else:
					p.terminate()
			except (psutil.NoSuchProcess, psutil.AccessDenied):
				continue
	
		return True
	
	except (psutil.NoSuchProcess, psutil.AccessDenied):
		return False


def kill_processes_by_name(
		name: str,
		force: bool = False,
		tree: bool = False,
		case_sensitive: bool = False
) -> List[int]:
	"""
	Kills all processes matching a specific name.

	Args:
		name (str): The process name.
		force (bool): Use SIGKILL if True.
		tree (bool): Kill children processes if True.
		case_sensitive (bool): Match name case-sensitively.

	Returns:
		List[int]: A list of PIDs that were successfully targeted.
	"""
	
	killed_pids = []
	
	target_name = name if case_sensitive else name.lower()
	
	for proc in psutil.process_iter(["pid", "name"]):
		try:
			p_name = proc.info["name"]
	
			if not p_name:
				continue
	
			is_match = (p_name == target_name) if case_sensitive else (p_name.lower() == target_name)
	
			if is_match:
				if _kill_proc_obj(proc, force=force, tree=tree):
					killed_pids.append(proc.info["pid"])
	
		except (psutil.NoSuchProcess, psutil.AccessDenied):
			continue
	
	return killed_pids


def kill_process_by_pid(pid: int, force: bool = False, tree: bool = False) -> bool:
	"""
	Kills a process identified by its PID.

	Args:
		pid (int): The process ID.
		force (bool): Use SIGKILL if True.
		tree (bool): Kill children processes if True.

	Returns:
		bool: True if successful, False if process not found or access denied.
	"""
	
	try:
		proc = psutil.Process(pid)
		return _kill_proc_obj(proc, force=force, tree=tree)
	
	except psutil.NoSuchProcess:
		return False


def get_process_table(
		columns: Dict[str, str] = None,
		regex_filter: Dict[str, re.Pattern[str]] = None,
		equal_filter: Dict[str, Any] = None,
		not_equal_filter: Dict[str, Any] = None,
		above_filter: Dict[str, Any] = None,
		under_filter: Dict[str, Any] = None,
		between_filter: Dict[str, Tuple[Any, Any]] = None,
) -> DataFrame:
	"""
	Generates a pandas DataFrame of system processes, filtered by various criteria.

	Args:
		columns (Dict[str, str]): Map of DataFrame column names to psutil attribute names.
		regex_filter (Dict[str, re.Pattern[str]]): Filters attributes matching regex patterns.
		equal_filter (Dict[str, Any]): Filters attributes equal to values.
		not_equal_filter (Dict[str, Any]): Filters attributes not equal to values.
		above_filter (Dict[str, Any]): Filters attributes strictly greater than values.
		under_filter (Dict[str, Any]): Filters attributes strictly less than values.
		between_filter (Dict[str, Tuple[Any, Any]]): Filters attributes strictly between two values.

	Returns:
		DataFrame: A pandas DataFrame containing the process information.
	"""
	
	if columns is None:
		columns = {"PID": "pid", "Name": "name", "Status": "status"}
	
	attributes_to_fetch = set(key.split(".")[0] for key in columns.values())
	
	all_filters = [
		regex_filter,
		equal_filter,
		not_equal_filter,
		above_filter,
		under_filter,
		between_filter
	]
	
	for f_dict in all_filters:
		if f_dict:
			for key in f_dict.keys():
				attributes_to_fetch.add(key.split(".")[0])
	
	validators: List[Callable[[Dict[str, Any]], bool]] = []
	
	if regex_filter:
		for attr, pattern in regex_filter.items():
			validators.append(functools.partial(check_regex, attribute=attr, pattern=pattern))
	
	if equal_filter:
		for attr, target in equal_filter.items():
			validators.append(functools.partial(check_equal, attribute=attr, target=target))
	
	if not_equal_filter:
		for attr, target in not_equal_filter.items():
			validators.append(functools.partial(check_not_equal, attribute=attr, target=target))
	
	if above_filter:
		for attr, limit in above_filter.items():
			validators.append(functools.partial(check_above, attribute=attr, limit=limit))
	
	if under_filter:
		for attr, limit in under_filter.items():
			validators.append(functools.partial(check_under, attribute=attr, limit=limit))
	
	if between_filter:
		for attr, (min_v, max_v) in between_filter.items():
			validators.append(functools.partial(check_between, attribute=attr, min_=min_v, max_=max_v))
	
	data: List[Dict[str, Any]] = []
	
	for proc in psutil.process_iter(attributes_to_fetch):
		try:
			info = proc.info
	
			if not all(validate(info) for validate in validators):
				continue
	
			data.append(
					{
						col_name: get_nested_val(value=info, path=attr_path)
						for col_name, attr_path in columns.items()
					}
			)
		except (psutil.NoSuchProcess, psutil.AccessDenied):
			continue
	
	return DataFrame(data)


def check_process_exists_by_pid(pid: int) -> bool:
	"""
	Checks if a process exists with the given PID.

	Args:
		pid (int): The process ID.

	Returns:
		bool: True if the process exists.
	"""
	
	return psutil.pid_exists(pid)


def check_process_exists_by_name(name: str, case_sensitive: bool = False) -> bool:
	"""
	Checks if any process exists with the given name.

	Args:
		name (str): The name of the process to search for.
		case_sensitive (bool): Whether the search matches case sensitivity.

	Returns:
		bool: True if a matching process exists.
	"""
	
	target_name = name if case_sensitive else name.lower()
	iterator = psutil.process_iter(["name"])
	
	if case_sensitive:
		return any(p.info["name"] == target_name for p in iterator)
	
	return any(p.info["name"] and p.info["name"].lower() == target_name for p in iterator)
