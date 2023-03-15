#pset p1 1.0
#pset p2 3.1

set resultFile [open results.out w]
puts -nonewline $resultFile [format "%8g" $p1]
close $resultFile
