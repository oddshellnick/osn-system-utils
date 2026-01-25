import re
from typing import Any


__all__ = [
	"check_above",
	"check_between",
	"check_equal",
	"check_not_equal",
	"check_regex",
	"check_under",
	"get_nested_val"
]


def get_nested_val(value: Any, path: str) -> Any:
	"""
	Retrieves a value from a nested structure (dictionary or object) using a dot-notation path.

	Args:
		value (Any): The root object or dictionary.
		path (str): The dot-separated path to the attribute (e.g., "a.b.c").

	Returns:
		Any: The value found at the path, or None if not found.
	"""
	
	def get(val: Any, key: str) -> Any:
		if isinstance(val, dict):
			return val.get(key, None)
		
		return getattr(val, key, None)
	
	parts = path.split(".")
	current_value = get(val=value, key=parts[0])
	
	for part in parts[1:]:
		current_value = get(val=current_value, key=part)
	
		if current_value is None:
			break
	
	return current_value


def check_under(value: Any, attribute: str, limit: Any) -> bool:
	"""
	Checks if a nested attribute is strictly less than a limit.

	Args:
		value (Any): The object to check.
		attribute (str): The path to the attribute.
		limit (Any): The threshold value.

	Returns:
		bool: True if value < limit, False otherwise.
	"""
	
	val = get_nested_val(value=value, path=attribute)
	
	return val is not None and val < limit


def check_regex(value: Any, attribute: str, pattern: re.Pattern[str]) -> bool:
	"""
	Checks if a nested attribute matches a regex pattern.

	Args:
		value (Any): The object to check.
		attribute (str): The path to the attribute.
		pattern (re.Pattern[str]): The compiled regex pattern.

	Returns:
		bool: True if the pattern matches, False otherwise.
	"""
	
	val = get_nested_val(value=value, path=attribute)
	
	return bool(val and pattern.search(str(val)))


def check_not_equal(value: Any, attribute: str, target: Any) -> bool:
	"""
	Checks if a nested attribute is not equal to a target value.

	Args:
		value (Any): The object to check.
		attribute (str): The path to the attribute.
		target (Any): The target value.

	Returns:
		bool: True if value != target.
	"""
	
	val = get_nested_val(value=value, path=attribute)
	
	return val != target


def check_equal(value: Any, attribute: str, target: Any) -> bool:
	"""
	Checks if a nested attribute is equal to a target value.

	Args:
		value (Any): The object to check.
		attribute (str): The path to the attribute.
		target (Any): The target value.

	Returns:
		bool: True if value == target.
	"""
	
	val = get_nested_val(value=value, path=attribute)
	
	return val == target


def check_between(value: Any, attribute: str, min_: Any, max_: Any) -> bool:
	"""
	Checks if a nested attribute is within a range (inclusive).

	Args:
		value (Any): The object to check.
		attribute (str): The path to the attribute.
		min_ (Any): The minimum valid value.
		max_ (Any): The maximum valid value.

	Returns:
		bool: True if min_ <= value <= max_.
	"""
	
	val = get_nested_val(value, attribute)
	
	return val is not None and min_ <= val <= max_


def check_above(value: Any, attribute: str, limit: Any) -> bool:
	"""
	Checks if a nested attribute is strictly greater than a limit.

	Args:
		value (Any): The object to check.
		attribute (str): The path to the attribute.
		limit (Any): The threshold value.

	Returns:
		bool: True if value > limit, False otherwise.
	"""
	
	val = get_nested_val(value=value, path=attribute)
	
	return val is not None and val > limit
