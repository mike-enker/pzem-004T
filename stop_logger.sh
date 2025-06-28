#!/bin/bash

sudo ps ux | grep -E 'python.*run_pzem_logger\.py' | awk '{print $2}' | xargs -rt sudo kill -2
