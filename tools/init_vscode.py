import json
import os
import re
import subprocess
import sys

from packaging.version import Version

def find_vswhere():
	program_files_x86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
	default_path = os.path.join(program_files_x86, "Microsoft Visual Studio", "Installer", "vswhere.exe")
	if os.path.isfile(default_path):
		return default_path
	else:
		print("vswhere.exe not found.")
		sys.exit(1)

def get_src_root_path():
	if os.path.exists("./src/"):
		return "."
	if os.path.exists("../src/"):
		return ".."
	print("Can't find source root directory.")
	sys.exit(1)

def get_latest_vs_path():
	vswhere = find_vswhere()
	try:
		command = [
			vswhere,
			"-latest",
			"-prerelease",
			"-products", "*",
			"-requires", "Microsoft.Component.MSBuild",
			"-property", "installationPath",
			"-nologo"
		]
		result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
		vs_path = result.stdout.strip()
		if not vs_path:
			print("No Visual Studio installation found.")
			sys.exit(1)
		return vs_path
	except subprocess.CalledProcessError as e:
		print("Error running vswhere:", e.stderr)
		sys.exit(1)

def find_latest_windows_sdk(sdk_base_path=r"C:/Program Files (x86)/Windows Kits/10/Include"):
	if not os.path.exists(sdk_base_path):
		print(f"Path does not exist: {sdk_base_path}")
		sys.exit(1)

	sdk_versions = []
	for entry in os.listdir(sdk_base_path):
		full_path = os.path.join(sdk_base_path, entry)
		if os.path.isdir(full_path) and re.match(r"10\.0\.\d+\.\d+", entry):
			try:
				sdk_versions.append(Version(entry))
			except Exception:
				pass

	if not sdk_versions:
		print("No valid 10.0.x.x SDK versions found.")
		sys.exit(1)

	latest_version = str(max(sdk_versions))
	return latest_version

if __name__ == "__main__":
	src_root_path = get_src_root_path()
	print(f"Source root: {src_root_path}")
	vs_path = get_latest_vs_path()
	vs_path_fwd = vs_path.replace("\\", "/")
	print(f"Latest Visual Studio path: {vs_path}")
	latest_win10_sdk = find_latest_windows_sdk()
	print(f"Latest Windows 10 SDK: {latest_win10_sdk}")
	c_cpp_properties_data = {
		"configurations": [
			{
				"name": "Win32",
				"includePath": [
					f"C:/Program Files (x86)/Windows Kits/10/Include/{latest_win10_sdk}/shared",
					f"C:/Program Files (x86)/Windows Kits/10/Include/{latest_win10_sdk}/ucrt",
					f"C:/Program Files (x86)/Windows Kits/10/Include/{latest_win10_sdk}/um",
					f"{vs_path_fwd}/VC/Tools/MSVC/*/atlmfc/include",
					f"{vs_path_fwd}/VC/Tools/MSVC/*/include"
				],
				"defines": [],
				"compilerPath": f"{vs_path_fwd}/VC/Tools/MSVC/*/bin/Hostx64/x64/cl.exe",
				"cStandard": "c17",
				"cppStandard": "c++23",
				"intelliSenseMode": "windows-msvc-x64"
			}
		],
		"version": 4
	}
	with open(f"{src_root_path}/.vscode/c_cpp_properties.json", "w", encoding="utf-8") as f:
		json.dump(c_cpp_properties_data, f, indent="\t")
