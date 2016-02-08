############################################################################
#	Data Format Translator
#	Author: Damon Tolhurst
#	Date: 15-Nov-2012
#
#	This script can perform the following conversions:
#	1) binary <-> hex
#	2) binary <-> decimal
#	3) binary <-> ascii
#	4) hex <-> decimal
#	5) hex <-> ascii
#	6) decimal <-> ascii
#	7) invert binary bits
#	8) hex > binary > invert > hex
#
#	This script can be run in one of two formats:
#	1) As a standalone, user-friendly, prompt-based program
#	2) Individual functions can be called by another module that passes
#	   in necessary parameters
#	The source file is assumed to be in the same directory as the script,
#	and the destination file will be saved there as well. A destination
#	of '--s' can be used to print to screen instead of writing to a file.
#	A destination of '--tmp' can be used to cause individual methods to
#	return data, though the main method never returns anything.
############################################################################

import sys
import os
import re
import binascii
import time

# Main method that allows repeated conversion based on user input
# Parameters: (none)
# Returns: (none)
def main():
	quit = ''
	while not re.search('q', quit.lower()):
		os.system('cls')
		convert()
		quit = raw_input('\n\nPress ENTER to convert again or enter \'q\' to exit.')
		while quit <> 'q' and quit <> '':
			quit = raw_input('\n\n***Invalid entry. Press ENTER to convert again or enter \'q\' to exit. ')

# Conversion process that takes in parameters for conversion
# Parameters: (none)
# Returns: (none)
def convert():		

	# convert with one line of parameters in command prompt
	if len(sys.argv) == 5:
		from_what = sys.argv[1] # first parameter (after program name) is original data format
		to_what = sys.argv[2] # second parameter is the format to convert to
		src = sys.argv[3] # third parameter is where the data is coming from (source file)
		dst = sys.argv[4] # fourth parameter is where the data is being written to
		src_text = 0
	# convert in user-friendly format with prompts
	elif len(sys.argv) == 1:
		os.system('cls')
		
		# prompt format to convert from
		from_what = raw_input('Enter the original data format (hex, dec, bin, ascii).\n\n  Convert from: ').lower()
		if from_what == '--q': # quit
			sys.exit()
		while from_what <> 'hex' and from_what <> 'dec' and from_what <> 'bin' and from_what <> 'ascii':
			from_what = raw_input('\n***ERROR: Invalid format entered. Enter either \'hex\', \'dec\', \'bin\', or \'ascii.\'\n\n  Convert from: ').lower()
			if from_what == '--q': # quit
				sys.exit()
				
		# prompt format to convert to
		if from_what == 'hex' or from_what == 'bin':
			to_string = '\nEnter the format to convert to (hex, dec, bin, ascii, inv).\n\'inv\', if given binary input, will invert each bit.\nIf given hex input, \'inv\' will convert hex to binary, invert, and back to hex.\n\n  Convert to: '
		else:
			to_string = '\nEnter the format to convert to (hex, dec, bin, ascii).\n\n  Convert to: '
		to_what = raw_input(to_string).lower()
		if to_what == '--q': # quit
			sys.exit()
		while to_what <> 'hex' and to_what <> 'dec' and to_what <> 'bin' and to_what <> 'ascii' and to_what <> 'inv':
			to_what = raw_input('\n***ERROR: Invalid conversion method entered. Enter either \'hex\', \'dec\', \'bin\', \'ascii\', \'inv\', or \'invhex\'.\n\n  Convert to: ').lower()
			if to_what == '--q': # quit
				sys.exit()
				
		# check that data formats are different
		if from_what == to_what:
			print ('\n***ERROR: Cannot convert between %s and %s. Enter different data formats to convert.\n') % (from_what, to_what)
			return
		
		# can only invert binary or hex data
		elif to_what == 'in' and from_what <> 'bin' and from_what <> 'hex':
			print '\n***ERROR: Cannot invert %s format.***' % (from_what)
			return
		
		# prompt destination
		dst = raw_input('\n  Press ENTER to print to screen or type a file name to save: ')
		if dst == '': # default destination is screen
			dst = '--s'
		elif dst == '--S':
			dst = '--s'
		elif dst == '--q': # quit
			sys.exit()
			
		# prompt data to convert
		src_text = raw_input('\n  Enter data to convert: ')
		while src_text == '':
			src_text = raw_input('\n***No data entered to convert.\n\n  Enter data to convert: ')
		
		if re.search('\s', src_text) and from_what <> 'dec':
			keep_space = raw_input('\n***Spaces detected in input.\n   Would you like to preserve spaces in conversion? (yes/no) ')
			if 'n' in keep_space or 'N' in keep_space or '0' in keep_space:
				src_text = src_text.replace(' ', '')
			
		src = 0 # indicate that the source is user input rather than a file
	else:
		print '\nInvalid input format. Enter either 4 or 0 parameters after program name.\n  <program name> convertFrom convertTo sourceFile destination.'
		sys.exit(1)
		
	if dst == '': # blank destination gets a default name that matches the source file
		def_dst = ''
		x = -1
		# increment appended number as long as the file already exists
		if os.path.exists(src[:-4] + '.txt'):
			def_dst = src[:-4] + str(x) + '.txt'
			while os.path.exists(def_dst):
				x -= 1
				def_dst = src[:-4] + str(x) + '.txt'
		else:
			dst = src[:-4] + '.txt'
	elif dst <> '--s' and dst[-4:] <> '.txt': # add .txt extension if not given
		dst += '.txt'
		
	# check if destination file already exists, ask to overwrite if so
	overwrite = '1'
	if os.path.exists(dst):
		overwrite = raw_input('\n' + dst + ' already exists. Overwrite? (yes/no)  ')
	if not 'y' in overwrite and not 'Y' in overwrite and not '1' in overwrite:
		print '\n***Conversion operation aborted.***'
		return
	
	# check which function should be performed. Each function independently handles its own conversion
	# and appropriately writing out data.
	if from_what == 'hex' and to_what == 'bin': # convert hex to binary
		try:
			hex_to_bin(src, dst, src_text)
		except ValueError:
			print '\n***ERROR: \'%s\' may contain invalid hex data.\n          Only 0-9, a-f, and A-F allowed.' % (src_text)
	elif from_what == 'hex' and to_what == 'dec': # convert hex to decimal
		try:
			hex_to_dec(src, dst, src_text)
		except ValueError:
			print '\n***ERROR: \'%s\' may contain invalid hex data.\n          Only 0-9, a-f, and A-F allowed.' % (src_text)
	elif from_what == 'hex' and to_what == 'ascii': # convert hex to ascii
		try:
			hex_to_ascii(src, dst, src_text)
		except (ValueError, TypeError):
			print '\n***ERROR: \'%s\' may contain invalid hex data.\n          Only 0-9, a-f, and A-F allowed.' % (src_text)
	elif from_what == 'hex' and to_what == 'inv': # convert hex to binary, invert binary, convert back to hex
		try:
			invert_hex(src, dst, src_text)
		except ValueError:
			print '\n***ERROR: \'%s\' may contain invalid hex data.\n          Only 0-9, a-f, and A-F allowed.' % (src_text)
	elif from_what == 'bin' and to_what == 'hex': # convert binary to hex
		try:
			bin_to_hex(src, dst, src_text)
		except ValueError:
			print '\n***ERROR: \'%s\' may contain invalid binary data.\n       Only 0 and 1 allowed.' % (src_text)
	elif from_what == 'bin' and to_what == 'dec': # convert binary to decimal
		try:
			bin_to_dec(src, dst, src_text)
		except ValueError:
			print '\n***ERROR: \'%s\' may contain invalid binary data.\n       Only 0 and 1 allowed.' % (src_text)
	elif from_what == 'bin' and to_what == 'ascii': # convert binary to ascii
		try:
			bin_to_ascii(src, dst, src_text)
		except ValueError:
			print '\n***ERROR: \'%s\' may contain invalid binary data.\n       Only 0 and 1 allowed.' % (src_text)
	elif from_what == 'bin' and to_what == 'inv': # invert binary bits
		try:
			invert_bin(src, dst, src_text)
		except ValueError:
			print '\n***ERROR: \'%s\' may contain invalid binary data.\n       Only 0 and 1 allowed.' % (src_text)
	elif from_what == 'dec' and to_what == 'bin': # convert decimal to binary
		try:
			dec_to_bin(src, dst, src_text)
		except ValueError:
			print '\n***ERROR: \'%s\' may contain invalid decimal data.\n       Only 0-9 allowed.' % (src_text)
	elif from_what == 'dec' and to_what == 'hex': # convert decimal to hex
		try:
			dec_to_hex(src, dst, src_text)
		except ValueError:
			print '\n***ERROR: \'%s\' may contain invalid decimal data.\n       Only 0-9 allowed.' % (src_text)
	elif from_what == 'dec' and to_what == 'ascii': # convert decimal to ascii
		try:
			dec_to_ascii(src, dst, src_text)
		except ValueError:
			print '\n***ERROR: \'%s\' may contain invalid decimal data.\n       Only 0-9 allowed.' % (src_text)
	elif from_what == 'ascii' and to_what == 'hex': # convert ascii to hex
		try:
			ascii_to_hex(src, dst, src_text)
		except ValueError:
			print '\n***ERROR: \'%s\' may contain invalid ascii data.' % (src_text)
	elif from_what == 'ascii' and to_what == 'dec': # convert ascii to decimal
		try:
			ascii_to_dec(src, dst, src_text)
		except ValueError:
			print '\n***ERROR: \'%s\' may contain invalid ascii data.' % (src_text)
	elif from_what == 'ascii' and to_what == 'bin': # convert ascii to binary
		try:
			ascii_to_bin(src, dst, src_text)
		except ValueError:
			print '\n***ERROR: \'%s\' may contain invalid ascii data.' % (src_text)
	else: # no valid conversion method was given, print error
		print '\n***ERROR: Invalid conversion method entered.'

# Convert data from hex to binary. Spaces in input text are retained and used
# as delimiters between pieces to convert individually.
# Parameters:
#	src - string, represents source file to be converted
#	dst - string, represents destination to write converted data to
#	src_text - string, is the input data to convert
# Returns:
#	bin_text - string, is the converted binary data (only returns if dst = '--tmp')
def hex_to_bin(src, dst, src_text):
	try:
		# read in source text if not in standalone mode
		if not src_text:
			src_text = open(src, 'rU').read()
	except IOError, WindowsError:
		print '\n***ERROR: Couldn\'t open', src, 'while converting hex to binary.'
		sys.exit(1)
	else:
		# This if statement serves to make sure src_text is actually in hex format.
		# Strings coming from user input are just strings that can be converted. Strings
		# coming from a .INO record have formatting to represent them as hex.
		# If the data is coming from a record (i.e. src <> 0), hexlifying the text
		# will remove the formatting and leave a straight hex string to convert.
		if src <> 0 and not re.search('.txt', src):
			src_text = binascii.hexlify(src_text)
		else:
			# This Try blocks allows for correct handling of invalid input from either
			# a source file or user-entered input.
			# If source file is .txt, we don't know what format the data is in.
			# This will convert to hex if needed (by checking for an error when not).
			try:
				test = bin(int(src_text, 16))
			except ValueError, e:
				# The second value in this comparison is the interpreted string from the ValueError.
				# This will be the program's rendering of the source text in hex. If src_text is not
				# already in hex, this string will be longer, as each character is converted into at
				# least two characters, thus we know it's not in hex and needs to be hexlified.
				if len(src_text) < len(str(e)[41:-1]):
					src_text = binascii.hexlify(src_text)
			
		bin_text = ''
		
		# loop over whole source text to convert while there's data left to convert
		while re.search('\S', src_text):
			i = 0
			bin_word = ''
			# grab data until a space, indicating a 'word' to convert
			while i < len(src_text) and src_text[i] <> ' ':
				bin_word += src_text[i]
				i += 1
			# convert the 'word' to binary							    
			if bin_word: # bin_word will be null if the current character is a space. This only converts if bin_word has data to convert.
				bin_word = bin(int(bin_word, 16))[2:]
			
				# make sure binary data is in byte form
				while len(bin_word) % 8 <> 0:
					bin_word = '0' + bin_word
				bin_text += ' ' + bin_word
			
			# remove that part of source text that was just read in and converted
			if i >= len(src_text):
				break
			else:
				src_text = src_text[i+1:]
				
		# determine where to write converted data
		if dst == '--s':
			print '\n' + bin_text.replace('0b', '')[1:]
		elif dst == '--tmp':
			return bin_text.replace(' ', '')
		else:
			if dst <> 'origBin.txt':
				print '\n...Writing file...'
			f = open(dst, 'w')
			f.write(bin_text[1:])
			f.close()
			if dst <> 'origBin.txt':
				print '\nFile ' + dst + ' saved to ' + os.getcwd() + '.'
	
# Convert data from hex to decimal. Spaces in input text are retained and used
# as delimiters between pieces to convert individually.
# Parameters:
#	src - string, represents source file to be converted
#	dst - string, represents destination to write converted data to
#	src_text - string, is the input data to convert
# Returns:
#	dec_text - string, is the converted decimal data (only returns if dst = '--tmp')
def hex_to_dec(src, dst, src_text):
	try:
		# read in source text if not in standalone mode
		if not src_text:
			src_text = open(src, 'rU').read()
	except IOError, WindowsError:
		print '\n***ERROR: Couldn\'t open', src, 'while converting hex to decimal.'
		sys.exit(1)
	else:
		# If the data is coming from a file, make sure it's actually in hex format
		# by trying a conversion and convert to hex if there's an error.
		if src <> 0:
			try:
				tmp = str(int(src_text[:6], 16))
			except ValueError:
				src_text = binascii.hexlify(src_text)
		dec_text = ''
		# loop over whole source text to convert while there's non-whitespace left
		while re.search('\S', src_text):
			i = 0
			while src_text[i] == ' ':
				src_text = src_text[i+1:]
			dec_word = ''
			# grab data until a space, indicating a 'word' to convert
			while i < len(src_text) and src_text[i] <> ' ':
				dec_word += src_text[i]
				i += 1
			# convert source hex 'word' to decimal
			dec_text += ' ' + str(int(dec_word, 16))
			
			if i >= len(src_text):
				break
			else:
				src_text = src_text[i+1:]
		
		# determine where to write data
		if dst == '--s':
			print '\n' + dec_text[1:]
		elif dst == '--tmp':
			return dec_text[1:]
		else:
			print '\n...Writing file...'
			f = open(dst, 'w')
			f.write(dec_text[1:])
			f.close()
			print '\nFile ' + dst + ' saved to ' + os.getcwd() + '.'

# Convert data from hex to ascii. Spaces in input text are retained and used
# as delimiters between pieces to convert individually.
# Parameters:
#	src - string, represents source file to be converted
#	dst - string, represents destination to write converted data to
#	src_text - string, is the input data to convert
# Returns:
#	ascii_text - string, is the converted ascii data (only returns if dst = '--tmp')
def hex_to_ascii(src, dst, src_text):
	try:
		# read in source text if not in standalone mode
		if not src_text:
			src_file = open(src, 'rU')
			src_text = src_file.read()
			src_file.close()
	except IOError, WindowsError:
		print '\n***ERROR: Couldn\'t open', src, 'while converting hex to ascii.'
		sys.exit(1)
	else:
		# If the data is coming from a file, make sure it's actually in hex format
		# by trying a conversion and convert to hex if there's an error.
		if src <> 0:
			try:
				tmp = str(int(src_text[:6], 16))
			except ValueError:
				src_text = binascii.hexlify(src_text)
				
		ascii_text = ''
		src_text = src_text.replace('0x', '')
		if re.search('\s', src_text):
			spaces = True
		else:
			spaces = False
		if src:
			src_text = src_text.replace(' ', '')
		
		# loop over whole source text to convert while there's non-whitespace left
		while re.search('\S', src_text):
			i = 0
			ascii_word = ''
			# grab data until a space, indicating a 'word' to convert
			while i < len(src_text) and src_text[i] <> ' ':
				ascii_word += src_text[i]
				i += 1
			# convert source hex 'word' to ascii
			if ascii_word and len(ascii_word) % 2 == 0:
				try:
					ascii_text += ' ' + binascii.unhexlify(ascii_word)
				except ValueError:
					print '\n***ERROR: 0x%s is not a valid ascii character. Character skipped.' % (ascii_word)
			else:
				print '\n***ERROR: Input data must be an even number of characters. You may need to add leading zeros to the hex bytes.'
				return
			
			if i >= len(src_text):
				break
			else:
				src_text = src_text[i+1:]
		
		# determine where to write data
		if dst == '--s':
			if spaces:
				print '\nNOTE: Delimiting spaces from input are indistinguishable from converted spaces (0x20).'
			print '\n' + ascii_text[1:]
		elif dst == '--tmp':
			return ascii_text[1:]
		else:
			print '\n...Writing file...'
			f= open(dst, 'w')
			f.write(ascii_text[1:])
			f.close()
			print '\nFile ' + dst + ' saved to ' + os.getcwd() + '.'

# Convert data from binary to hex. Spaces in input text are retained and used
# as delimiters between pieces to convert individually.
# Parameters:
#	src - string, represents source file to be converted
#	dst - string, represents destination to write converted data to
# Returns:
#	hex_text - string, is the converted hex data (only returns if dst = '--tmp')
def bin_to_hex(src, dst, src_text):
	try:
		# read in source text if not in standalone mode
		if not src_text:
			src_text = open(src, 'rU').read()
	except IOError, WindowsError:
		print '\n***ERROR: Couldn\'t open', src, 'while converting binary to hex.'
		sys.exit(1)
	else:
		hex_text = ''
		# loop over whole source text to convert while there's non-whitespace left
		while re.search('\S', src_text):
			i = 0
			hex_word = ''
			# grab data until a space, indicating a 'word' to convert
			while i < len(src_text) and src_text[i] <> ' ':
				hex_word += src_text[i]
				i += 1
			# convert source binary 'word' to hex
			hex_word = hex(int(hex_word, 2))[2:]
			hex_word = hex_word.replace('L', '')
			
			# ensure each hex 'word' is at least 2 characters for future conversions
			##if len(hex_word) < 2:
			if len(hex_word) % 2 <> 0:
				hex_word = '0' + hex_word
			
			# add hex 'word' to the output text
			hex_text += ' ' + hex_word
			
			if i >= len(src_text):
				break
			else:
				src_text = src_text[i+1:]			
					
		# determine where to write data
		if dst == '--s':
			print '\n' + hex_text.upper()[1:]
		elif dst == '--tmp':
			return hex_text.upper()[1:]
		else:
			if dst <> '--tmp':
				print '\n...Writing file...'
			f = open(dst, 'w')
			f.write(hex_text.upper()[1:])
			f.close()
			if dst <> '--tmp':
				print '\nFile ' + dst + ' saved to ' + os.getcwd() + '.'

# Convert data from binary to decimal. Spaces in input text are retained and used
# as delimiters between pieces to convert individually.
# Parameters:
#	src - string, represents source file to be converted
#	dst - string, represents destination to write converted data to
#	src_text - string, is the input data to convert
# Returns:
#	dec_text - string, is the converted decimal data (only returns if dst = '--tmp')
def bin_to_dec(src, dst, src_text):
	try:
		# read in source text if not in standalone mode
		if not src_text:
			src_text = open(src, 'rU').read()
	except IOError, WindowsError:
		print '\n***ERROR: Couldn\'t open', src, 'while converting binary to decimal.'
		sys.exit(1)
	else:
		dec_text = ''
		# loop over whole source text to convert while there's non-whitespace left
		while re.search('\S', src_text):
			i = 0
			dec_word = ''
			# grab data until a space, indicating a 'word' to convert
			while src_text[i] <> ' ':
				dec_word += src_text[i]
				i += 1
				if i >= len(src_text):
					break
			# convert source binary 'word' to decimal
			dec_text += ' ' + str(int(dec_word,2))
			if i >= len(src_text):
				break
			else:
				src_text = src_text[i+1:]
		
		# determine where to write data
		if dst == '--s':
			print '\n' + dec_text[1:]
		elif dst == '--tmp':
			return dec_text[1:]
		else:
			print '\n...Writing file...'
			f = open(dst, 'w')
			f.write(dec_text[1:])
			f.close()
			print '\nFile ' + dst + ' saved to ' + os.getcwd() + '.'

# Convert data from binary to ascii. Spaces in input text are retained and used
# as delimiters between pieces to convert individually. Binary representations of
# space characters are translated as '_' since the visual space character is
# used in the output to separate converted pieces.
# Parameters:
#	src - string, represents source file to be converted
#	dst - string, represents destination to write converted data to
#	src_text - string, is the input data to convert
# Returns:
#	ascii_text - string, is the converted ascii data (only returns if dst = '--tmp')
def bin_to_ascii(src, dst, src_text):
	try:
		# read in source text if not in standalone mode
		if not src_text:
			src_text = open(src, 'rU').read()
	except IOError, WindowsError:
		print '\n***ERROR: Couldn\'t open', src, 'while converting binary to ascii.'
		sys.exit(1)
	else:
		ascii_text = ''
		#use_spaces = '0'
		add_zeros = '0'
		src_text = src_text.replace('0b', '')
		
		# loop over whole source text to convert while there's non-whitespace left
		while re.search('\S', src_text):
			i = 0
			ascii_word = ''
			
			while i < 8 and i < len(src_text) and src_text[i] <> ' ':
				ascii_word += src_text[i]
				i += 1
				
			if ascii_word:
				if len(ascii_word) <> 8 and add_zeros == '0':
					add_zeros = raw_input('\n***Input data does not divide evenly into bytes. Would you like to add leading \n   zeros? (y, n) ')
				
				if add_zeros:
					while len(ascii_word) % 8 <> 0:
						ascii_word = '0' + ascii_word
				
				ascii_text += chr(int(ascii_word, 2))
			
			if i < len(src_text) and src_text[i] == ' ':
				ascii_text += ' '
				i += 1

			if i >= len(src_text):
				break
			else:
				src_text = src_text[i:]
		
		# determine where to write data
		if dst == '--s':
			if re.search(' ', ascii_text):
				print '\nNOTE: Delimiting spaces from input are indistinguishable from converted spaces (0b100000).'
			print '\n' + ascii_text
		elif dst == '--tmp':
			return ascii_text[1:]
		else:
			print '\n...Writing file...'
			f = open(dst, 'w')
			f.write(ascii_text[1:])
			f.close()
			print '\nFile ' + dst + ' saved to ' + os.getcwd() + '.'
	
# Convert data from decimal to binary. Spaces in input text are retained and used
# as delimiters between pieces to convert individually.
# Parameters:
#	src - string, represents source file to be converted
#	dst - string, represents destination to write converted data to
#	src_text - string, is the input data to convert
# Returns:
#	bin_text - string, is the converted binary data (only returns if dst = '--tmp')
def dec_to_bin(src, dst, src_text):
	try:
		# read in source text if not in standalone mode
		if not src_text:
			src_text = open(src, 'rU').read()
	except IOError, WindowsError:
		print '\n***ERROR: Couldn\'t open', src, 'while converting decimal to binary.'
		sys.exit(1)
	else:
		bin_text = ''
		use_spaces = '0'
		if re.search('\s', src_text):
			use_spaces = raw_input('\n***Spaces detected in input.\n   Would you like to preserve spaces in conversion? (yes/no) ')
		# loop over whole source text to convert while there's non-whitespace left
		while re.search('\S', src_text):
			i = 0
			bin_word = ''
			# grab data until a space, indicating a 'word' to convert
			while i < len(src_text) and src_text[i] <> ' ':
				bin_word += src_text[i]
				i += 1
				
			if bin_word:
				# convert source decimal 'word' to binary
				bin_text += ' ' + bin(int(bin_word))[2:]

			if i >= len(src_text):
				break
			else:
				src_text = src_text[i+1:]
		
		# Decimal data can't be broken into bytes, so we need to leave the spaces until after converting.
		# Now we determine whether or not to remove spaces in output.
		if not re.search('Y', use_spaces.upper()):
			bin_text = bin_text.replace(' ', '')
		if bin_text[0] == ' ':
			bin_text = bin_text[1:]
		
		# determine where to write data
		if dst == '--s':
			print '\n' + bin_text
		elif dst == '--tmp':
			return bin_text
		else:
			print '\n...Writing file...'
			f = open(dst, 'w')
			f.write(bin_text)
			f.close()
			print '\nFile ' + dst + ' saved to ' + os.getcwd() + '.'

# Convert data from decimal to hex. Spaces in input text are retained and used
# as delimiters between pieces to convert individually.
# Parameters:
#	src - string, represents source file to be converted
#	dst - string, represents destination to write converted data to
#	src_text - string, is the input data to convert
# Returns:
#	hex_text - string, is the converted hex data (only returns if dst = '--tmp')
def dec_to_hex(src, dst, src_text):
	try:
		# read in source text if not in standalone mode
		if not src_text:
			src_text = open(src, 'rU').read()
	except IOError, WindowsError:
		print '\n***ERROR: Couldn\'t open', src, 'while converting decimal to hex.'
		sys.exit(1)
	else:
		hex_text = ''
		use_spaces = '0'
		if re.search('\s', src_text):
			use_spaces = raw_input('\n***Spaces detected in input.\n   Would you like to preserve spaces in conversion? (yes/no) ')
		# loop over whole source text to convert while there's non-whitespace left
		while re.search('\S', src_text):
			i = 0
			hex_word = ''
			# grab data until a space, indicating a 'word' to convert
			while i < len(src_text) and src_text[i] <> ' ':
				hex_word += src_text[i]
				i += 1
			
			if hex_word:
				# convert source decimal 'word' to hex
				hex_text += ' ' + hex(int(hex_word))[2:]
				hex_text = hex_text.replace('L', '')
				
			if i >= len(src_text):
				break
			else:
				src_text = src_text[i+1:]
		
		# Decimal data can't be broken into bytes, so we need to leave the spaces until after converting.
		# Now we determine whether or not to remove spaces in output.
		if not re.search('Y', use_spaces.upper()):
			hex_text = hex_text.replace(' ', '')
		if hex_text[0] == ' ':
			hex_text = hex_text[1:]
		
		# determine where to write data
		if dst == '--s':
			print '\n' + hex_text.upper()
		elif dst == '--tmp':
			return hex_text.uuper()
		else:
			print '\n...Writing file...'
			f = open(dst, 'w')
			f.write(hex_text.upper())
			f.close()
			print '\nFile ' + dst + ' saved to ' + os.getcwd() + '.'

# Convert data from decimal to ascii. Spaces in input text are retained and used
# as delimiters between pieces to convert individually. Decimal representations of
# space characters are translated as '_' since the visual space character is
# used in the output to separate converted pieces.
# Parameters:
#	src - string, represents source file to be converted
#	dst - string, represents destination to write converted data to
#	src_text - string, is the input data to convert
# Returns:
#	ascii_text - string, is the converted ascii data (only returns if dst = '--tmp')
def dec_to_ascii(src, dst, src_text):
	try:
		# read in source text if not in standalone mode
		if not src_text:
			src_text = open(src, 'rU').read()
	except IOError, WindowsError:
		print '\n***ERROR: Couldn\'t open', src, 'while converting decimal to ascii.'
		sys.exit(1)
	else:
		ascii_text = ''
		use_spaces = '0'
		if re.search('\s', src_text):
			use_spaces = raw_input('\n***Spaces detected in input.\n   Would you like to preserve spaces in conversion? (yes/no) ')
		if len(src_text) > 3 and not re.search('\s', src_text):
			print '\n***ERROR: Invalid input format. Enter decimal values delimited by spaces.'
			return
		# loop over whole source text to convert while there's non-whitespace left
		loop = 1
		while re.search('\S', src_text) or loop:
			i = 0
			ascii_word = ''
			# grab data until a space, indicating a 'word' to convert
			while i < len(src_text) and src_text[i] <> ' ':
				ascii_word += src_text[i]
				i += 1
			
			# convert source decimal 'word' to ascii
			if ascii_word:
				if int(ascii_word) > 255:
					print '\n***ERROR: Cannot convert integers greater than 255 to ASCII.'
					return
				if int(ascii_word) == 32:
					ascii_text += ' |~' # temporary placeholder for space character since it can be convused with delimiting spaces
				else:
					ascii_text += ' ' + chr(int(ascii_word))
				
			if i >= len(src_text):
				break
			else:
				src_text = src_text[i+1:]
			
			loop = 0
		
		# Decimal data can't be broken into bytes, so we need to leave the spaces until after converting.
		# Now we determine whether or not to remove spaces in output.
		if not re.search('Y', use_spaces.upper()):
			ascii_text = ascii_text.replace(' ', '')
		if ascii_text[0] == ' ':
			ascii_text = ascii_text[1:]
		ascii_text = ascii_text.replace('|~', ' ') # replace the space placeholder now that delimiting spaces have been removed
		
		# determine where to write data
		if dst == '--s':
			if re.search('Y', use_spaces.upper()):
				print '\nNOTE: Delimiting spaces from input are indistinguishable from converted spaces (32).'
			print '\n' + ascii_text
		elif dst == '-tmp':
			return ascii_text
		else:
			print '\n...Writing file...'
			f = open(dst, 'w')
			f.write(ascii_text)
			f.close()
			print '\nFile ' + dst + ' saved to ' + os.getcwd() + '.'

# Convert data from ascii to binary. Spaces in input text are not retained since they
# represent an ascii character, and they are converted to'00100000'. Output prints each
# character one after another without delimiter based on input.
# Parameters:
#	src - string, represents source file to be converted
#	dst - string, represents destination to write converted data to
#	src_text - string, is the input data to convert
# Returns:
#	bin_text - string, is the converted binary data (only returns if dst = '--tmp')
def ascii_to_bin(src, dst, src_text):
	try:
		# read in source text if not in standalone mode
		if not src_text:
			src_text = open(src, 'rU').read()
	except IOError, WindowsError:
		print '\n***ERROR: Couldn\'t open', src, 'while converting ascii to binary.'
		sys.exit(1)
	else:
		i = 0
		bin_text = ''
		# loop over whole source text and convert each ascii character to 8-bit binary
		# space characters in src_text are left intact and converted to '00100000'.
		while i < len(src_text):
			bin_word = bin(ord(src_text[i]))[2:]
			while len(bin_word) < 8:
				bin_word = '0' + bin_word
			bin_text += ' ' + bin_word
			i += 1
			
		# determine where to write data
		if dst == '--s':
			print '\n(Spaces entered above are represented as \'00100000\'.\n' + bin_text[1:]
		elif dst == '--tmp':
			return bin_text[1:]
		else:
			print '\n...Writing file...'
			f = open(dst, 'w')
			f.write(bin_text[1:])
			f.close()
			print '\nFile ' + dst + ' saved to ' + os.getcwd() + '.'
	
# Convert data from ascii to decimal. Spaces in input text are not retained since they
# represent an ascii character, and they are converted to'35'. Output prints each
# character one after another without delimiter based on input.
# Parameters:
#	src - string, represents source file to be converted
#	dst - string, represents destination to write converted data to
#	src_text - string, is the input data to convert
# Returns:
#	dec_text - string, is the converted decimal data (only returns if dst = '--tmp')

def ascii_to_dec(src, dst, src_text):
	try:
		# read in source text if not in standalone mode
		if not src_text:
			src_text = open(src, 'rU').read()
	except IOError, WindowsError:
		print '\n***ERROR: Couldn\'t open', src, 'while converting ascii to decimal.'
		sys.exit(1)
	else:
		dec_text = ''
		# loop over whole source text and convert each ascii character to decimal
		# space characters in src_text are left intact and converted to '32'.
		i = 0
		while i < len(src_text):
			dec_text += ' ' + str(ord(src_text[i]))
			i += 1
		
		# determine where to write data
		if dst == '--s':
			print '\nSpaces entered above are represented as \'32\'.\n' + dec_text[1:]
		elif dst == '--tmp':
			return dec_text[1:]
		else:
			print '\n...Writing file...'
			f = open(dst, 'w')
			f.write(dec_text[1:])
			f.close()
			print '\nFile ' + dst + ' saved to ' + os.getcwd() + '.'

# Convert data from ascii to hex. Spaces in input text are not retained since they
# represent an ascii character, and they are converted to'20'. Output prints each
# character one after another without delimiter based on input.
# Parameters:
#	src - string, represents source file to be converted
#	dst - string, represents destination to write converted data to
#	src_text - string, is the input data to convert
# Returns:
#	hex_text - string, is the converted hex data (only returns if dst = '--tmp')
def ascii_to_hex(src, dst, src_text):
	try:
		# read in source text if not in standalone mode
		if not src_text:
			src_text = open(src, 'rU').read()
	except IOError, WindowsError:
		print '***ERROR: Couldn\'t open', src, 'while converting ascii to hex.'
		sys.exit(1)
	else:
		hex_text = ''
		# loop over whole source text and convert each ascii character to hex
		# space characters in src_text are left intact and converted to '20'.
		i = 0
		while i < len(src_text):
			hex_word = str(hex(ord(src_text[i])))[2:]
			while len(hex_word) < 2:
				hex_word = '0' + hex_word
			hex_text += ' ' + hex_word
			i += 1
			
		# determine where to write data
		if dst == '--s':
			print '\n(Each ASCII character above is separated by a space below. \'20\' indicates a space character in input.)\n' + hex_text.upper()[1:]
		elif dst == '--tmp':
			return hex_text.upper()[1:]
		else:
			print '\n...Writing file...'
			f = open(dst, 'w')
			f.write(hex_text.upper()[1:])
			f.close()
			print '\nFile ' + dst + ' saved to ' + os.getcwd() + '.'

# Convert hex to binary, invert the bits, convert back to hex
# Parameters:
#	src - string, represents source file to be converted
#	dst - string, represents destination to write converted data to
# Returns:
#	inverted_hex, string of inverted and converted data
def invert_hex(src, dst, src_text):
	# creates two intermediate files and then deletes them
	hex_to_bin(src, 'origBin.txt', src_text)
	invert_bin('origBin.txt', 'invBin.txt', 0)
	inverted_hex = bin_to_hex('invBin.txt', dst, 0)
	os.remove('origBin.txt')
	os.remove('invBin.txt')
	return inverted_hex

# Invert binary string
# Parameters:
#	src - Source file with data to convert
#	dst - Destination file to save final data to
# Returns:
#	inv_bits - string, inverted input bits (only if dst = '--tmp')
def invert_bin(src, dst, src_text):
	try:
		if not src_text:
			s = open(src,'rU')
			src_text = s.read()
			s.close()
	except IOError, WindowsError:
		print '***ERROR: Couldn\'t open', src, 'while inverting binary.'
		sys.exit(1)
	else:		
		# add a leading zero if the input string is not an even number of bits
		src_bits = len(src_text)
		while len(src_text.replace(' ', '')) %8 <> 0:
			src_text = '0' + src_text
			
		# print to screen or write to file
		inv_bits = ""
		
		# save inverted bits to temporary string
		for i in src_text:
			if i == '1':
				inv_bits += '0'
			elif i == '0':
				inv_bits += '1'
			elif i == ' ':
				inv_bits += ' '
			else: # source file containined non-binary bits, error
				print "\n***Error in inversion: Invalid binary file..."
				sys.exit(1)
				
		# print, return, or write inverted string
		if dst == '--s':
			print '\nAs entered: ' + inv_bits[-src_bits:] # print string of inverted bits
			print '\nBy bytes: ' + inv_bits
		elif dst == '--tmp':
			return inv_bits # return string of inverted bits
		else:
			if re.search('.txt', dst):
				d = open(dst, 'w')
			else:
				d = open(dst + '.txt', 'w')
			
			# only print writing status if not being called internally from invert_hex
			if not (src == 'origBin.txt' and dst == 'invBin.txt'):
				print '\n...Writing file...'
			
			# write inverted bits to file
			d.write(inv_bits)
					
			d.close()
			# only print saved status if not being called internally from invert_hex
			if not (src == 'origBin.txt' and dst == 'invBin.txt'):
				print '\nFile ' + dst + ' saved to ' + os.getcwd() + '.'
				

if __name__ == '__main__':
  main()