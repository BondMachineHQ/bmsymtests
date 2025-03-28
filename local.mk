ROOTDIR=.
WORKING_DIR=working_dir
CURRENT_DIR=$(shell pwd)
SOURCE_FLEXPY=generated.py
FLEXPY_APP=working_dir/expression.c
FLEXPY_ARGS=--basm --build-app --app-file $(FLEXPY_APP) --emit-bmapi-maps --bmapi-maps-file bmapi.json --io-mode async --config-file flexpyconfig.json
FLEXPY_LIB=library
BOARD=zedboard
BASM_ARGS=-disable-dynamical-matching -chooser-min-word-size -chooser-force-same-name
MAPFILE=zedboard_maps.json
SHOWARGS=-dot-detail 5
SHOWRENDERER=dot -Tpng > bondmachine.png
include bmapi.mk
include deploy.mk
include simbatch.mk
include simulation.mk
