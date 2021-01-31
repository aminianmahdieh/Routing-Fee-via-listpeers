# Theoretical Understanding 

A transaction starts from the sender and go to a gateway node through a non-advertised channel and then it goes to a bridge node through a bridge channel. It can do the last part multiple times till it reaches the gateway channel of the recipient that is directly connected to the recipient with a non-advertised channel.   
The sender is connected to 5 gateway nodes by default. And the metrics of the autopilot is by checking the uptime and the cost. The uptime means availability by another node. That makes the network more reliable.  The AMP is splitting a large transaction to multiple small ones. That each one can go through different paths. 

So, the opened issue in the below link on the clightning repository is willing to show the sender what are the routing feerate of each peer the sender is connected to as it is believed it would be important.  
