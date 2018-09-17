from crea.blockchain import Blockchain

# parse the whole chain
for event in Blockchain().replay():
    print("Event: %s" % event['op_type'])
    print("Time: %s" % event['timestamp'])
    print("Body: %s\n" % event['op'])

# parse only payments from specific datetime until now
b = Blockchain()
history = b.replay(
    start_block=b.get_block_from_time("2016-09-01T00:00:00"),
    end_block=b.get_current_block(),
    filter_by=['transfer']
)
for payment in history:
    print("@%s sent %s to @%s" % (payment['from'], payment['amount'], payment['to']))

# Output:
# @victoriart sent 1.000 CBD to @null
# @dude sent 5.095 CREA to @bittrex
# @devil sent 5.107 CREA to @poloniex
# @pinoytravel sent 0.010 CBD to @null
# @aladdin sent 5.013 CREA to @poloniex
# @mrwang sent 31.211 CREA to @blocktrades
# @kodi sent 0.030 CBD to @creabingo
