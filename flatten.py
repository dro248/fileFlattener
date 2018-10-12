import os
import sys
import random
import string
import shutil
import argparse

class DirectoryFlattener:
	def flatten(self, fromDir, toDir):
		# Check that fromDir and toDir are valid files
		if not os.path.isdir(fromDir) or not os.path.isdir(toDir):
			print("Error: parameters must be directories.")
			return

		self.recursiveCopy(fromDir, toDir)

	def recursiveCopy(self, fromDir, toDir):
		# print("entered recursiveCopy:", fromDir, toDir)
		for item in os.listdir(fromDir):
			if os.path.isdir(os.path.join(fromDir, item)):
				# print("Item is directory")
				# print(item)
				self.recursiveCopy(os.path.join(fromDir, item), toDir)

			# else:
			elif os.path.isfile(os.path.join(fromDir,item)):
				# print("Item is a file")
				# print("\t", item)
				fileExt = os.path.splitext(item)[1]
				newfilename = self.generateRandomFilename(fileExt)

				# print("newFilename:", newfilename)

				# If for some reason we're getting fn collisions, keep generating new random fns
				# until we get on that doesn't exist.
				while os.path.isfile(newfilename):
					newfilename = self.generateRandomFilename(fileExt)

				# copy the item to the new location with the new randomly generated filename.
				shutil.copyfile(os.path.join(fromDir, item), os.path.join(toDir, newfilename))

	def generateRandomFilename(self, fileExt):
		prefix = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(20))
		return prefix + fileExt


def parse_options():
	parser = argparse.ArgumentParser(prog="flatten", description="flatten files", add_help=True)

	parser.add_argument("FROMDIR", help="Source Directory")
	parser.add_argument("TODIR", help="Destination Directory")
	return parser.parse_args()

if __name__ == "__main__":
	args = parse_options()
	FROMDIR = args.FROMDIR
	TODIR = args.TODIR

	df = DirectoryFlattener()

	for countryName in os.listdir(FROMDIR):
		print("Country Name:", countryName)

		# create a filename for the subfolder in FROMDIR
		fromdir_country = os.path.join(FROMDIR, countryName)

		# create a filename for the subfolder in TODIR (that we'll be creating)
		todir_country = os.path.join(TODIR, countryName)

		# Create a subfolder (todir_country) with this given name in TODIR
		os.makedirs(todir_country)
		df.flatten(fromdir_country, todir_country)


