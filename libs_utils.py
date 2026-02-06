# Colors for terminal output
from turtle import color
import subprocess
import re
import IPython.display as display


GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
STANDARD = "\033[0m"

def highlightDone(val):
	color = 'green' if val > 0.0 else 'red'
	return f'background-color: {color}'

# Get the prefix from the data_type running the bmnumbers cli applications
def getPrefix(data_type):
	prefixData = "0f"
	prefixCommand = ["bmnumbers", "-get-prefix", data_type]
	try:
		result = subprocess.run(prefixCommand, capture_output=True, text=True, check=True)
		prefixData = result.stdout.strip()
		return prefixData
	except subprocess.CalledProcessError as e:
		print("Error: bmnumbers command failed with error code "+str(e.returncode))
		return "0f"
	except FileNotFoundError:
		print("Error: bmnumbers command not found")
		return "0f"

def getDataSize(data_type):
	sizeCommand = ["bmnumbers", "-get-size", data_type]
	try:
		result = subprocess.run(sizeCommand, capture_output=True, text=True, check=True)
		sizeData = int(result.stdout.strip())
		return sizeData
	except subprocess.CalledProcessError as e:
		print("Error: bmnumbers command failed with error code "+str(e.returncode))
		return -1
	except FileNotFoundError:
		print("Error: bmnumbers command not found")
		return -1

# Convert to unsigned using bmnumbers
def convert_to_unsigned(token):
	convertCommand = ["bmnumbers", "-cast", "unsigned", token]
	try:
		result = subprocess.run(convertCommand, capture_output=True, text=True, check=True)
		convertedToken = result.stdout.strip()
		return convertedToken
	except subprocess.CalledProcessError as e:
		print("Error: bmnumbers command failed with error code "+str(e.returncode))
		return token
	except FileNotFoundError:
		print("Error: bmnumbers command not found")
		return token

def convert_from_unsigned(token,dataType,size):
	convertCommand = ["bmnumbers", "-cast", dataType, "0u<"+str(size)+">"+token]
	# print(convertCommand)
	try:
		result = subprocess.run(convertCommand, capture_output=True, text=True, check=True)
		convertedToken = result.stdout.strip()
		return convertedToken
	except subprocess.CalledProcessError as e:
		print("Error: bmnumbers command failed with error code "+str(e.returncode))
		return token
	except FileNotFoundError:
		print("Error: bmnumbers command not found")
		return token

# Sequencer and Desequencer
def csv2sequence(csvFile,seqFile,pref):
	with open(csvFile, 'r') as f:
		lines = f.readlines()
		with open(seqFile, 'w') as g:
			for line in lines:
				for token in line.split(','):
					if token.startswith(pref):
						token = token[len(pref):]
					token = token.strip()
					if token!="" and token!='\n':
						g.write(token+'\n')

def csv2sequenceunsigned(csvFile,seqFile,pref):
	with open(csvFile, 'r') as f:
		lines = f.readlines()
		with open(seqFile, 'w') as g:
			for line in lines:
				for token in line.split(','):
					token = token.strip()
					if token!="" and token!='\n':
						token = convert_to_unsigned(token)
						g.write(token+'\n')

def sequence2csv(seqFile,csvFile,dataWidth,pref):
	with open(seqFile, 'r') as f:
		lines = f.readlines()
		dataW = dataWidth
		with open(csvFile, 'w') as g:
			for line in lines:
				g.write(pref+line.strip())
				dataW -= 1
				if dataW==0:
					g.write('\n')
					dataW = dataWidth
				else:
					g.write(',')

def sequence2csvunsigned(seqFile,csvFile,dataWidth,dataType,benchcore):
	size=getDataSize(dataType)
	prefix=getPrefix(dataType)
	with open(seqFile, 'r') as f:
		lines = f.readlines()
		dataW = dataWidth
		with open(csvFile, 'w') as g:
			for line in lines:
				if dataW == 1 and benchcore:
					g.write(line.strip())
				else:
					dataEntry = convert_from_unsigned(line.strip(), dataType, size)
					dataEntry = dataEntry.removeprefix(prefix)
					g.write(dataEntry)
				dataW -= 1
				if dataW==0:
					g.write('\n')
					dataW = dataWidth
				else:
					g.write(',')

# Function to show the generated sympy expression
def showFunction(spExpr):
	exec(open("generated.py").read())
	display.display(spExpr)

# Function to show the generated BM
def showBM():
	display.Image("bondmachine.png")