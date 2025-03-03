#!/usr/bin/env python3
import sys
import re
import os
from tqdm import tqdm

input_file: str = "sql"
output_folder: str = "output"

def read_file(filename: str):
	if not os.path.exists(f"{output_folder}/create"):
		os.makedirs(f"{output_folder}/create")
	if not os.path.exists(f"{output_folder}/insert"):
		os.makedirs(f"{output_folder}/insert")
	output_file = f"{output_folder}/head"
	try:
		with open(filename, 'r') as file:
			for line in tqdm(file):
				if line.startswith("--"): continue
				# INFO: this stuff usually fails @ php myadmin
				if line.startswith("/*"): continue
				if line.startswith("CREATE") or line.startswith("ALTER"):
					match = re.search(r"`([a-zA-Z_0-9]+)`", line)
					if match is None:
						print(f"error no match found on lime {line}")
						return
					table_name = match.group(1)
					output_file = f"{output_folder}/create/{table_name}.sql"
					# TODO: dependencies
				if line.startswith("INSERT INTO"):
					match = re.search(r"`([a-zA-Z_0-9]+)`", line)
					if match is None:
						print(f"error no match found on lime {line}")
						return
					table_name = match.group(1)
					output_file = f"{output_folder}/insert/{table_name}.sql"
				try: 
					with open(output_file, 'a') as output:
						output.write(line.strip() + '\n')
				except Exception as e:
					print(e)

	except FileNotFoundError:
		print(f"Error: File '{filename}' not found.")
	except Exception as e:
		print(f"Error: {e}")

def num_to_alphabetical(num):
	"""
	Utility function for file names might change
	"""
	# 0 = aaa, 1 = aab, 2 = aac, ..., 25 = aaz, 26 = aba, 27 = abb, ...
	first_char = chr((num // (26 * 26)) + 97)
	second_char = chr((num // 26 % 26) + 97)
	third_char = chr((num % 26) + 97)
	return f"{first_char}{second_char}{third_char}"

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python script.py <filename>")
	else:
		filename = sys.argv[1]
		read_file(filename)
