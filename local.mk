ROOTDIR=.
WORKING_DIR=working_dir
CURRENT_DIR=$(shell pwd)
FLEXPY_APP=working_dir/expression.c
FLEXPY_ARGS=--basm --build-app --app-file $(FLEXPY_APP) --emit-bmapi-maps --bmapi-maps-file bmapi.json --io-mode sync --config-file flexpyconfig.json --neuron-statistics statistics.json
FLEXPY_LIB=library
BOARD=zedboard
BASM_ARGS=-disable-dynamical-matching -chooser-min-word-size -chooser-force-same-name
BASM_LIB_FILES=library/*basm
MAPFILE=zedboard_maps.json
SHOWARGS=-dot-detail 5
SHOWRENDERER=dot -Tpng > bondmachine.png
EXTRACLEAN=*.csv *.seq num_outputs.txt bmapi.json bondmachine.png statistics.json zedboard* source.mk out.basm
include bmapi.mk
include deploy.mk
include simbatch.mk
include simulation.mk
include source.mk