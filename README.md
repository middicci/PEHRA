
# P.E.H.R.A - Protocol for Energy Harvesting & Recovery Automation   #COP26


## Kafka - PEHRA (Energy Saving Protocol for Kafka cluster) 

In order to save energy consumption by keeping some nodes dormant in the kafka cluster a protocol is required for inter-node communication.


```peharedar = election(random(nodes), term):```

All participating nodes entering in elections are choose randomly to dimish predictibility and attack on the Peharedar node (monitor node).


```alarmClock(nodes, intervals):```

All participating nodes in PEHRA, choose an interval at which they wakeUp() themselves  and see if there's an incoming request or current Peharedar node is active. If elected Pehredar node is not active, it will send a WakeUpAll(nodes) signal to participating nodes in PEHRA.

```wakeUpAll(nodes):```

Peharedar node sends wakeUpAll() signal to all dormant nodes when it start receiving traffic.


```reElection(nodes, term):```

All participating nodes reElect Peharedar node before the end of term length of Peharedar node.


```maintenance(nodes):```

All nodes except Peharedar go under maintenance one by one and choose new Peharedar via election before taking down current Peharedar.


```allDown(nodes):```

When all nodes go down for any reason, first node to become active becomes temp Peharadar and waits for all node to be active to participate in new election.

```sleepCycle(nodes, interval):```

All nodes except Peharedar node are allowed to sleep/hibernate for a specified amount of time when no traffic activity. A node can choose to be awake all time.


```disablePehra(peharedar):```

Peharedar node can disable PEHRA mode and wakeUpAll() before doing so if it senses a threat of any kind.


```enablePehra(nodes)```

Only a human admin can enable PEHRA mode at any time for a given cluster. A human admin can also disable PEHRA at ant moment.









