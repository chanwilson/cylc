#!/usr/bin/python

# A program that masquerade's as a given tasks by reporting its outputs
# completed on time according to the controller's dummy clock.

import Pyro.naming, Pyro.core
from Pyro.errors import NamingError
import reference_time
import datetime
import sys
import os
import re
from time import sleep

class dummy_task:

    def __init__( self, task_name, ref_time ):

        # get a pyro proxy for the task object that I'm masquerading as
        self.name = task_name
        self.ref_time = ref_time
        self.task = Pyro.core.getProxyForURI('PYRONAME://' + system_name + '.' + self.name + '%' + self.ref_time )
        
        # get a pyro proxy for the dummy clock
        self.clock = Pyro.core.getProxyForURI('PYRONAME://' + system_name + '.dummy_clock' )


    def run( self ):

        # get a list of output messages to fake: outputs[ time ] = output
        outputs = self.task.get_timed_postrequisites()

        # ordered list of times
        times = outputs.keys()
        times.sort()

        # task-specific delay
        self.delay()

        # time to stop counting and generate the output
        # [ 0, 28, 30 ] dummy minutes
        prev_time = times[0]
        for time in times:
            # wait until the stop time for each output, and then generate the output
            diff_hrs = ( time - prev_time )/60.0
            dt_diff = datetime.timedelta( 0,0,0,0,0,diff_hrs,0 )
            dt_diff_sec = dt_diff.seconds
            dt_diff_sec_real = dt_diff_sec * dummy_clock_rate / 60.0 / 60.0 
            sleep( dt_diff_sec_real )

            self.task.incoming( "NORMAL", outputs[ time ] )

            prev_time = time
            
    def delay( self ):

        real_time_delay = self.task.get_real_time_delay()
        if real_time_delay == None:
            # not a contact task
            return

        rt = reference_time._rt_to_dt( self.ref_time )
        delayed_start = rt + datetime.timedelta( 0,0,0,0,0,real_time_delay,0 ) 
        current_time = self.clock.get_datetime()

        if current_time >= delayed_start:
            # already past the delayed start time
            self.task.incoming( 'NORMAL', 'CATCHINGUP: external event already occurred' )
        else:
            # sleep until the delayed start time
            self.task.incoming( 'NORMAL', 'CAUGHTUP: waiting on external event' )
            diff_real_secs = (delayed_start - current_time).seconds * dummy_clock_rate / ( 60. * 60.)
            sleep( diff_real_secs )


#----------------------------------------------------------------------
if __name__ == '__main__':
    task_name = os.environ['TASK_NAME']
    ref_time = os.environ['REFERENCE_TIME']
    system_name = os.environ['SYSTEM_NAME'] 
    dummy_clock_rate = int( os.environ['CLOCK_RATE'] )
    dummy_clock_offset = os.environ['CLOCK_OFFSET']
        
    #print "DUMMY TASK STARTING: " + task_name + " " + ref_time
    dummy = dummy_task( task_name, ref_time )
    dummy.run()
    #print "DUMMY TASK FINISHED: " + task_name + " " + ref_time
