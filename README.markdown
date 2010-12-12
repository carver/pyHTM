pyHTM - Hierarchical Temporal Memory in Python
=

*Note: [Numenta](http://www.numenta.com/) reserves certain patent rights, despite this project being licensed LGPL. See Intellectual Property for details.*

Summary
-
This project is an unofficial implementation of the Cortical Learning Algorithms version of HTM, as described in v0.1.1 of the [writeup](http://www.numenta.com/htm-overview/education.php).  Ultimately, pyHTM will demonstrate learning and categorization of various sensory inputs, and display the results.

This implementation will favor code readability over optimization when those options are mutually exclusive.  If you want to understand what's going on, just dig into carver/htm_main.py and trace the code (using the Numenta paper as a reference).

The project is very young, and still remains unproven in terms of correctness.  I welcome bug reports, forks and pull requests.

Goals
-
* Near Term
  * Build diagnostic UI tools to show network state
  * Confirm correctness of algorithm (as defined by Numenta)
* Medium Term
  * Build showcase of effectiveness on both trivial and real-world data
  * Serialize network state to disk to pause & continue
* Long Term
  * Build UI to configure and run HTM networks
  * Optimize for speed, never sacrificing code readability.
 

Status
-
Dec 10: The most basic correctness tests are passing!

 * the same columns light up on the same input data
 * particular cells within the column become active after learning temporal patterns
 
Intellectual Property
-
Numenta [encourages non-commercial experimentation](http://www.numenta.com/about-numenta/licensing.php): "Numenta promises that it will not assert its current patent rights against development or use of independent HTM systems, as long as such development or use is for research purposes only, and not for any commercial or production use."  You should contact them if you want a commercial license.

A section of this code, found in the numenta package, is a direct translation from the pseudocode in their writeup.  Despite pretty significant changes in the translation to python, I am assuming the Numenta copyright still holds (I only have a basic understanding of copyright law).  The rest of the implementation is in the carver.htm package, and is licensed LGPL; see carver-license.txt for my interpretation of what constitutes library usage.
