import pathlib
from typing import List

from setuptools import find_packages, setup


def get_long_description() -> str:
	long_description_path = pathlib.Path("README.md")
	
	if long_description_path.is_file():
		return long_description_path.read_text(encoding="utf-8")

	raise FileNotFoundError("README.md not found")


def get_install_requires() -> List[str]:
	requirement_path = pathlib.Path("requirements.txt")
	
	if requirement_path.is_file():
		return requirement_path.read_text(encoding="utf-8").splitlines()

	raise FileNotFoundError("requirements.txt not found")


def get_description() -> str:
	description_path = pathlib.Path("description.txt")
	
	if description_path.is_file():
		return description_path.read_text(encoding="utf-8")

	raise FileNotFoundError("description.txt not found")


setup(
		name="osn-system-utils",
		version="0.0.4",
		author="oddshellnick",
		author_email="oddshellnick.programming@gmail.com",
		description=get_description(),
		long_description=get_long_description(),
		long_description_content_type="text/markdown",
		packages=find_packages(exclude=["unit_tests*"]),
		install_requires=get_install_requires(),
		include_package_data=True,
)
