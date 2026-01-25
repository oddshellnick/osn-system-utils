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
	"AvailableSSFamilies",
	"AvailableSSModes",
	"AvailableSSModifiers",
	"AvailableSSProtocols",
	"AvailableSSResolutions",
	"AvailableSSScopes",
	"SSFamily",
	"SSMode",
	"SSModifier",
	"SSProtocol",
	"SSResolution",
	"SSScope",
	"build_ss",
	"run_ss"
]

SSMode = Literal["list", "summary", "events"]
AvailableSSModes = ["list", "summary", "events"]

SSScope = Literal["established", "listening", "all"]
AvailableSSScopes = ["established", "listening", "all"]

SSResolution = Literal["default", "numeric", "resolve"]
AvailableSSResolutions = ["default", "numeric", "resolve"]

SSFamily = Literal["ipv4", "ipv6", "unix", "packet", "netlink", "vsock"]
AvailableSSFamilies = ["ipv4", "ipv6", "unix", "packet", "netlink", "vsock"]

SSProtocol = Literal["tcp", "udp", "dccp", "raw", "sctp"]
AvailableSSProtocols = ["tcp", "udp", "dccp", "raw", "sctp"]

SSModifier = Literal[
	"processes",
	"extended_info",
	"timer_info",
	"memory_usage",
	"internal_tcp_info",
	"selinux_context"
]
AvailableSSModifiers = [
	"processes",
	"extended_info",
	"timer_info",
	"memory_usage",
	"internal_tcp_info",
	"selinux_context"
]


def build_ss(
		mode: SSMode = "list",
		scope: SSScope = "established",
		resolution: SSResolution = "default",
		families: Optional[Iterable[SSFamily]] = None,
		protocols: Optional[Iterable[SSProtocol]] = None,
		modifiers: Optional[Iterable[SSModifier]] = None,
) -> List[str]:
	"""
	Builds the ss (socket statistics) command arguments.

	Args:
		mode (SSMode): The operational mode.
		scope (SSScope): The scope of sockets to display.
		resolution (SSResolution): Address resolution mode.
		families (Optional[Iterable[SSFamily]]): Address families to filter.
		protocols (Optional[Iterable[SSProtocol]]): Protocols to filter.
		modifiers (Optional[Iterable[SSModifier]]): Additional output modifiers.

	Returns:
		List[str]: The constructed command list.
	"""
	
	validate_parameter(value=mode, value_name="mode", available_values=AvailableSSModes)
	validate_parameter(value=scope, value_name="scope", available_values=AvailableSSScopes)
	validate_parameter(
			value=resolution,
			value_name="resolution",
			available_values=AvailableSSResolutions
	)
	
	clean_families = deduplicate_list(families)
	
	if clean_families:
		map(
				lambda family: validate_parameter(
						value=family,
						value_name="families",
						available_values=AvailableSSFamilies
				),
				clean_families
		)
	
	clean_protocols = deduplicate_list(protocols)
	
	if clean_protocols:
		map(
				lambda protocol: validate_parameter(
						value=protocol,
						value_name="protocols",
						available_values=AvailableSSProtocols
				),
				clean_protocols
		)
	
	clean_modifiers = deduplicate_list(modifiers)
	
	if clean_modifiers:
		map(
				lambda modifier: validate_parameter(
						value=modifier,
						value_name="modifier",
						available_values=AvailableSSModifiers
				),
				clean_modifiers
		)
	
	cmd = ["ss"]
	
	if mode == "summary":
		cmd.append("-s")
		return cmd
	elif mode == "events":
		cmd.append("-E")
	
	if scope == "listening":
		cmd.append("-l")
	elif scope == "all":
		cmd.append("-a")
	
	if resolution == "numeric":
		cmd.append("-n")
	elif resolution == "resolve":
		cmd.append("-r")
	
	if "ipv4" in clean_families:
		cmd.append("-4")
	
	if "ipv6" in clean_families:
		cmd.append("-6")
	
	if "unix" in clean_families:
		cmd.append("-x")
	
	if "packet" in clean_families:
		cmd.append("-0")
	
	if "netlink" in clean_families:
		cmd.append("--netlink")
	
	if "vsock" in clean_families:
		cmd.append("--vsock")
	
	if "tcp" in clean_protocols:
		cmd.append("-t")
	
	if "udp" in clean_protocols:
		cmd.append("-u")
	
	if "dccp" in clean_protocols:
		cmd.append("-d")
	
	if "raw" in clean_protocols:
		cmd.append("-w")
	
	if "sctp" in clean_protocols:
		cmd.append("-S")
	
	if "processes" in clean_modifiers:
		cmd.append("-p")
	
	if "extended_info" in clean_modifiers:
		cmd.append("-e")
	
	if "timer_info" in clean_modifiers:
		cmd.append("-o")
	
	if "memory_usage" in clean_modifiers:
		cmd.append("-m")
	
	if "internal_tcp_info" in clean_modifiers:
		cmd.append("-i")
	
	if "selinux_context" in clean_modifiers:
		cmd.append("-Z")
	
	return cmd


def run_ss(
		mode: SSMode = "list",
		scope: SSScope = "established",
		resolution: SSResolution = "default",
		families: Optional[Iterable[SSFamily]] = None,
		protocols: Optional[Iterable[SSProtocol]] = None,
		modifiers: Optional[Iterable[SSModifier]] = None,
		encoding: str = "utf-8",
) -> str:
	"""
	Executes the ss command.

	Args:
		mode (SSMode): Operational mode.
		scope (SSScope): Socket scope.
		resolution (SSResolution): Address resolution.
		families (Optional[Iterable[SSFamily]]): Address families.
		protocols (Optional[Iterable[SSProtocol]]): Protocols.
		modifiers (Optional[Iterable[SSModifier]]): Output modifiers.
		encoding (str): Output encoding.

	Returns:
		str: The command output.
	"""
	
	return run_command(
			command_parts=build_ss(
					mode=mode,
					scope=scope,
					resolution=resolution,
					families=families,
					protocols=protocols,
					modifiers=modifiers,
			),
			encoding=encoding,
	)
