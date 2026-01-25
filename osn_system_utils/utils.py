import subprocess
from osn_system_utils.exceptions import (
	CommandExecutionError
)
from typing import (
	Any,
	Iterable,
	List,
	Optional,
	Sequence,
	TypeVar
)


__all__ = ["deduplicate_list", "run_command", "validate_parameter"]

_T = TypeVar("_T")


def validate_parameter(value: Any, value_name: str, available_values: Iterable[Any]) -> None:
	"""
	Validates that a value is present in a list of available values.

	Args:
		value (Any): The value to check.
		value_name (str): The name of the value for the error message.
		available_values (Iterable[Any]): A sequence of valid values.

	Raises:
		ValueError: If the value is not in available_values.
	"""
	
	if value not in available_values:
		available_str = ", ".join(map(str, available_values))
	
		raise ValueError(f"Invalid {value_name}: {value}. Valid values are: {available_str}")


def run_command(command_parts: Sequence[str], encoding: str) -> str:
	"""
	Executes a shell command provided as a list of parts.

	Args:
		command_parts (Sequence[str]): The parts of the command to execute.
		encoding (str): The encoding to use for the output.

	Returns:
		str: The standard output of the command.

	Raises:
		CommandExecutionError: If the command fails or is not found.
	"""
	
	cmd = [str(part) for part in command_parts if part]
	
	try:
		result = subprocess.run(
				cmd,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				text=True,
				encoding=encoding,
				shell=False,
		)
	
		if result.returncode != 0:
			raise CommandExecutionError(f"Command failed: {' '.join(cmd)}\nError: {result.stderr}")
	
		return result.stdout
	except FileNotFoundError:
		raise CommandExecutionError(f"Command not found: {cmd[0]}")


def deduplicate_list(items: Optional[Iterable[_T]]) -> List[_T]:
	"""
	Removes duplicate items from a list while preserving order.

	Args:
		items (Optional[Iterable[T]]): The input sequence or list.

	Returns:
		List[T]: A list containing unique items.
	"""
	
	if not items:
		return []
	
	return list(dict.fromkeys(items))
