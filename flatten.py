import os
import sys
import random
import string
import shutil
import argparse

print(sys.argv)

if(len(sys.argv) < 3):
	print("Not enough args")
	print("usage: python3 flatten.py FROMDIR TODIR")
	sys.exit()

FROMDIR = sys.argv[1]
TODIR = sys.argv[2]


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


df = DirectoryFlattener()

# df.flatten(FROMDIR, TODIR)

for countryName in os.listdir(FROMDIR):
	print("Country Name:", countryName)

	# create a filename for the subfolder in FROMDIR
	fromdir_country = os.path.join(FROMDIR, countryName)

	# create a filename for the subfolder in TODIR (that we'll be creating)
	todir_country = os.path.join(TODIR, countryName)

	# Create a subfolder (todir_country) with this given name in TODIR
	os.makedirs(todir_country)
	df.flatten(fromdir_country, todir_country)