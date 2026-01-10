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


TaskkillModifier = Literal["force", "tree"]
AvailableTaskkillModifiers = ["force", "tree"]


def build_taskkill(
		pids: Optional[Iterable[int]] = None,
		image_names: Optional[Iterable[str]] = None,
		modifiers: Optional[Iterable[TaskkillModifier]] = None,
		system: Optional[str] = None,
		username: Optional[str] = None,
		password: Optional[str] = None,
) -> List[str]:
	"""
	Builds the taskkill command arguments.

	Args:
		pids (Optional[Iterable[int]]): List of PIDs to kill.
		image_names (Optional[Iterable[str]]): List of image names to kill.
		modifiers (Optional[Iterable[TaskkillModifier]]): Command flags.
		system (Optional[str]): Remote system.
		username (Optional[str]): Remote username.
		password (Optional[str]): Remote password.

	Returns:
		List[str]: The constructed command list.
	"""
	
	clean_modifiers = deduplicate_list(modifiers)
	
	if clean_modifiers:
		map(
				lambda modifier: validate_parameter(
						value=modifier,
						value_name="modifier",
						available_values=AvailableTaskkillModifiers
				),
				clean_modifiers
		)
	
	cmd = ["taskkill"]
	
	if system:
		cmd.extend(["-S", system])
	
		if username:
			cmd.extend(["-U", username])
	
		if password:
			cmd.extend(["-P", password])
	
	if "force" in clean_modifiers:
		cmd.append("-F")
	
	if "tree" in clean_modifiers:
		cmd.append("-T")
	
	if pids:
		for pid in deduplicate_list(pids):
			cmd.extend(["-PID", str(pid)])
	
	if image_names:
		for image in deduplicate_list(image_names):
			cmd.extend(["-IM", image])
	
	return cmd


def run_taskkill(
		pids: Optional[Iterable[int]] = None,
		image_names: Optional[Iterable[str]] = None,
		modifiers: Optional[Iterable[TaskkillModifier]] = None,
		system: Optional[str] = None,
		username: Optional[str] = None,
		password: Optional[str] = None,
		encoding: str = "windows-1252",
) -> None:
	"""
	Executes the taskkill command.

	Args:
		pids (Optional[Iterable[int]]): PIDs to kill.
		image_names (Optional[Iterable[str]]): Images to kill.
		modifiers (Optional[Iterable[TaskkillModifier]]): Modifiers.
		system (Optional[str]): Remote system.
		username (Optional[str]): Username.
		password (Optional[str]): Password.
		encoding (str): Encoding.

	Raises:
		ValueError: If neither pids nor image_names are provided.
	"""
	
	if not pids and not image_names:
		raise ValueError("At least one PID or Image Name must be provided.")
	
	run_command(
			command_parts=build_taskkill(
					pids=pids,
					image_names=image_names,
					modifiers=modifiers,
					system=system,
					username=username,
					password=password,
			),
			encoding=encoding,
	)
