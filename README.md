# What is the issue?

A transaction starts from the sender and go to a gateway node through a non-advertised channel and then it goes to a bridge node through a bridge channel. It can do the last part multiple times till it reaches the gateway channel of the recipient that is directly connected to the recipient with a non-advertised channel.   

The sender is connected to 5 gateway nodes by default. And the metrics of the autopilot is by checking the uptime and the cost. The uptime means availability by another node. That makes the network more reliable.  The AMP is splitting a large transaction to multiple small ones. That each one can go through different paths. 

Thus, the opened issue in the below link on the clightning repository is willing to show the sender what are the routing feerate of each peer the sender is connected to as it is believed it would be important.  

So, in this repositority we wish to address the problem of [listpeers function](https://github.com/ElementsProject/lightning/issues/3683). 

# Theoretical understanding

First let us simply explain how does routing payments work. Imagine a node B in an A-B-C serial connection. The channels are set in a way that B has inbound capacity from A and outgoing capacity to C. If A wants to pay C there will be 1 hop in the route which is B. Therefore, A sends the satoshis to B (the routing node) which will pay to C.

For this kind of transformation through a hop two kind of fee components are needed:
* base fee: is a flat rate that is charged per transaction that is routed through the node (e.g. in this case B can charge A for the route payments through his node). 
* fee_rate: is a percentage fee charged on the value of the payment transaction that node provides.

So A can estimate exactly what fee he is going to pay B by reading two parameter [fee_base_msat, fee_proportional_millionths] in nodes policy and compute:

> base_fee_millisatoshi + ( amount_to_forward * fee_proportional_millionths / 1000000 )

That base_fee_millisatoshi for each channel can be find by the command:

```
ligthning-cli listchannels
```

But it's challenging due to the fact that there are huge amount of channels which makes wanting to find the one; a hard task to accomplish. There is also a website Containg all infirmation about ligthning nodes and channels [](https://1ml.com/). Therefore, A can simply search B node is or the channel id that it has with B and find out about the base fee and fee rate to compute its transaction's cost.

Well here we are getting a little ahead of ourselve. First please let us explain what steps we took to set uo the field in order to solve the afromentioned problem.\

# Setup Steps

In our assignment, we are working on displaying the feerate of each peer in our listpeers Clightning command. To do that we need to have a Clightning node. Clightning connects to Bitcoin Core in its configuration, so before working with Clightning we need a working bitcoind node.  

1. TOR: 

We Installed TOR and configuring it listening to bitcoin Core ports so that we keep our public key encrypted to assure being anonymous. It is not mandatory in our assignment, but it adds value to our work and security to our node. 

2. Bitcoin Core: 

We installed Bitcoin Core and configured it as needed. 

```
$ wget https://bitcoincore.org/bin/bitcoin-core-0.20.1/bitcoin-0.20.1-x86_64-linux-gnu.tar.gz 

$ tar xvzf bitcoin-0.20.1-x86_64-linux-gnu.tar.gz 

$ cd bitcoin-0.20.1 
```
Note that the bitcoin core takes by default the mainnet network, but we are working on the testnet so we did the needed modifications to the config file

![1](https://user-images.githubusercontent.com/72521500/106398629-3e2a1180-6414-11eb-8091-ad16babee9f5.jpeg)

Then we run the bitcoin daemon using the below command and wait till it is synchronized: 

```
$ bitcoind
```

![2](https://user-images.githubusercontent.com/72521500/106398016-c3132c00-6410-11eb-80df-9cf89acbe154.JPG)

The next step is to create a new Wallet that holds our funds. To make sure our bitcoin node is working on testnet we can run the command below: 

```
$ bitcoin-cli -testnet -getinfo 
```

To create the wallet, we run the below commands: 

```
$ bitcoin-cli -testnet - getnewaddress 
``` 

The outcome of the above command is our public key, so to know our private key we can do the following: 

```
$ bitcoin-cli -testnet dumpprivkey PUBLIC_KEY 
``` 

To view our wallets, we can run the below command: 

```
$ bitcoin-cli -testnet listreceivedbyaddress 1 true 
``` 

To view our wallet’s info, we can run the below command: 

```
$ bitcoin-cli -testnet getwalletinfo 
``` 

To send BTC to another wallet, we use the public address of that wallet in the below command: 

```
$ bitcoin-cli -testnet sendtoaddress PUBLIC_KEY AMOUNTINBTC 
```

To view our wallet’s info, we can run the below command: 

```
$ bitcoin-cli -testnet getwalletinfo 
```

3. Clightning 

Get dependencies: 

```
$ sudo apt-get update 

$ sudo apt-get install -y \ 
  autoconf automake build-essential git libtool libgmp-dev \ 
  libsqlite3-dev python3 python3-mako net-tools zlib1g-dev libsodium-dev \ 
  gettext 
``` 

Clone lightning: 

```
$ git clone https://github.com/ElementsProject/lightning.git 

$ cd lightning 
```
 
Running lightning daemon and creating a new channel:  

```
$ lightningd 

$ lightning-cli newaddress

$ lightning-cli getinfo

```

![3](https://user-images.githubusercontent.com/72521500/106398143-711ed600-6411-11eb-9941-fa39c558993e.jpeg)

Now that we have both bitcoin and ligthning set up, we must connect to the network.

# Connecting to Network: 

After having a running clightning node and connected to the Bitcoin Daemon, we need our clightning node to have funds and connected to a list of peers. 

1. Funding by transaction from bitcoin node to the cligthning node

![4](https://user-images.githubusercontent.com/72521500/106398266-310c2300-6412-11eb-8cc1-5c5ddb289653.JPG)

After setting up a Clightning Node with a new address we need to fund it first from our bitcoin Node. 

![5](https://user-images.githubusercontent.com/72521500/106398728-f2c43300-6414-11eb-87c8-a2b333589a51.jpeg)

![5 1](https://user-images.githubusercontent.com/72521500/106398732-f8ba1400-6414-11eb-9363-1b247ea5110a.jpeg)


2. Funding and Connecting to channels: 

After having funds, we can connect to channels that have a lot of nodes. So, we connected our clightning node to top active channels on the testnet network after we fund them with the minimum amount (100,000 satoushis). The reason behind this funding is to share this amount with the channel and they keep it blocked and they send back the same amount that is going to be blocked from our node. This exchange allows us to make a transaction or to pass a transaction by our node of maximum amount 100,000 satoushis (The amount funded to the channel). We choose the channels from the [](https://1ml.com/testnet/node?order=capacity&public=true) website as a reference. 

![6](https://user-images.githubusercontent.com/72521500/106398443-1a1a0080-6413-11eb-94b4-f44dce1af35c.JPG)

![7](https://user-images.githubusercontent.com/72521500/106398464-37e76580-6413-11eb-9728-9b28e0e2920d.JPG)

3. List Channels and List Peers: 

Now after connecting to two channels we now have a list of nodes for each channel, and we are directly connected to two peers due to the channel funding made, and all routing possibilities that we are connected to in the listchannels. 

In the following you see the outcome of `listpeers` , `listchannels` and `listnodes` respectively. 

![8](https://user-images.githubusercontent.com/72521500/106398588-eb505a00-6413-11eb-91b4-860f9778f19e.jpeg)

![9](https://user-images.githubusercontent.com/72521500/106398590-f5725880-6413-11eb-9566-a43418cc28ea.jpeg)

![10](https://user-images.githubusercontent.com/72521500/106398597-002ced80-6414-11eb-8e9e-e16c33567ff2.jpeg)

Now let's see what are the solutions to the afromentioned issue.

# What are the solutions?

As we already mentioned the main purpose of this assignment is to add to the clightning ‘listpeers’ command the capability to display the routing fee of each peer in the list. So, after being connected to a list of peers we hypothesize two solutions for it. 

> Routing fee = Base fee + (amount of transaction* fee rate) 

Without losing generality we assume the amount of transaction is 1 sat that simplify our computations.

We purpose 2 solutions as follow:

1. C Code Modification of the [Clightning Repository](https://github.com/ElementsProject/lightning): 

The first step was to understand the running code behind clightning. We knew how clightning daemon takes control of the running process starting with lightningd and other daemon that are responsible for a certain operation. The communication among these daemons is what makes clightning. Each Daemon has a separate directory, and the common directory have the data structure of common Struct used in the project. 

For us, we get into the wallet directory then to walletrpc.c code where listpeers function is coded. We’ve seen that it treats a list of channels, so we got interested the Struct Channel. Then we got to the common directory and found the struct channel in the initial_channel.h file. As we’ve conceived that the routing fee rate is calculated during the transaction pathway through the channel, and it is not communicated concretely before any routing decision. Which made our objective difficult to achieve, as we are willing to provide an information that needs to be shared and not found locally. So, to achieve it by modifying the C code needs modifications not only in our used Github Repository on our machine but also on every other user’s side.  

Not only we’ve not seen suggestions for a solution that closes the issue that we are working on but also, we’ve seen the routing fee rate is an information that is not found locally for each peer.  

Thus, we considered this hypothesis that it is not validated and moved to the second hypothesis. 

2. Implementing Plugins: 









