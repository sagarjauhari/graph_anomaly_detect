##Anomaly detection in time evolving graphs
Finding anomalies in graphs using NetSimile[1] algorithm

### Local Configuration
After cloning the repo on your local machine, add a file named 'dev_settings.py' in your repo which has the following contents:
<pre>
DATA_URL="<path to your data folder>"
SAVE_URL="<path to your output folder>"
</pre>

The path mentioned in 'DATA_URL' should contain all the unzipped data in 4 folders: 
<pre>
as-733  enron  p2p-Gnutella  reality_mining_voices
</pre>

### Generated Plots
####AS-733
![Plot](https://raw.github.com/sagarjauhari/graph_anomaly_detect/master/png/as-733_canberra.png)

####Enron
![Plot](https://raw.github.com/sagarjauhari/graph_anomaly_detect/master/png/enron_canberra.png)
####p2p-Gnutella
![Plot](https://raw.github.com/sagarjauhari/graph_anomaly_detect/master/png/p2p-Gnutella_canberra.png)
####Reality Mining Voices
![Plot]

### References
[1] Berlingerio, Michele, et al. "NetSimile: a scalable approach to size-independent network similarity." arXiv preprint arXiv:1209.2684 (2012).
