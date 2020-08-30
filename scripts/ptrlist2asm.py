#!/bin/python

import os, sys
from ast import literal_eval
sys.path.append(os.path.join(os.path.dirname(__file__), 'common'))
from common import utils

if __name__ == '__main__':
	input_file = sys.argv[1]
	output_file = sys.argv[2]
	version_suffix = sys.argv[3]

	prefix = "." + os.path.splitext(os.path.basename(input_file))[0]

	char_table = utils.merge_dicts([
		utils.read_table("scripts/res/tileset_MainSpecial.tbl", reverse=True), 
		utils.read_table("scripts/res/tileset_MainDialog.tbl", reverse=True), 
		utils.read_table("scripts/res/dakuten.tbl", reverse=True),
	])

	try:
		with open(input_file, 'r', encoding="utf-8") as i, open(output_file, 'w') as o:
			term,prefixlen = literal_eval(i.readline().strip())
			ptrs = []

			version_check = "[{}]".format(version_suffix)
			for n, line in enumerate(i):
				if not line.startswith("[") or line.startswith(version_check):
					line = line.replace(version_check,"") # Not the best way to do it, but it's good enough
					line = line.rstrip('\n')
					b = utils.txt2bin(line, char_table)
					if not (
						(len(b) == 1 and b[0] == term) or
						(len(b) == prefixlen)
					):
						b.append(term)
					ptrs.append(("{}_{:02X}".format(prefix, n),", ".join("${:02X}".format(x) for x in b)))
			o.write("".join("dw {}\n".format(ptr[0]) for ptr in ptrs))

			for ptr in ptrs:
				o.write("{}:\n".format(ptr[0]))
				o.write("  db {}\n".format(ptr[1]))
	except Exception as error:
		os.remove(output_file)
		raise error