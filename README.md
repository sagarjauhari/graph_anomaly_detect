graph_anomaly_detect
====================

Anomaly detection in time series graphs


### Local Configuration
After cloning the repo on your local machine, add a file named 'dev_settings.py' in your repo which has the following contents:
<pre>
DATA_URL="<path to your data folder>"
SAVE_URL="<path to your output folder>"
</pre>

The path mentioned in 'DATA_URL' should contain all the unzipped data in 4 folders: 
<pre>
as-733  enron  p2p-Gnutella  reality_mining_voices
<pre>
