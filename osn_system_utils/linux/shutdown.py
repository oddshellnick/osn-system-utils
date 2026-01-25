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


__all__ = [
	"AvailableShutdownModes",
	"AvailableShutdownModifiers",
	"ShutdownMode",
	"ShutdownModifier",
	"build_shutdown",
	"run_shutdown"
]

ShutdownMode = Literal["poweroff", "halt", "reboot", "cancel", "kidding"]
AvailableShutdownModes = ["poweroff", "halt", "reboot", "cancel", "kidding"]

ShutdownModifier = Literal["no_wall"]
AvailableShutdownModifiers = ["no_wall"]


def build_shutdown(
		mode: ShutdownMode = "poweroff",
		modifiers: Optional[Iterable[ShutdownModifier]] = None,
		time_spec: str = "now",
		wall_message: Optional[str] = None,
) -> List[str]:
	"""
	Builds the shutdown command arguments.

	Args:
		mode (ShutdownMode): The mode of shutdown.
		modifiers (Optional[Iterable[ShutdownModifier]]): Optional flags.
		time_spec (str): Time specification string.
		wall_message (Optional[str]): Message to broadcast to logged-in users.

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
	
	if mode == "poweroff":
		cmd.append("-P")
	elif mode == "halt":
		cmd.append("-H")
	elif mode == "reboot":
		cmd.append("-r")
	elif mode == "cancel":
		cmd.append("-c")
	elif mode == "kidding":
		cmd.append("-k")
	
	if "no_wall" in clean_modifiers:
		cmd.append("--no-wall")
	
	if mode != "cancel":
		if time_spec:
			cmd.append(time_spec)
	
		if wall_message:
			cmd.append(wall_message)
	
	return cmd


def run_shutdown(
		mode: ShutdownMode = "poweroff",
		time_spec: str = "now",
		wall_message: Optional[str] = None,
		modifiers: Optional[Iterable[ShutdownModifier]] = None,
		encoding: str = "utf-8",
) -> None:
	"""
	Executes the shutdown command.

	Args:
		mode (ShutdownMode): Shutdown mode.
		time_spec (str): Time specification.
		wall_message (Optional[str]): Wall message.
		modifiers (Optional[Iterable[ShutdownModifier]]): Command modifiers.
		encoding (str): Output encoding.
	"""
	
	run_command(
			command_parts=build_shutdown(
					mode=mode,
					time_spec=time_spec,
					wall_message=wall_message,
					modifiers=modifiers,
			),
			encoding=encoding,
	)
