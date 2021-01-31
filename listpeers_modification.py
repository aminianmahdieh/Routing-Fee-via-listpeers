

from lightning import Plugin

import json

plugin = Plugin()

@plugin.method("listpeers_modification")
def listpeers_modification(plugin):

    reply = {}
    peers = plugin.rpc.listpeers()
    channelss= plugin.rpc.listchannels()
    fee_rate= 0.000001
    for p in peers['peers']:
        for c in p['channels']:
            short_channel_id= c['short_channel_id']
            for channel in channelss['channels']:
                if channel['short_channel_id']==short_channel_id:
                    base_fee = int(channel['base_fee_millisatoshi'])*0.0001
                    break
                routing_fee = base_fee + fee_rate
                c['routing_fees'] = routing_fee
    reply['channels'] = json.dumps(peers)
    return reply


@plugin.init()
def init(options, configuration, plugin):
    plugin.log("Plugin listpeers_modification.py initialized")


plugin.run()