from typing import (
	Iterable,
	List,
	Literal,
	Optional
)
from osn_system_utils.utils import (
	deduplicate_list,
	run_command,
	validate_parameter
)


ShutdownMode = Literal[
	"shutdown",
	"restart",
	"shutdown_restart_apps",
	"restart_restart_apps",
	"logoff",
	"hibernate",
	"abort",
	"power_off_immediate"
]
AvailableShutdownModes = [
	"shutdown",
	"restart",
	"shutdown_restart_apps",
	"restart_restart_apps",
	"logoff",
	"hibernate",
	"abort",
	"power_off_immediate"
]

ShutdownModifier = Literal["force", "hybrid", "firmware_ui", "advanced_boot"]
AvailableShutdownModifiers = ["force", "hybrid", "firmware_ui", "advanced_boot"]


def build_shutdown(
		mode: ShutdownMode = "shutdown",
		modifiers: Optional[Iterable[ShutdownModifier]] = None,
		timeout: Optional[int] = None,
		comment: Optional[str] = None,
		reason: Optional[str] = None,
		target_computer: Optional[str] = None,
) -> List[str]:
	"""
	Builds the shutdown command arguments.

	Args:
		mode (ShutdownMode): The mode of operation.
		modifiers (Optional[Iterable[ShutdownModifier]]): Command flags.
		timeout (Optional[int]): Timeout in seconds.
		comment (Optional[str]): Comment for the shutdown.
		reason (Optional[str]): Reason code.
		target_computer (Optional[str]): Remote computer name.

	Returns:
		List[str]: The constructed command list.
	"""
	
	validate_parameter(value=mode, value_name="mode", available_values=AvailableShutdownModes)
	
	clean_modifiers = deduplicate_list(modifiers)
	
	if clean_modifiers:
		map(
				lambda modifier: validate_parameter(
						value=modifier,
						value_name="modifier",
						available_values=AvailableShutdownModifiers
				),
				clean_modifiers
		)
	
	cmd = ["shutdown"]
	
	if mode == "shutdown":
		cmd.append("-s")
	elif mode == "restart":
		cmd.append("-r")
	elif mode == "shutdown_restart_apps":
		cmd.append("-sg")
	elif mode == "restart_restart_apps":
		cmd.append("-g")
	elif mode == "logoff":
		cmd.append("-l")
	elif mode == "hibernate":
		cmd.append("-h")
	elif mode == "abort":
		cmd.append("-a")
	elif mode == "power_off_immediate":
		cmd.append("-p")
	
	if "hybrid" in clean_modifiers and mode == "shutdown":
		cmd.append("-hybrid")
	
	if "advanced_boot" in clean_modifiers and mode == "restart":
		cmd.append("-o")
	
	if "firmware_ui" in clean_modifiers:
		cmd.append("-fw")
	
	if "force" in clean_modifiers:
		cmd.append("-f")
	
	if target_computer:
		cmd.extend(["-m", f"\\\\{target_computer}"])
	
	if timeout is not None:
		cmd.extend(["-t", str(timeout)])
	
	if comment:
		cmd.extend(["-c", comment])
	
	if reason:
		cmd.extend(["-d", reason])
	
	return cmd


def run_shutdown(
		mode: ShutdownMode = "shutdown",
		modifiers: Optional[Iterable[ShutdownModifier]] = None,
		timeout: Optional[int] = None,
		comment: Optional[str] = None,
		reason: Optional[str] = None,
		target_computer: Optional[str] = None,
		encoding: str = "windows-1252",
) -> None:
	"""
	Executes the shutdown command.

	Args:
		mode (ShutdownMode): Operation mode.
		modifiers (Optional[Iterable[ShutdownModifier]]): Modifiers.
		timeout (Optional[int]): Timeout.
		comment (Optional[str]): Comment.
		reason (Optional[str]): Reason.
		target_computer (Optional[str]): Target.
		encoding (str): Encoding.
	"""
	
	run_command(
			command_parts=build_shutdown(
					mode=mode,
					modifiers=modifiers,
					timeout=timeout,
					comment=comment,
					reason=reason,
					target_computer=target_computer,
			),
			encoding=encoding,
	)
