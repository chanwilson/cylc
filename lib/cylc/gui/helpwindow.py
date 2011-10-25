#!/usr/bin/env python

#C: THIS FILE IS PART OF THE CYLC FORECAST SUITE METASCHEDULER.
#C: Copyright (C) 2008-2011 Hilary Oliver, NIWA
#C:
#C: This program is free software: you can redistribute it and/or modify
#C: it under the terms of the GNU General Public License as published by
#C: the Free Software Foundation, either version 3 of the License, or
#C: (at your option) any later version.
#C:
#C: This program is distributed in the hope that it will be useful,
#C: but WITHOUT ANY WARRANTY; without even the implied warranty of
#C: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#C: GNU General Public License for more details.
#C:
#C: You should have received a copy of the GNU General Public License
#C: along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import gtk
import pango
import string
from color_rotator import rotator

class helpwindow_base( object ):
    def __init__( self, title, height=400 ):
        self.window = gtk.Window()
        #window.set_border_width( 10 )
        self.window.set_title( title )

        self.window.set_size_request(600, int(height))

        sw = gtk.ScrolledWindow()
        sw.set_policy( gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC )

        vbox = gtk.VBox()
        quit_button = gtk.Button( "_Close" )
        quit_button.connect("clicked", lambda x: self.window.destroy() )
        vbox.pack_start( sw )
        vbox.pack_start( quit_button, False )

        textview = gtk.TextView()
        textview.set_border_width(5)
        textview.modify_base( gtk.STATE_NORMAL, gtk.gdk.color_parse( "#def" ))
        textview.set_editable( False )
        textview.set_wrap_mode( gtk.WRAP_WORD )
        sw.add( textview )
        self.window.add( vbox )
        self.tb = textview.get_buffer()

        self.tag_text = self.tb.create_tag( None, foreground = "#222" )
        self.tag_title = self.tb.create_tag( None, foreground = "#003" )
        self.tag_heading = self.tb.create_tag( None, foreground = "#008" )
        self.tag_subheading = self.tb.create_tag( None, foreground = "#00f" )
        self.tag_bold = self.tb.create_tag( None, weight = pango.WEIGHT_BOLD )

        self.add_main_heading( title )
        quit_button.grab_focus()
         
    def add_main_heading( self, text ):
        self.tb.insert_with_tags( self.tb.get_end_iter(), '\n' + text + '\n', self.tag_bold, self.tag_title )

    def add_heading( self, text ):
        self.tb.insert_with_tags( self.tb.get_end_iter(), '\n' + text, self.tag_bold, self.tag_heading )
 
    def add_subheading( self, text ):
        self.tb.insert_with_tags( self.tb.get_end_iter(), '\n    ' + text, self.tag_bold, self.tag_subheading )

    def add_text( self, text ):
        self.tb.insert_with_tags( self.tb.get_end_iter(), text + '\n', self.tag_text )
 
    def add_text_bold( self, text ):
        self.tb.insert_with_tags( self.tb.get_end_iter(), text, self.tag_text, self.tag_bold )

    def add_list_item( self, item ):
        self.tb.insert_with_tags( self.tb.get_end_iter(), '\n o ', self.tag_bold )
        self.tb.insert_with_tags( self.tb.get_end_iter(), item, self.tag_text )

    def show( self ):
        self.window.show_all()

class helpwindow( helpwindow_base ):
    def __init__( self, title, height, text ):
        helpwindow_base.__init__(self, title, height )
        self.parse( text )

    def parse( self, text ):
        def strip( line ):
            # strip '%' tags
            return re.sub( '%[\w\d]+ ', '', line )

        # pre-parse to concatenate paragraphs into a single string
        # because textbuffer inserts seem to add a newline that 
        # stop line wrapping from working properly...
        lines = []
        para = ''
        for line in string.split( text, '\n' ):
            if re.match( '^%', line ):
                # tag
                if para != '':
                    lines.append(para)
                    para = ''
                lines.append(line)
            elif re.match( '^\s*$', line ):
                # blank
                lines.append(line)
                if para != '':
                    lines.append(para)
                    para = ''
            else:
                para += ' ' + line
        if para != '':
            lines.append(para)

        for line in lines:
            if re.match( '^\s*$', line ):
                # blank line
                self.add_text( '' )
            elif re.match( '^%h1', line ):
                self.add_main_heading( strip(line) )
            elif re.match( '^%h2', line ):
                self.add_heading( strip(line) )
            elif re.match( '^%h3', line ):
                self.add_subheading( strip(line) )
            elif re.match( '^%b', line ):
                self.add_text_bold( strip(line ))
            elif re.match( '^%i', line ):
                self.add_list_item( strip(line ))
            else:
                self.add_text( line )

##########
def main( b ):
    help = helpwindow( "gcylc Main Window Help", 500, """%h2 Overview

When gcylc starts up it shows your private suite database. Using
the menu bar and right-click menu items you can register new suites;
copy, reregister, and unregister existing suites; start a suite control
application to run a dormant suite or connect to one that is already
running; edit, search, validate, and graph suite definitions; and import
suites from, or export them to, the central suite database (which is
seen by all users). You can also view, search, validate, and graph
suites in the central database when considering whether to import them
for your own use.

%h2 Menu Bar

%h3 File > New
Register another suite. This opens a file chooser dialog configured to
filter for cylc suite definition (suite.rc) files.

%h3 File > Exit
Quits the gcylc application, but not any external programs you have launched
from gcylc (such as suite edit sessions or suite control apps.

%h3 View > Filter
Change which suites are visible by searching on group and name match
patterns.

%h3 View > Expand
Expand the registration database treeview.

%h3 View > Collapse
Collapse the registration database treeview.

%h3 View > Refresh
Check the database for invalid registrations (e.g. due to manual
deletion of a suite definition directory) and update any suite
titles that have changed. Note that changes to the database itself
are automatically detected and updated by the GUI. Suite titles though,
while held in the database, are originally parsed from suite config
files. 

%h3 Database > Private
Switch to your private suite registration database.

%h3 Database > Central
Switch to the central suite registration database.


%h2 Right Click Menu Options

The Right-Click menu options available depend on whether you have
clicked on a running suite, a dormant suite, or a group of suites.  For
options relating to suite registration, registration groups are created
and deleted as required (you don't need to explicitly create group 'foo'
before registering a suite 'foo:bar', for example).

Most right-click menu items invoke cylc command line programs inside a
wrapper that captures subprocess stdout and stderr streams and displays
in a window that updates in real time. These output log windows can be
closed without affecting the associated subprocess, but you will lose
access to the output (except in the case of the stdout/stderr from cylc
itself for suites that are started from a suite control GUI - see below).

If you start a suite from the command line, what happens to cylc stdout
and stderr is of course entirely up to you (you may want to use
command line redirection and/or the posix nohup command).

%h3 Control (treeview) or Control (graph)

Launch a suite control GUI, with either the text treeview interface,
or the newer dependency graph based interface, to start a suite running,
or to connect to a suite that is already running. 

If you start the suite from within the control GUI, or if you connect to
a suite that was started from a control GUI, the GUI subprocess output
window will show cylc stdout and stderr as redirected to the files
$HOME/.cylc/GROUP:NAME.(out|err). If you start a suite from the
command line, where cylc stdout and stderr goes is up to you (use 
output redirection and/or the posix nohup command, for instance).

%h3 Submit A Task

Submit a single task from the suite, exactly as it would be submitted by
the suite.

%h3 View Cylc Output
This opens a new view of the suite stdout and stderr files
$HOME/.cylc/GROUP:NAME.(out|err) used when suites are started from
within gcylc (if you start a suite from the command line, where its
stdout and stderr end up is entirely up to you). This is available from
running tasks, and finished tasks while they remain in the suite (so
long as you don't stop and restart the suite).

%h3 View Cylc Log
This opens a searchable and filterable view of the log file that records,
timestamped, all important events as the suite runs.

%h3 Dump Suite State
(Running suites only) Print the current state of each task in the suite.

%h3 Describe
Print the suite description as parsed from the suite.rc file.

%h3 List Tasks
Print the suite's task list, parsed from the suite.rc file.

%h3 Edit
Edit the suite config (suite.rc) file

%h3 Graph
Plot the suite.rc dependency graph, or the most recent run time graph
(if the suite has run at least once before). The suite.rc graph will
update in real time as you edit the suite.

%h3 Search
Search in the suite config file and bin directory.

%h3 Validate
Parse the suite config file, validating it against the suite config
spec, then attempt to instantiate all suite task proxies, and report any
errors.

%h3 Copy
Copy an existing suite (or group of suites) and register it (or them)
for use.

%h3 Export
Export a suite (or group of suites) to the central database to make it
(or them) available to others.

%h3 Import
Import a suite (or group of suites) from the central database, to modify
and use yourself.

%h3 Reregister
Reregister an existing suite under a different GROUP:NAME, or reregister
a group of suites under a different GROUP:

%h3 Unregister
Delete the registration of a suite (or group of suites) and optionally 
delete its (or their) suite definition directory(s).""")
    help.show()

def filter( b ):
    help = helpwindow( "Filter Help", 300, """
Change suite visibility by filtering on group and/or name with
(Python-style) regular expressions (so, for example, the
wildcard is '.*' not '*' as in a shell glob expression).

Leaving a filter entry blank is equivalent to '.*' (i.e. match
anything).

Filter patterns have an implicit string start character ('^')
but no implicit string end character ('$'). Examples:

%i foo - matches 'foo' and 'foobar', but not 'barfoo'
%i foo$ - matches 'foo' only
%i .*foo$  - matches 'foo', 'barfoo', but not 'foobar'
%i (?i)foo - case-insensitive (matches 'foo', 'Food', 'FOOb',...)
%i (foo|bar) - match 'foo' or 'bar' followed by anything""")
    help.show()

def todo( b) :
    help = helpwindow( "Commands or command options not yet implemented in the GUI", 300, """
%h2 'cylc restart --no-release' option: don't release held tasks on restarting a suite.""")
    help.show()

def capture( b ):
    help = helpwindow( "Subprocess Capture Help", 200, """
This window captures stdout and stderr messages, in real time, from
subprocesses spawned by the gcylc GUI. You can close this window without
adversely affecting the subprocess itself, BUT [1] when the subprocess 
ends it will leave zombie entry in the system process table until you 
close gcylc (however, these are not real processes and do not
use system resources) and [2] you will lose access to the output streams
(except in the case of suites started from from gcylc, in which case the
output goes to special files that can be accessed again).""")
    help.show()

def graph_viewer( b ):
    help = helpwindow( "Graph Viewer Help", 500, """The graph viewer plots suite dependency graphs parsed from the suite.rc
file. The viewer updates automatically when the suite.rc file is saved
during editing (however, the [visualization] -> 'collapsed families' item
only affects the initial plot, after which any manual changes to family
node grouping, using the viewer controls, take precedence).

%h2 Controls

%i Center the graph: left-click on a node.
%i Pan: left-drag.
%i Zoom: Tool bar, mouse-wheel, Ctrl-left-drag, Shift-left-drag (box zoom).
%i Best Fit and Normal Size: Tool bar.

%h3 Family Grouping, Toolbar:
%i "group" - group all families up to root.
%i "ungroup" - recursively ungroup all families.

%h3 Family Grouping, Right-click menu:
%i "group" - close this node's parent family.
%i "ungroup" - open this family node.
%i "recursive ungroup" - ungroup all families below this node.""")
    help.show()


#-----------------------------------------------------------------------
# TO DO: THE FOLLOWING HELP WINDOWS SHOULD BE REDONE IN FORMATTED STRING 
# FORM, AS ABOVE.

def update_tb( tb, line, tags = None ):
    if tags:
        tb.insert_with_tags( tb.get_end_iter(), line, *tags )
    else:
        tb.insert( tb.get_end_iter(), line )

def userguide( w, graph=False ):
    window = gtk.Window()
    #window.set_border_width( 10 )
    #if readonly:
    #    window.set_title( "Cylc View Quick Guide" )
    #else:
    window.set_title( "Cylc Suite Control Quick Guide" )
    window.set_size_request(600, 600)

    sw = gtk.ScrolledWindow()
    sw.set_policy( gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC )

    vbox = gtk.VBox()
    quit_button = gtk.Button( "_Close" )
    quit_button.connect("clicked", lambda x: window.destroy() )
    vbox.pack_start( sw )
    vbox.pack_start( quit_button, False )

    textview = gtk.TextView()
    textview.set_border_width(5)
    textview.modify_bg( gtk.STATE_NORMAL, gtk.gdk.color_parse( "#fff" ))
    textview.set_editable( False )
    sw.add( textview )
    window.add( vbox )
    tb = textview.get_buffer()

    textview.set_wrap_mode( gtk.WRAP_WORD )

    blue = tb.create_tag( None, foreground = "blue" )
    red = tb.create_tag( None, foreground = "darkgreen" )
    alert = tb.create_tag( None, foreground = "red" )
    bold = tb.create_tag( None, weight = pango.WEIGHT_BOLD )

    #if readonly:
    #    update_tb( tb, "\n\nThis is 'cylc view', the read-only "
    #        "version of the 'cylc control' GUI: all of the suite control "
    #        "functionality documented below has been disabled.'\n\n", [bold, alert] )

    update_tb( tb, "Suite Control GUI Quick Guide", [bold, blue] )

    if not graph:
        update_tb( tb, "\n\nThis is a real time suite control "
            "and monitoring application for cylc, traditional interface. "
            "See 'cylc help' for the equivalent command line functionality." )

        update_tb( tb, "The upper 'light panel' "
            "provides a quick visual overview of the current state "
            "of the suite, with colours to indicate task state: "
            "blue=waiting, orange=submitted, green=running, "
            "gray=succeeded, red=failed, yellow=held. "
            "The lower panel is a cycle-time tree view "
            "with more detail on each task. You can filter on task state or task "
            "name to quickly find the tasks you're interested in. " )
        update_tb( tb, 
            "Right-click on tasks in the lower panel for task control "
            "and interrogation options.", [bold] )

    else:
        update_tb( tb, "\n\nThis is a real time suite control "
            "and monitoring application for cylc, using the new dependency "
            "graph interface. "
            "See 'cylc help' for the equivalent command line functionality. " )

        update_tb( tb, "Graph node colours indicate "
            "task state. The configured suite dependency "
            "graph, with off-white nodes, is used as a base for "
            "the displayed nodes. " )
        update_tb( tb,  "Left-click to center the graph on a "
            "node; left-drag to pan; Zoom buttons, mouse-wheel, or "
            "ctrl-left-drag to zoom in and out, and shift-left-drag to "
            "zoom in on a box. "
            "Right-click on nodes for task control "
            "and interrogation options. ", [bold] )
        update_tb( tb, 
            "NOTE that small changes in the task population as the suite evolves "
            "may cause large jumps in the graph layout, particularly for large "
            "complex suites, because the "
            "graphviz layout engine performs a global optimization "
            "each time the graph is plotted. The 'DIS|REconnect' "
            "toggle button is provided to freeze the action "
            "temporarily. The graph timezoom and tree-collapse " 
            "mechanism can also be used to focus on particular parts of "
            "a suite that you are interested in." )

    update_tb( tb, "\n\nMenu: File > ", [bold, red] )
    update_tb( tb, "\n o Exit: ", [bold])
    update_tb( tb, "Exit the control GUI (does not shut the suite down).")

    update_tb( tb, "\n\nMenu: View > ", [bold, red] )
    update_tb( tb, "\n o Nudge Suite: ", [bold])

    update_tb( tb, "Invoke the cylc task processing loop when nothing else "
            "is happening, in order to update estimated completion times "
            "(which are not yet shown in the graph-base GUI) and the "
            "\"state last updated at\" time in the status bar." )

    update_tb( tb, "\n o View Suite Log: ", [bold])
    update_tb( tb, "View the cylc log for this suite, updating the view "
            "in real time if the suite is running." )

    if graph:
        update_tb( tb, "\n o Expand All Subtrees ", [bold])
        update_tb( tb, "Expand any graph subtrees that you have "
                "collapsed via the right-click popup menu.")

        update_tb( tb, "\n o Time Range Focus ", [bold])
        update_tb( tb, "Restrict display to a specified range of cycle times.")

        update_tb( tb, "\n o Toggle Graph Key ", [bold])
        update_tb( tb, "Show or remove the dependency graph color key.")

        update_tb( tb, "\n o Toggle Crop Base Graph ", [bold])
        update_tb( tb, "This controls whether or not the suite base "
                "graph (off-white coloured nodes) is plotted for tasks "
                "that are not currently present in the suite. Not plotting "
                "them may result in several apparently disconnected "
                "graph sections, but plotting them may not be advantageous "
                "if there are tasks with widely separated cycle times "
                "present." )

    else:
        update_tb( tb, "\n o Toggle Task Names ", [bold])
        update_tb( tb, "Show or remove task names in the upper \"light panel\" display.")

        update_tb( tb, "\n o Toggle Auto-Expand Tree ", [bold])
        update_tb( tb, "If on, any cycle times containing submitted, running, or "
                "failed tasks will be automatically expanded whenever the suite "
                "state is updated.")

    update_tb( tb, "\n\nMenu: Control > ", [bold, red] )
    update_tb( tb, "\n o Run Suite: ", [bold])
    update_tb( tb, "Cold Start, Warm Start, Raw Start, or Restart the suite.")
    update_tb( tb, "\n o Stop Suite: ", [bold])
    update_tb( tb, "Shut down the suite when all currently running tasks have finished "
            "or immediately (beware of orphaned tasks!), or after a all tasks have "
            "passed a given cycle time, or after a particular wall clock time, or "
            "after a particular task has finished." )
    update_tb( tb, "\n o Hold Suite (pause): ", [bold])
    update_tb( tb, "Refrain from submitting tasks that are ready to run.")
    update_tb( tb, "\n o Release Suite (unpause): ", [bold])
    update_tb( tb, "Resume submitting tasks that are ready to run.")
    update_tb( tb, "\n o Insert Task(s): ", [bold])
    update_tb( tb, "Insert a task or task group into a running suite." )
    update_tb( tb, "\n o Block Access: ", [bold])
    update_tb( tb, "Refuse to comply with subsequent intervention commands." )
    update_tb( tb, "\n o Unblock Access: ", [bold])
    update_tb( tb, "Comply with subsequent intervention commands." )
    update_tb( tb, "\n o Change Runahead Limit: ", [bold])
    update_tb( tb, "Change the suite's configured runahead limit at "
            "run time." )

    if not graph:
        update_tb( tb, "\n\nTask Tree View Panel: Right-Click Popup Menu > ", [bold, red] )
    else:
        update_tb( tb, "\n\nGraph Node: Right-Click Popup Menu > ", [bold, red] )
            
        update_tb( tb, "\n o Collapse Subtree: ", [bold])
        update_tb( tb, "Collapse everything downstream of this task into a single node." )

        update_tb( tb, "\n o Focus On YYYYMMDDHH: ", [bold])
        update_tb( tb, "Restrict the graph to just the cycle time of this node (task)." )
 
        update_tb( tb, "\n o Focus On Range: ", [bold])
        update_tb( tb, "Restrict the graph to a specified range of cycle times." )

        update_tb( tb, "\n o Focus Reset: ", [bold])
        update_tb( tb, "Reset any cycle time focusing and show the whole graph." )
  
    update_tb( tb, "\n o View Job Script: ", [bold])
    update_tb( tb, "View the script used to submit this task to run." )
    update_tb( tb, "\n o View Output: ", [bold])
    update_tb( tb, "View task stdout and stderr logs in real time." )
    update_tb( tb, "\n o View State: ", [bold])
    update_tb( tb, "View the state of a task's prerequisites and outputs.")
    update_tb( tb, "\n o Trigger: ", [bold])
    update_tb( tb, "Reset the task to the 'ready' state (all prerequisites "
            "satisfied), thereby causing it to trigger immediately (NOTE: "
            "if the suite is held (paused) the task will trigger when "
            "the hold is released)." )
    update_tb( tb, "\n o Reset to 'waiting': ", [bold])
    update_tb( tb, "Set all of a task's prerequisites unsatisfied." )
    update_tb( tb, "\n o Reset to 'succeeded': ", [bold])
    update_tb( tb, "Set all of a task's outputs completed." )
    update_tb( tb, "\n o Reset to 'failed': ", [bold])
    update_tb( tb, "Put the task in the 'failed' state." )

    update_tb( tb, "\n o Hold: ", [bold])
    update_tb( tb, "Put a task in the 'held' state; "
            "it won't run or spawn until released." )

    update_tb( tb, "\n o Release: ", [bold])
    update_tb( tb, "Release a task from the 'held' state "
            "so that it can run again as normal." )

    update_tb( tb, "\n o Remove after spawning: ", [bold])
    update_tb( tb, "Remove a task from the suite after forcing it to "
            "spawn a successor if it has not done so already." )
    update_tb( tb, "\n o Remove without spawning: ", [bold])
    update_tb( tb, "Remove a task from the suite even if it has not "
            "yet spawned a successor (in which case it will be removed "
            "permanently unless re-inserted)." )
    update_tb( tb, "\n o Remove Tree (Recursive Purge): ", [bold])
    update_tb( tb, "Remove a task from the suite, then remove any task "
            "that would depend on it, then remove any tasks that would depend on "
            "those tasks, and so on, through to a given stop cycle." )

    update_tb( tb, "\n o Add A Prerequisite: ", [bold])
    update_tb( tb, "Here you can add a new prerequisite to a task at "
            "run time. Example of use: make a task wait on a one off task "
            "that it does not normally depend on but which has been "
            "inserted into the suite to handle some unusual situation.")


    window.show_all()

