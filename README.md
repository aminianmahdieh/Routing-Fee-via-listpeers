# What is the issue?

A transaction starts from the sender and go to a gateway node through a non-advertised channel and then it goes to a bridge node through a bridge channel. It can do the last part multiple times till it reaches the gateway channel of the recipient that is directly connected to the recipient with a non-advertised channel.   
The sender is connected to 5 gateway nodes by default. And the metrics of the autopilot is by checking the uptime and the cost. The uptime means availability by another node. That makes the network more reliable.  The AMP is splitting a large transaction to multiple small ones. That each one can go through different paths. 

Thus, the opened issue in the below link on the clightning repository is willing to show the sender what are the routing feerate of each peer the sender is connected to as it is believed it would be important.  

So, in this repositority we wish to address the problem of [listpeers function](https://github.com/ElementsProject/lightning/issues/3683). 

# Theoretical understanding

First let us simply explain how does routing payments work. Imagine a node B in an A-B-C serial connection. The channels are set in a way that B has inbound capacity from A and outgoing capacity to C. If A wants to pay C there will be 1 hop in the route which is B. Therefore, A sends the satoshis to B (the routing node) which will pay to C.
The capacity of the channels do not change, only move.

For this kind of transformation through a hop two kind of fee components are needed:
* base fee: is a flat rate that is charged per transaction that is routed through the node (e.g. in this case B can charge A for the route payments through his node). 
* fee_rate: is a percentage fee charged on the value of the payment transaction that node provides.

So A can estimate exactly what fee he is going to pay B by reading two parameter [fee_base_msat, fee_proportional_millionths] in nodes policy and compute:

> base_fee_millisatoshi + ( amount_to_forward * fee_proportional_millionths / 1000000 )

That base_fee_millisatoshi for each channel can be find by the command:

```
ligthning-cli listchannels
```

But it's challenging due to the fact that there are huge amount of channel that just wanting to find the one is a hard task to accomplish. There is also a website 

