import matplotlib.pyplot as plt
import pandas as pd
import json

raw = json['list']
wpm = []
time = []
for i in raw:
	wpm.append(i[0])
	time.append(i[1])


plt.figure(figsize=(12, 9))  
  
ax = plt.subplot(111)  
ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False)  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  

plt.xticks(fontsize=16)  
plt.yticks(range(5000, 30001, 5000), fontsize=16)  
  
plt.xlabel("Time Elapsed", fontsize=16)  
plt.ylabel("Word Per Minute(WPM)", fontsize=16)  

plt.axhline(y=150,linewidth=1, color=r)
plt.axhline(y=120,linewidth=1, color=g)

plt.plot(time.values, wpm.values,color="#3F5D7D")  

plt.savefig("wpm-time-graph.png", bbox_inches="tight");