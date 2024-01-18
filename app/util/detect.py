import os
import json
import struct

def extension(file_path):
	'''
	Basic extension check.
	'''
	match os.path.splitext(file_path)[1]:
		case ".ckpt" | ".pth" | ".pt":
			return "Checkpoint"
		case ".lora":
			return "Lora"
		case ".lycoris":
			return "LyCORIS"
		case ".safetensors":
			return safetensor(file_path)
		case _:
			return "Unknown"

def safetensor(file_path):
	'''
	Opens safetensor file to analyze file type.
	Work in progress.
	'''
	with open(file_path, "rb") as fd:
		length_of_header = struct.unpack('<Q', fd.read(8))[0]
		header = json.loads(fd.read(length_of_header))

		if "__metadata__" in header:
			if "ss_network_module" in header["__metadata__"]:
				match header["__metadata__"]["ss_network_module"]:
					case "networks.lora":
						return "Lora"
					case "lycoris.kohya":
						return "LyCORIS"

	return "safetensor"