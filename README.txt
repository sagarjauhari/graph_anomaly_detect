(a) Software that needs to be installed (if any) with URL’s to download it from 
and instructions on how to install them.
Python 2.7: http://www.python.org/download/releases/2.7/
IGraph Python Module: http://igraph.sourceforge.net/
Numpy: http://www.numpy.org/
Scipy: http://www.scipy.org/


(b) Environment variable settings (if any) and OS it should/could run on.
The program has been tested on Ubuntu 13.10 (64bit)


(c) Instructions on how to run the program (and the script to change the output 
format, if included).

STEP 1
------
Set the 2 URLs in dev_settings.py:
DATA_URL="<path to datasets>"
SAVE_URL="<path where results will be saved>"

The contents of the folder pointed by DATA_URL should be as follows:
$ ls /media/media/DATA/gdm_p2/
as-733  enron   p2p-Gnutella  reality_mining_voices

STEP 2
------
$ cd <path to project directory>
$ ls
dev_settings.py  netsimile.py  out  png  profiler  README.md  README.txt  
report.md  util.py

$ python netsimile.py reality_mining_voices
$ python netsimile.py enron
$ python netsimile.py as-733
$ python netsimile.py p2p-Gnutella


(d) Instructions on how to interpret the results.
The results are generated in the folder pointed by SAVE_URL in dev_settings.py

$ ls <path to SAVE_URL>
as-733_anomalies.txt  p2p-Gnutella_anomalies.txt
as-733_dists.csv      p2p-Gnutella_dists.csv
enron_anomalies.txt   reality_mining_voices_anomalies.txt
enron_dists.csv       reality_mining_voices_dists.csv

The CSV files are the distance files. 
The TXT files are the anomaly files in the required format.

(e) Sample input and output ﬁles.
INPUT: Time series datasets given to us by TA
OUTPUT:
$ cat as-733_anomalies.txt 
5.88616099352 NaN
189 6.05701204772 6.13549877515
588 14.3684041483 14.3416357864
620 14.1817815211 14.219906334
637 27.2965956181 27.295211961
638 27.295211961 15.6105245379
639 15.6105245379 15.6507282621
694 13.1443321866 16.7713801145
695 16.7713801145 16.8246712096


(f) Citations to any software you may have used or any dataset you may have 
tested your code on.
