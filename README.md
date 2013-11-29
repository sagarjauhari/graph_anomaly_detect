##Anomaly detection in time evolving graphs


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
![Plot](https://github.com/sagarjauhari/graph_anomaly_detect/blob/master/png/as-733_canberra.png)
####Enron
![Plot](https://raw.github.com/sagarjauhari/graph_anomaly_detect/master/png/enron_canberra.png)
####p2p-Gnutella
![Plot](https://raw.github.com/sagarjauhari/graph_anomaly_detect/master/png/p2p-Gnutella_canberra.png)
####Reality Mining Voices
![Plot](https://raw.github.com/sagarjauhari/graph_anomaly_detect/master/png/reality_mining_voices_canberra.png)
