# Kafka - PEHRA (Energy Saving Protocol for Kafka cluster)  #COP26

In order to save energy consumption by keeping some nodes dormant in the kafka cluster a protocol is required for inter-node communication.


```elect(node, term):```

Elects a node from Kafka cluster as Peharedar (monitor node) to received incoming requests, while all other nodes are allowed to sleep (be dormant).


```alarmClock(nodes, intervals):```

All participating nodes in PEHRA, choose an interval at which they wakeUp() themselves  and see if there's an incoming request or current Peharedar node is active. If elected Pehredar node is not active, it will send a WakeUpAll(nodes) signal to participating nodes in PEHRA.


```reElection(nodes, term):```

All participating nodes reElect Peharedar node before the end of term length of Peharedar node.


```election(peharedar = random(nodes)):```

All participating nodes entering in elections are choose randomly to dimish predictibility and attack on the Peharedar node.


```maintenance(nodes):```

All nodes except Peharedar go under maintenance one by one and choose new Peharedar via election before taking down current Peharedar.


```allDown(nodes):```

When all nodes go down for any reason, first node to become active becomes temp Peharadar and waits for all node to be active to participate in new election.


```wakeUpAll(nodes):```

Peharedar node sends wakeUpAll() signal to all dormant nodes when it receives a message.










