pyHTM - Hierarchical Temporal Memory in Python
=

*Note: [Numenta](http://www.numenta.com/) reserves certain patent rights. See Intellectual Property for details.*

Summary
-
This project is an unofficial implementation of the Cortical Learning Algorithms version of HTM, as described in v0.2 of the [writeup](http://www.numenta.com/htm-overview/education.php).  Ultimately, pyHTM will demonstrate learning and categorization of various sensory inputs, and display the results.

This implementation will favor code readability over optimization when those options are mutually exclusive.  If you want to understand what's going on, just dig into carver/htm_main.py and trace the code (using the Numenta paper as a reference).

The project is very young, and still remains unproven in terms of correctness.  I welcome bug reports, forks and pull requests.

Quickstart
-
#preferably inside a virtual environment
git clone git://github.com/carver/pyHTM.git
cd pyHTM
pip install -r requirements.txt
python src/htm_main.py 

Goals
-
* Near Term
  * Build diagnostic UI tools to show network state
  * Confirm correctness of algorithm (as defined by Numenta) <-- currently
* Medium Term
  * Build showcase of effectiveness on both trivial and real-world data
  * Serialize network state to disk to pause & continue
* Long Term
  * Build UI to configure and run HTM networks
  * Optimize for speed, never sacrificing code readability.
 

Status
-
Mar 23: New API for execution

 * htm.execute() split into two distinct options: execute and executeOnce
 * executeOnce takes a single data structure (2-d list of binary values) and runs a single cycle 
 * execute takes an iterable and runs executeOnce until the iterable runs out (or until the number of cycles specified by 'ticks') 

Feb 20: can have fewer columns than input pixels

 * Added new test to recognition_static
 * Input compression works at 3.5x; this is not a limit, just as high as I tested today
 * Specifically, a 14x14 grid of pixels, with a 4x4 network of columns, can recognize 4 distinct images 

Feb 18: Pass all tests again!

 * A mutable data bug was causing failure for recognition of 4 static images, fixed
 * Updated the htm.execute API to use a data generator instead of a function that mutates a data structure (what was I thinking?)
 * Next up: temporal recognition tests

Feb 1: Added test for recognition of 4 static images (does not yet pass all tests)
@see src/carver/tests/recognition_static.py
 
Intellectual Property
-
Numenta [encourages non-commercial experimentation](http://www.numenta.com/about-numenta/licensing.php): "Numenta promises that it will not assert its current patent rights against development or use of independent HTM systems, as long as such development or use is for research purposes only, and not for any commercial or production use."

In fact the license I'm using on this project is also non-commercial, so if you want a commercial license, you'll have to work it out with both Numenta and myself.

A section of this code, found in the numenta package, is a direct translation from the pseudocode in their writeup.  Despite pretty significant changes in the translation to python, I am assuming the Numenta copyright still holds (I only have a basic understanding of copyright law).  The rest of the implementation is in the carver.htm package, and is licensed under the Numenta Non-commercial License; see license.txt for details.
