#!/usr/bin/python

# MULTIFLIGHT CONTROLLER CONFIGURATION FILE

# You can define:
#  (1) start_time (string, "YYYYMMHHDD")
#      * can override with the commandline
#  (2) stop_time (string, "YYYYMMHHDD")
#      * defaults to None (i.e. never stop)
#  (3) task_list (list of task name strings, subset of tasks.all_tasks)
#      * defaults to tasks.all_tasks
#  (4) verbosity (string, output level) 
#      * 'NORMAL' (default)
#      * 'VERBOSE'  
#  (5) run_mode 
#      * 'real_models'
#      * 'dummy_realtime'  (downloader waits for earlier tasks to finish)
#      * 'dummy_catchup'   (downloader returns immediately) 

#verbosity = "VERBOSE"

#run_mode = 'real_models'    
run_mode = 'dummy_realtime'     
#run_mode = 'dummy_catchup'    

# start_time and stop_time must be strings
start_time = "2008080812"
stop_time = "2008081512"

# task_list should be a subset of tasks.all_tasks (defaults to all)
task_list = [ 
        'downloader',
        'nwpglobal',
        'globalprep',
        'globalwave',
        'nzlam',
        'nzlampost',
        'nzwave',
        'ricom',
        'nztide',
        'topnet',
        'mos' 
        ]
