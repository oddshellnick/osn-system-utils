from typing import (
	Iterable,
	List,
	Literal,
	Optional,
	Union
)
from osn_system_utils.utils import (
	deduplicate_list,
	run_command,
	validate_parameter
)


__all__ = [
	"AvailablePkillModifiers",
	"PkillModifier",
	"build_kill",
	"build_pkill",
	"run_kill",
	"run_pkill"
]

PkillModifier = Literal[
	"full_command_line",
	"newest",
	"oldest",
	"exact_match",
	"case_insensitive",
	"echo_pid"
]
AvailablePkillModifiers = [
	"full_command_line",
	"newest",
	"oldest",
	"exact_match",
	"case_insensitive",
	"echo_pid"
]


def build_pkill(
		pattern: str,
		signal: Union[int, str] = 15,
		modifiers: Optional[Iterable[PkillModifier]] = None,
) -> List[str]:
	"""
	Builds the pkill command list.

	Args:
		pattern (str): The pattern to match processes.
		signal (Union[int, str]): The signal to send. Defaults to 15 (SIGTERM).
		modifiers (Optional[Iterable[PkillModifier]]): List of modifiers for pkill.

	Returns:
		List[str]: The constructed command parts.

	Raises:
		ValueError: If pattern is empty.
	"""
	
	if not pattern:
		raise ValueError("Pattern cannot be empty.")
	
	clean_modifiers = deduplicate_list(modifiers)
	
	if clean_modifiers:
		map(
				lambda modifier: validate_parameter(
						value=modifier,
						value_name="modifier",
						available_values=AvailablePkillModifiers
				),
				clean_modifiers
		)
	
	cmd = ["pkill", f"-{signal}"]
	
	if "full_command_line" in clean_modifiers:
		cmd.append("-f")
	
	if "newest" in clean_modifiers:
		cmd.append("-n")
	
	if "oldest" in clean_modifiers:
		cmd.append("-o")
	
	if "exact_match" in clean_modifiers:
		cmd.append("-x")
	
	if "case_insensitive" in clean_modifiers:
		cmd.append("-i")
	
	if "echo_pid" in clean_modifiers:
		cmd.append("-e")
	
	cmd.append(pattern)
	
	return cmd


def run_pkill(
		pattern: str,
		signal: Union[int, str] = 15,
		modifiers: Optional[Iterable[PkillModifier]] = None,
		encoding: str = "utf-8",
) -> Optional[str]:
	"""
	Executes the pkill command.

	Args:
		pattern (str): The process name pattern.
		signal (Union[int, str]): Signal to send.
		modifiers (Optional[Iterable[PkillModifier]]): Command modifiers.
		encoding (str): Output encoding.

	Returns:
		Optional[str]: The command output.
	"""
	
	return run_command(
			command_parts=build_pkill(pattern=pattern, signal=signal, modifiers=modifiers),
			encoding=encoding,
	)


def build_kill(pids: Iterable[int], signal: Union[int, str] = 15) -> List[str]:
	"""
	Builds the kill command list.

	Args:
		pids (Iterable[int]): A list of process IDs to kill.
		signal (Union[int, str]): The signal to send.

	Returns:
		List[str]: The constructed command parts.

	Raises:
		ValueError: If pids list is empty.
	"""
	
	if not pids:
		raise ValueError("List of PIDs cannot be empty.")
	
	cmd = ["kill", f"-{signal}"]
	
	for pid in deduplicate_list(pids):
		cmd.append(str(pid))
	
	return cmd


def run_kill(pids: Iterable[int], signal: Union[int, str] = 15, encoding: str = "utf-8") -> None:
	"""
	Executes the kill command for specified PIDs.

	Args:
		pids (Iterable[int]): Process IDs.
		signal (Union[int, str]): Signal to send.
		encoding (str): Output encoding.
	"""
	
	run_command(command_parts=build_kill(pids=pids, signal=signal), encoding=encoding)
