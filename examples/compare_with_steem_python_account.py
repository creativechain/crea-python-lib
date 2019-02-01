from __future__ import print_function
import sys
from datetime import timedelta
import time
import io
from crea import Crea
from crea.account import Account
from crea.amount import Amount
from crea.utils import parse_time
from crea.account import Account as creaAccount
from crea.post import Post as creaPost
from crea import Crea as creaCrea
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    stm = Crea("https://node1.creary.net")
    crea_acc = Account("holger80", crea_instance=stm)
    stm2 = creaCrea(nodes=["https://node1.creary.net"])
    crea_acc = creaAccount("holger80", cread_instance=stm2)

    # profile
    print("crea_acc.profile  {}".format(crea_acc.profile))
    print("crea_acc.profile {}".format(crea_acc.profile))
    # sp
    print("crea_acc.sp  {}".format(crea_acc.sp))
    print("crea_acc.sp {}".format(crea_acc.sp))
    # rep
    print("crea_acc.rep  {}".format(crea_acc.rep))
    print("crea_acc.rep {}".format(crea_acc.rep))
    # balances
    print("crea_acc.balances  {}".format(crea_acc.balances))
    print("crea_acc.balances {}".format(crea_acc.balances))
    # get_balances()
    print("crea_acc.get_balances()  {}".format(crea_acc.get_balances()))
    print("crea_acc.get_balances() {}".format(crea_acc.get_balances()))
    # reputation()
    print("crea_acc.get_reputation()  {}".format(crea_acc.get_reputation()))
    print("crea_acc.reputation() {}".format(crea_acc.reputation()))
    # voting_power()
    print("crea_acc.get_voting_power()  {}".format(crea_acc.get_voting_power()))
    print("crea_acc.voting_power() {}".format(crea_acc.voting_power()))
    # get_followers()
    print("crea_acc.get_followers()  {}".format(crea_acc.get_followers()))
    print("crea_acc.get_followers() {}".format(crea_acc.get_followers()))
    # get_following()
    print("crea_acc.get_following()  {}".format(crea_acc.get_following()))
    print("crea_acc.get_following() {}".format(crea_acc.get_following()))
    # has_voted()
    print("crea_acc.has_voted()  {}".format(crea_acc.has_voted("@holger80/api-methods-list-for-appbase")))
    print("crea_acc.has_voted() {}".format(crea_acc.has_voted(creaPost("@holger80/api-methods-list-for-appbase"))))
    # curation_stats()
    print("crea_acc.curation_stats()  {}".format(crea_acc.curation_stats()))
    print("crea_acc.curation_stats() {}".format(crea_acc.curation_stats()))
    # virtual_op_count
    print("crea_acc.virtual_op_count()  {}".format(crea_acc.virtual_op_count()))
    print("crea_acc.virtual_op_count() {}".format(crea_acc.virtual_op_count()))
    # get_account_votes
    print("crea_acc.get_account_votes()  {}".format(crea_acc.get_account_votes()))
    print("crea_acc.get_account_votes() {}".format(crea_acc.get_account_votes()))
    # get_withdraw_routes
    print("crea_acc.get_withdraw_routes()  {}".format(crea_acc.get_withdraw_routes()))
    print("crea_acc.get_withdraw_routes() {}".format(crea_acc.get_withdraw_routes()))
    # get_conversion_requests
    print("crea_acc.get_conversion_requests()  {}".format(crea_acc.get_conversion_requests()))
    print("crea_acc.get_conversion_requests() {}".format(crea_acc.get_conversion_requests()))
    # export
    # history
    crea_hist = []
    for h in crea_acc.history(only_ops=["transfer"]):
        crea_hist.append(h)
        if len(crea_hist) >= 10:
            break
    crea_hist = []
    for h in crea_acc.history(filter_by="transfer", start=0):
        crea_hist.append(h)
        if len(crea_hist) >= 10:
            break
    print("crea_acc.history()  {}".format(crea_hist))
    print("crea_acc.history() {}".format(crea_hist))
    # history_reverse
    crea_hist = []
    for h in crea_acc.history_reverse(only_ops=["transfer"]):
        crea_hist.append(h)
        if len(crea_hist) >= 10:
            break
    crea_hist = []
    for h in crea_acc.history_reverse(filter_by="transfer"):
        crea_hist.append(h)
        if len(crea_hist) >= 10:
            break
    print("crea_acc.history_reverse()  {}".format(crea_hist))
    print("crea_acc.history_reverse() {}".format(crea_hist))
