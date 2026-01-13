import os
os.environ["PATH"]=os.environ["PATH"]+":/tools/Xilinx/Vivado/2023.2/bin"
os.environ["PATH"]=os.environ["PATH"]+":/home/mirko/.go/bin"
os.environ["PATH"]=os.environ["PATH"]+":/home/mirko/.cargo/bin"

debug=False
singleRun=False
runMode=False
singleRunPatch=False
fullRun=False
runSimbatchTests=False
runBmsimTests=False
storeBM=False

benchcore=False
showLatencyDistribution=False