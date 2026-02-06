# Colors for terminal output
from turtle import color
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
					if token.startswith(pref):
						token = token[len(pref):]
					token = token.strip()
					if token!="" and token!='\n':
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

# Function to show the generated sympy expression
def showFunction(spExpr):
	exec(open("generated.py").read())
	display.display(spExpr)

# Function to show the generated BM
def showBM():
	display.Image("bondmachine.png")