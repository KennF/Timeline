#!/bin/bash

cur_dir=`pwd`
if [ "$PYTHONPATH" = "" ]; then
	export PYTHONPATH=$cur_dir
else 
	export PYTHONPATH=$PYTHONPATH:$cur_dir
fi
echo "PYTHONPATH is $PYTHONPATH"