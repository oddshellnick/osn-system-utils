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


NetstatMode = Literal["default", "routing_table", "ethernet_stats", "protocol_stats"]
AvailableNetstatModes = ["default", "routing_table", "ethernet_stats", "protocol_stats"]

NetstatScope = Literal["active_only", "all", "all_and_bound"]
AvailableNetstatScopes = ["active_only", "all", "all_and_bound"]

NetstatAddress = Literal["default", "numeric", "fqdn"]
AvailableNetstatAddresses = ["default", "numeric", "fqdn"]

NetstatProtocol = Literal["TCP", "UDP", "TCPv6", "UDPv6", "ICMP", "ICMPv6", "IP", "IPv6"]
AvailableNetstatProtocols = ["TCP", "UDP", "TCPv6", "UDPv6", "ICMP", "ICMPv6", "IP", "IPv6", None]

NetstatModifier = Literal["pid", "exe", "offload_state", "network_direct", "tcp_template"]
AvailableNetstatModifiers = ["pid", "exe", "offload_state", "network_direct", "tcp_template"]


def build_netstat(
		mode: NetstatMode = "default",
		scope: NetstatScope = "active_only",
		address_display: NetstatAddress = "default",
		modifiers: Optional[Iterable[NetstatModifier]] = None,
		protocol: Optional[NetstatProtocol] = None,
		include_protocol_stats: bool = False,
) -> List[str]:
	"""
	Builds the netstat command arguments.

	Args:
		mode (NetstatMode): The operational mode.
		scope (NetstatScope): Scope of connections to show.
		address_display (NetstatAddress): How to display addresses.
		modifiers (Optional[Iterable[NetstatModifier]]): Output modifiers.
		protocol (Optional[NetstatProtocol]): Specific protocol to filter.
		include_protocol_stats (bool): Whether to include stats.

	Returns:
		List[str]: The constructed command list.
	"""
	
	validate_parameter(value=mode, value_name="mode", available_values=AvailableNetstatModes)
	validate_parameter(
			value=scope,
			value_name="scope",
			available_values=AvailableNetstatScopes
	)
	validate_parameter(
			value=address_display,
			value_name="address_display",
			available_values=AvailableNetstatAddresses
	)
	validate_parameter(
			value=protocol,
			value_name="protocol",
			available_values=AvailableNetstatProtocols
	)
	
	clean_modifiers = deduplicate_list(modifiers)
	
	if clean_modifiers:
		map(
				lambda modifier: validate_parameter(
						value=modifier,
						value_name="modifier",
						available_values=AvailableNetstatModifiers
				),
				clean_modifiers
		)
	
	cmd = ["netstat"]
	
	if mode == "routing_table":
		cmd.append("-r")
	
		if include_protocol_stats:
			cmd.append("-s")
	
		return cmd
	
	if mode == "ethernet_stats":
		cmd.append("-e")
	
		if include_protocol_stats:
			cmd.append("-s")
	
		return cmd
	
	if mode == "protocol_stats":
		cmd.append("-s")
	
		if protocol:
			cmd.extend(["-p", protocol])
	
		return cmd
	
	if scope == "all":
		cmd.append("-a")
	elif scope == "all_and_bound":
		cmd.append("-q")
	
	if address_display == "numeric":
		cmd.append("-n")
	elif address_display == "fqdn":
		cmd.append("-f")
	
	if "pid" in clean_modifiers:
		cmd.append("-o")
	
	if "exe" in clean_modifiers:
		cmd.append("-b")
	
	if "offload_state" in clean_modifiers:
		cmd.append("-t")
	
	if "network_direct" in clean_modifiers:
		cmd.append("-x")
	
	if "tcp_template" in clean_modifiers:
		cmd.append("-y")
	
	if protocol:
		cmd.extend(["-p", protocol])
	
	return cmd


def run_netstat(
		mode: NetstatMode = "default",
		scope: NetstatScope = "active_only",
		address_display: NetstatAddress = "default",
		modifiers: Optional[Iterable[NetstatModifier]] = None,
		protocol: Optional[NetstatProtocol] = None,
		include_protocol_stats: bool = False,
		encoding: str = "windows-1252",
) -> str:
	"""
	Executes the netstat command.

	Args:
		mode (NetstatMode): Operational mode.
		scope (NetstatScope): Scope.
		address_display (NetstatAddress): Address format.
		modifiers (Optional[Iterable[NetstatModifier]]): Modifiers.
		protocol (Optional[NetstatProtocol]): Protocol filter.
		include_protocol_stats (bool): Include statistics.
		encoding (str): Output encoding.

	Returns:
		str: The command output.
	"""
	
	return run_command(
			command_parts=build_netstat(
					mode=mode,
					scope=scope,
					address_display=address_display,
					modifiers=modifiers,
					protocol=protocol,
					include_protocol_stats=include_protocol_stats,
			),
			encoding=encoding,
	)
