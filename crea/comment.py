# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
import json
import re
import logging
import pytz
import math
from datetime import datetime, date, time
from .instance import shared_crea_instance
from .account import Account
from .amount import Amount
from .price import Price
from .utils import resolve_authorperm, construct_authorperm, derive_permlink, remove_from_dict, make_patch, formatTimeString, formatToTimeStamp
from .blockchainobject import BlockchainObject
from .exceptions import ContentDoesNotExistsException, VotingInvalidOnArchivedPost
from creabase import operations
from creagraphenebase.py23 import py23_bytes, bytes_types, integer_types, string_types, text_type
from crea.constants import CREA_REVERSE_AUCTION_WINDOW_SECONDS_HF6, CREA_REVERSE_AUCTION_WINDOW_SECONDS_HF20, CREA_100_PERCENT, CREA_1_PERCENT
log = logging.getLogger(__name__)


class Comment(BlockchainObject):
    """ Read data about a Comment/Post in the chain

        :param str authorperm: identifier to post/comment in the form of
            ``@author/permlink``
        :param Crea crea_instance: :class:`crea.crea.Crea` instance to use when accessing a RPC


        .. code-block:: python

        >>> from crea.comment import Comment
        >>> from crea.account import Account
        >>> from crea import Crea
        >>> stm = Crea("https://cread.minnowsupportproject.org")
        >>> acc = Account("gtg", crea_instance=stm)
        >>> authorperm = acc.get_blog(limit=1)[0]["authorperm"]
        >>> c = Comment(authorperm)
        >>> postdate = c["created"]
        >>> postdate_str = c.json()["created"]

    """
    type_id = 8

    def __init__(
        self,
        authorperm,
        full=True,
        lazy=False,
        crea_instance=None
    ):
        self.full = full
        self.lazy = lazy
        self.crea = crea_instance or shared_crea_instance()
        if isinstance(authorperm, string_types) and authorperm != "":
            [author, permlink] = resolve_authorperm(authorperm)
            self["id"] = 0
            self["author"] = author
            self["permlink"] = permlink
            self["authorperm"] = authorperm
        elif isinstance(authorperm, dict) and "author" in authorperm and "permlink" in authorperm:
            authorperm["authorperm"] = construct_authorperm(authorperm["author"], authorperm["permlink"])
            authorperm = self._parse_json_data(authorperm)
        super(Comment, self).__init__(
            authorperm,
            id_item="authorperm",
            lazy=lazy,
            full=full,
            crea_instance=crea_instance
        )

    def _parse_json_data(self, comment):
        parse_times = [
            "active", "cashout_time", "created", "last_payout", "last_update",
            "max_cashout_time"
        ]
        for p in parse_times:
            if p in comment and isinstance(comment.get(p), string_types):
                comment[p] = formatTimeString(comment.get(p, "1970-01-01T00:00:00"))
        # Parse Amounts
        sbd_amounts = [
            "total_payout_value",
            "max_accepted_payout",
            "pending_payout_value",
            "curator_payout_value",
            "total_pending_payout_value",
            "promoted",
        ]
        for p in sbd_amounts:
            if p in comment and isinstance(comment.get(p), (string_types, list, dict)):
                comment[p] = Amount(comment.get(p, "0.000 %s" % (self.crea.sbd_symbol)), crea_instance=self.crea)

        # turn json_metadata into python dict
        meta_str = comment.get("json_metadata", "{}")
        if meta_str == "{}":
            comment['json_metadata'] = meta_str
        if isinstance(meta_str, (string_types, bytes_types, bytearray)):
            try:
                comment['json_metadata'] = json.loads(meta_str)
            except:
                comment['json_metadata'] = {}

        comment["tags"] = []
        comment['community'] = ''
        if isinstance(comment['json_metadata'], dict):
            if "tags" in comment['json_metadata']:
                comment["tags"] = comment['json_metadata']["tags"]
            if 'community' in comment['json_metadata']:
                comment['community'] = comment['json_metadata']['community']

        parse_int = [
            "author_reputation",
        ]
        for p in parse_int:
            if p in comment and isinstance(comment.get(p), string_types):
                comment[p] = int(comment.get(p, "0"))

        if "active_votes" in comment:
            new_active_votes = []
            for vote in comment["active_votes"]:
                if 'time' in vote and isinstance(vote.get('time'), string_types):
                    vote['time'] = formatTimeString(vote.get('time', "1970-01-01T00:00:00"))
                parse_int = [
                    "rshares", "reputation",
                ]
                for p in parse_int:
                    if p in vote and isinstance(vote.get(p), string_types):
                        vote[p] = int(vote.get(p, "0"))
                new_active_votes.append(vote)
            comment["active_votes"] = new_active_votes
        return comment

    def refresh(self):
        if self.identifier == "":
            return
        if not self.crea.is_connected():
            return
        [author, permlink] = resolve_authorperm(self.identifier)
        self.crea.rpc.set_next_node_on_empty_reply(True)
        if self.crea.rpc.get_use_appbase():
            content = self.crea.rpc.get_discussion({'author': author, 'permlink': permlink}, api="tags")
        else:
            content = self.crea.rpc.get_content(author, permlink)
        if not content or not content['author'] or not content['permlink']:
            raise ContentDoesNotExistsException(self.identifier)
        content = self._parse_json_data(content)
        content["authorperm"] = construct_authorperm(content['author'], content['permlink'])
        super(Comment, self).__init__(content, id_item="authorperm", lazy=self.lazy, full=self.full, crea_instance=self.crea)

    def json(self):
        output = self.copy()
        if "authorperm" in output:
            output.pop("authorperm")
        if 'json_metadata' in output:
            output["json_metadata"] = json.dumps(output["json_metadata"], separators=[',', ':'])
        if "tags" in output:
            output.pop("tags")
        if "community" in output:
            output.pop("community")
        parse_times = [
            "active", "cashout_time", "created", "last_payout", "last_update",
            "max_cashout_time"
        ]
        for p in parse_times:
            if p in output:
                p_date = output.get(p, datetime(1970, 1, 1, 0, 0))
                if isinstance(p_date, (datetime, date)):
                    output[p] = formatTimeString(p_date)
                else:
                    output[p] = p_date
        sbd_amounts = [
            "total_payout_value",
            "max_accepted_payout",
            "pending_payout_value",
            "curator_payout_value",
            "total_pending_payout_value",
            "promoted",
        ]
        for p in sbd_amounts:
            if p in output and isinstance(output[p], Amount):
                output[p] = output[p].json()
        parse_int = [
            "author_reputation",
        ]
        for p in parse_int:
            if p in output and isinstance(output[p], integer_types):
                output[p] = str(output[p])
        if "active_votes" in output:
            new_active_votes = []
            for vote in output["active_votes"]:
                if 'time' in vote:
                    p_date = vote.get('time', datetime(1970, 1, 1, 0, 0))
                    if isinstance(p_date, (datetime, date)):
                        vote['time'] = formatTimeString(p_date)
                    else:
                        vote['time'] = p_date
                parse_int = [
                    "rshares", "reputation",
                ]
                for p in parse_int:
                    if p in vote and isinstance(vote[p], integer_types):
                        vote[p] = str(vote[p])
                new_active_votes.append(vote)
            output["active_votes"] = new_active_votes
        return json.loads(str(json.dumps(output)))

    @property
    def id(self):
        return self["id"]

    @property
    def author(self):
        return self["author"]

    @property
    def permlink(self):
        return self["permlink"]

    @property
    def authorperm(self):
        return construct_authorperm(self["author"], self["permlink"])

    @property
    def category(self):
        if "category" in self:
            return self["category"]
        else:
            return ""

    @property
    def parent_author(self):
        return self["parent_author"]

    @property
    def parent_permlink(self):
        return self["parent_permlink"]

    @property
    def depth(self):
        return self["depth"]

    @property
    def title(self):
        if "title" in self:
            return self["title"]
        else:
            return ""

    @property
    def body(self):
        if "body" in self:
            return self["body"]
        else:
            return ""

    @property
    def json_metadata(self):
        if "json_metadata" in self:
            return self["json_metadata"]
        else:
            return {}

    def is_main_post(self):
        """ Returns True if main post, and False if this is a comment (reply).
        """
        return self['depth'] == 0

    def is_comment(self):
        """ Returns True if post is a comment
        """
        return self['depth'] > 0

    @property
    def reward(self):
        """ Return the estimated total CBD reward.
        """
        a_zero = Amount(0, self.crea.sbd_symbol, crea_instance=self.crea)
        author = Amount(self.get("total_payout_value", a_zero), crea_instance=self.crea)
        curator = Amount(self.get("curator_payout_value", a_zero), crea_instance=self.crea)
        pending = Amount(self.get("pending_payout_value", a_zero), crea_instance=self.crea)
        return author + curator + pending

    def is_pending(self):
        """ Returns if the payout is pending (the post/comment
            is younger than 7 days)
        """
        a_zero = Amount(0, self.crea.sbd_symbol, crea_instance=self.crea)
        total = Amount(self.get("total_payout_value", a_zero), crea_instance=self.crea)
        post_age_days = self.time_elapsed().total_seconds() / 60 / 60 / 24
        return post_age_days < 7.0 and float(total) == 0

    def time_elapsed(self):
        """Returns a timedelta on how old the post is.
        """
        utc = pytz.timezone('UTC')
        return utc.localize(datetime.utcnow()) - self['created']

    def curation_penalty_compensation_CBD(self):
        """ Returns The required post payout amount after 15 minutes
            which will compentsate the curation penalty, if voting earlier than 15 minutes
        """
        self.refresh()
        if self.crea.hardfork >= 20:
            reverse_auction_window_seconds = CREA_REVERSE_AUCTION_WINDOW_SECONDS_HF20
        else:
            reverse_auction_window_seconds = CREA_REVERSE_AUCTION_WINDOW_SECONDS_HF6
        return self.reward * reverse_auction_window_seconds / ((self.time_elapsed()).total_seconds() / 60) ** 2

    def estimate_curation_CBD(self, vote_value_CBD, estimated_value_CBD=None):
        """ Estimates curation reward

            :param float vote_value_CBD: The vote value in CBD for which the curation
                should be calculated
            :param float estimated_value_CBD: When set, this value is used for calculate
                the curation. When not set, the current post value is used.
        """
        self.refresh()
        if estimated_value_CBD is None:
            estimated_value_CBD = float(self.reward)
        t = 1.0 - self.get_curation_penalty()
        k = vote_value_CBD / (vote_value_CBD + float(self.reward))
        K = (1 - math.sqrt(1 - k)) / 4 / k
        return K * vote_value_CBD * t * math.sqrt(estimated_value_CBD)

    def get_curation_penalty(self, vote_time=None):
        """ If post is less than 15 minutes old, it will incur a curation
            reward penalty.

            :param datetime vote_time: A vote time can be given and the curation
                penalty is calculated regarding the given time (default is None)
                When set to None, the current date is used.
            :returns: Float number between 0 and 1 (0.0 -> no penalty, 1.0 -> 100 % curation penalty)
            :rtype: float

        """
        if vote_time is None:
            elapsed_seconds = self.time_elapsed().total_seconds()
        elif isinstance(vote_time, str):
            elapsed_seconds = (formatTimeString(vote_time) - self["created"]).total_seconds()
        elif isinstance(vote_time, (datetime, date)):
            elapsed_seconds = (vote_time - self["created"]).total_seconds()
        else:
            raise ValueError("vote_time must be a string or a datetime")
        if self.crea.hardfork >= 20:
            reward = (elapsed_seconds / CREA_REVERSE_AUCTION_WINDOW_SECONDS_HF20)
        else:
            reward = (elapsed_seconds / CREA_REVERSE_AUCTION_WINDOW_SECONDS_HF6)
        if reward > 1:
            reward = 1.0
        return 1.0 - reward

    def get_vote_with_curation(self, voter=None, raw_data=False, pending_payout_value=None):
        """ Returns vote for voter. Returns None, if the voter cannot be found in `active_votes`.

            :param str voter: Voter for which the vote should be returned
            :param bool raw_data: If True, the raw data are returned
            :param pending_payout_CBD: When not None this value instead of the current
                value is used for calculating the rewards
            :type pending_payout_CBD: float, str
        """
        specific_vote = None
        if voter is None:
            voter = Account(self["author"], crea_instance=self.crea)
        else:
            voter = Account(voter, crea_instance=self.crea)
        for vote in self["active_votes"]:
            if voter["name"] == vote["voter"]:
                specific_vote = vote
        if specific_vote is not None and (raw_data or not self.is_pending()):
            return specific_vote
        elif specific_vote is not None:
            curation_reward = self.get_curation_rewards(pending_payout_CBD=True, pending_payout_value=pending_payout_value)
            specific_vote["curation_reward"] = curation_reward["active_votes"][voter["name"]]
            specific_vote["ROI"] = float(curation_reward["active_votes"][voter["name"]]) / float(voter.get_voting_value_CBD(voting_weight=specific_vote["percent"] / 100)) * 100
            return specific_vote
        else:
            return None

    def get_beneficiaries_pct(self):
        """ Returns the sum of all post beneficiaries in percentage
        """
        beneficiaries = self["beneficiaries"]
        weight = 0
        for b in beneficiaries:
            weight += b["weight"]
        return weight / 100.

    def get_rewards(self):
        """ Returns the total_payout, author_payout and the curator payout in CBD.
            When the payout is still pending, the estimated payout is given out.

            .. note:: Potential beneficiary rewards were already deducted from the
                      `author_payout` and the `total_payout`

            Example:::

                {
                    'total_payout': 9.956 CBD,
                    'author_payout': 7.166 CBD,
                    'curator_payout': 2.790 CBD
                }

        """
        if self.is_pending():
            total_payout = Amount(self["pending_payout_value"], crea_instance=self.crea)
            author_payout = self.get_author_rewards()["total_payout_CBD"]
            curator_payout = total_payout - author_payout
        else:
            author_payout = Amount(self["total_payout_value"], crea_instance=self.crea)
            curator_payout = Amount(self["curator_payout_value"], crea_instance=self.crea)
            total_payout = author_payout + curator_payout
        return {"total_payout": total_payout, "author_payout": author_payout, "curator_payout": curator_payout}

    def get_author_rewards(self):
        """ Returns the author rewards.

            Example::

                {
                    'pending_rewards': True,
                    'payout_SP': 0.912 CREA,
                    'payout_CBD': 3.583 CBD,
                    'total_payout_CBD': 7.166 CBD
                }

        """
        if not self.is_pending():
            return {'pending_rewards': False,
                    "payout_SP": Amount(0, self.crea.crea_symbol, crea_instance=self.crea),
                    "payout_CBD": Amount(0, self.crea.sbd_symbol, crea_instance=self.crea),
                    "total_payout_CBD": Amount(self["total_payout_value"], crea_instance=self.crea)}

        median_hist = self.crea.get_current_median_history()
        if median_hist is not None:
            median_price = Price(median_hist, crea_instance=self.crea)
        beneficiaries_pct = self.get_beneficiaries_pct()
        curation_tokens = self.reward * 0.25
        author_tokens = self.reward - curation_tokens
        curation_rewards = self.get_curation_rewards()
        if self.crea.hardfork >= 20 and median_hist is not None:
            author_tokens += median_price * curation_rewards['unclaimed_rewards']

        benefactor_tokens = author_tokens * beneficiaries_pct / 100.
        author_tokens -= benefactor_tokens

        if median_hist is not None:
            sbd_crea = author_tokens * self["percent_crea_dollars"] / 20000.
            vesting_crea = median_price.as_base(self.crea.crea_symbol) * (author_tokens - sbd_crea)
            return {'pending_rewards': True, "payout_SP": vesting_crea, "payout_CBD": sbd_crea, "total_payout_CBD": author_tokens}
        else:
            return {'pending_rewards': True, "total_payout": author_tokens}

    def get_curation_rewards(self, pending_payout_CBD=False, pending_payout_value=None):
        """ Returns the curation rewards.

            :param bool pending_payout_CBD: If True, the rewards are returned in CBD and not in CREA (default is False)
            :param pending_payout_value: When not None this value instead of the current
                value is used for calculating the rewards
            :type pending_payout_value: float, str

            `pending_rewards` is True when
            the post is younger than 7 days. `unclaimed_rewards` is the
            amount of curation_rewards that goes to the author (self-vote or votes within
            the first 30 minutes). `active_votes` contains all voter with their curation reward.

            Example::

                {
                    'pending_rewards': True, 'unclaimed_rewards': 0.245 CREA,
                    'active_votes': {
                        'leprechaun': 0.006 CREA, 'timcliff': 0.186 CREA,
                        'st3llar': 0.000 CREA, 'crokkon': 0.015 CREA, 'feedyourminnows': 0.003 CREA,
                        'isnochys': 0.003 CREA, 'loshcat': 0.001 CREA, 'greenorange': 0.000 CREA,
                        'qustodian': 0.123 CREA, 'jpphotography': 0.002 CREA, 'thinkingmind': 0.001 CREA,
                        'oups': 0.006 CREA, 'mattockfs': 0.001 CREA, 'holger80': 0.003 CREA, 'michaelizer': 0.004 CREA,
                        'flugschwein': 0.010 CREA, 'ulisessabeque': 0.000 CREA, 'hakancelik': 0.002 CREA, 'sbi2': 0.008 CREA,
                        'zcool': 0.000 CREA, 'creahq': 0.002 CREA, 'rowdiya': 0.000 CREA, 'qurator-tier-1-2': 0.012 CREA
                    }
                }

        """
        median_hist = self.crea.get_current_median_history()
        if median_hist is not None:
            median_price = Price(median_hist, crea_instance=self.crea)
        pending_rewards = False
        total_vote_weight = self["total_vote_weight"]
        if not self["allow_curation_rewards"] or not self.is_pending():
            max_rewards = Amount(0, self.crea.crea_symbol, crea_instance=self.crea)
            unclaimed_rewards = max_rewards.copy()
        else:
            if pending_payout_value is None:
                pending_payout_value = Amount(self["pending_payout_value"], crea_instance=self.crea)
            elif isinstance(pending_payout_value, (float, integer_types)):
                pending_payout_value = Amount(pending_payout_value, self.crea.sbd_symbol, crea_instance=self.crea)
            elif isinstance(pending_payout_value, str):
                pending_payout_value = Amount(pending_payout_value, crea_instance=self.crea)
            if pending_payout_CBD or median_hist is None:
                max_rewards = (pending_payout_value * 0.25)
            else:
                max_rewards = median_price.as_base(self.crea.crea_symbol) * (pending_payout_value * 0.25)
            unclaimed_rewards = max_rewards.copy()
            pending_rewards = True

        active_votes = {}
        for vote in self["active_votes"]:
            if total_vote_weight > 0:
                claim = max_rewards * int(vote["weight"]) / total_vote_weight
            else:
                claim = 0
            if claim > 0 and pending_rewards:
                unclaimed_rewards -= claim
            if claim > 0:
                active_votes[vote["voter"]] = claim
            else:
                active_votes[vote["voter"]] = 0

        return {'pending_rewards': pending_rewards, 'unclaimed_rewards': unclaimed_rewards, "active_votes": active_votes}

    def get_reblogged_by(self, identifier=None):
        """Shows in which blogs this post appears"""
        if not identifier:
            post_author = self["author"]
            post_permlink = self["permlink"]
        else:
            [post_author, post_permlink] = resolve_authorperm(identifier)
        if not self.crea.is_connected():
            return None
        self.crea.rpc.set_next_node_on_empty_reply(False)
        if self.crea.rpc.get_use_appbase():
            return self.crea.rpc.get_reblogged_by({'author': post_author, 'permlink': post_permlink}, api="follow")['accounts']
        else:
            return self.crea.rpc.get_reblogged_by(post_author, post_permlink, api="follow")

    def get_replies(self, raw_data=False, identifier=None):
        """ Returns content replies

            :param bool raw_data: When set to False, the replies will be returned as Comment class objects
        """
        if not identifier:
            post_author = self["author"]
            post_permlink = self["permlink"]
        else:
            [post_author, post_permlink] = resolve_authorperm(identifier)
        if not self.crea.is_connected():
            return None
        self.crea.rpc.set_next_node_on_empty_reply(False)
        if self.crea.rpc.get_use_appbase():
            content_replies = self.crea.rpc.get_content_replies({'author': post_author, 'permlink': post_permlink}, api="tags")['discussions']
        else:
            content_replies = self.crea.rpc.get_content_replies(post_author, post_permlink, api="tags")
        if raw_data:
            return content_replies
        return [Comment(c, crea_instance=self.crea) for c in content_replies]

    def get_all_replies(self, parent=None):
        """ Returns all content replies
        """
        if parent is None:
            parent = self
        if parent["children"] > 0:
            children = parent.get_replies()
            if children is None:
                return []
            for cc in children[:]:
                children.extend(self.get_all_replies(parent=cc))
            return children
        return []

    def get_parent(self, children=None):
        """ Returns the parent post with depth == 0"""
        if children is None:
            children = self
        while children["depth"] > 0:
            children = Comment(construct_authorperm(children["parent_author"], children["parent_permlink"]), crea_instance=self.crea)
        return children

    def get_votes(self, raw_data=False):
        """Returns all votes as ActiveVotes object"""
        if raw_data:
            return self["active_votes"]
        from .vote import ActiveVotes
        return ActiveVotes(self, lazy=False, crea_instance=self.crea)

    def upvote(self, weight=+100, voter=None):
        """ Upvote the post

            :param float weight: (optional) Weight for posting (-100.0 -
                +100.0) defaults to +100.0
            :param str voter: (optional) Voting account

        """
        last_payout = self.get('last_payout', None)
        if last_payout is not None:
            if formatToTimeStamp(last_payout) > 0:
                raise VotingInvalidOnArchivedPost
        return self.vote(weight, account=voter)

    def downvote(self, weight=-100, voter=None):
        """ Downvote the post

            :param float weight: (optional) Weight for posting (-100.0 -
                +100.0) defaults to -100.0
            :param str voter: (optional) Voting account

        """
        last_payout = self.get('last_payout', None)
        if last_payout is not None:
            if formatToTimeStamp(last_payout) > 0:
                raise VotingInvalidOnArchivedPost
        return self.vote(weight, account=voter)

    def vote(self, weight, account=None, identifier=None, **kwargs):
        """ Vote for a post

            :param float weight: Voting weight. Range: -100.0 - +100.0.
            :param str account: (optional) Account to use for voting. If
                ``account`` is not defined, the ``default_account`` will be used
                or a ValueError will be raised
            :param str identifier: Identifier for the post to vote. Takes the
                form ``@author/permlink``.

        """
        if not account:
            if "default_account" in self.crea.config:
                account = self.crea.config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, crea_instance=self.crea)
        if not identifier:
            post_author = self["author"]
            post_permlink = self["permlink"]
        else:
            [post_author, post_permlink] = resolve_authorperm(identifier)

        vote_weight = int(float(weight) * CREA_1_PERCENT)
        if vote_weight > CREA_100_PERCENT:
            vote_weight = CREA_100_PERCENT
        if vote_weight < -CREA_100_PERCENT:
            vote_weight = -CREA_100_PERCENT

        op = operations.Vote(
            **{
                "voter": account["name"],
                "author": post_author,
                "permlink": post_permlink,
                "weight": vote_weight
            })

        return self.crea.finalizeOp(op, account, "posting", **kwargs)

    def edit(self, body, meta=None, replace=False):
        """ Edit an existing post

            :param str body: Body of the reply
            :param json meta: JSON meta object that can be attached to the
                post. (optional)
            :param bool replace: Instead of calculating a *diff*, replace
                the post entirely (defaults to ``False``)

        """
        if not meta:
            meta = {}
        original_post = self

        if replace:
            newbody = body
        else:
            newbody = make_patch(original_post["body"], body)
            if not newbody:
                log.info("No changes made! Skipping ...")
                return

        reply_identifier = construct_authorperm(
            original_post["parent_author"], original_post["parent_permlink"])

        new_meta = {}
        if meta is not None:
            if bool(original_post["json_metadata"]):
                new_meta = original_post["json_metadata"]
                for key in meta:
                    new_meta[key] = meta[key]
            else:
                new_meta = meta

        return self.crea.post(
            original_post["title"],
            newbody,
            reply_identifier=reply_identifier,
            author=original_post["author"],
            permlink=original_post["permlink"],
            json_metadata=new_meta,
        )

    def reply(self, body, title="", author="", meta=None):
        """ Reply to an existing post

            :param str body: Body of the reply
            :param str title: Title of the reply post
            :param str author: Author of reply (optional) if not provided
                ``default_user`` will be used, if present, else
                a ``ValueError`` will be raised.
            :param json meta: JSON meta object that can be attached to the
                post. (optional)

        """
        return self.crea.post(
            title,
            body,
            json_metadata=meta,
            author=author,
            reply_identifier=self.identifier)

    def delete(self, account=None, identifier=None):
        """ Delete an existing post/comment

            :param str account: (optional) Account to use for deletion. If
                ``account`` is not defined, the ``default_account`` will be
                taken or a ValueError will be raised.

            :param str identifier: (optional) Identifier for the post to delete.
                Takes the form ``@author/permlink``. By default the current post
                will be used.

            .. note:: A post/comment can only be deleted as long as it has no
                      replies and no positive rshares on it.

        """
        if not account:
            if "default_account" in self.crea.config:
                account = self.crea.config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, crea_instance=self.crea)
        if not identifier:
            post_author = self["author"]
            post_permlink = self["permlink"]
        else:
            [post_author, post_permlink] = resolve_authorperm(identifier)
        op = operations.Delete_comment(
            **{"author": post_author,
               "permlink": post_permlink})
        return self.crea.finalizeOp(op, account, "posting")

    def recrea(self, identifier=None, account=None):
        """ Recrea a post

            :param str identifier: post identifier (@<account>/<permlink>)
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)

        """
        if not account:
            account = self.crea.configStorage.get("default_account")
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, crea_instance=self.crea)
        if identifier is None:
            identifier = self.identifier
        author, permlink = resolve_authorperm(identifier)
        json_body = [
            "reblog", {
                "account": account["name"],
                "author": author,
                "permlink": permlink
            }
        ]
        return self.crea.custom_json(
            id="follow", json_data=json_body, required_posting_auths=[account["name"]])


class RecentReplies(list):
    """ Obtain a list of recent replies

        :param str author: author
        :param bool skip_own: (optional) Skip replies of the author to him/herself.
            Default: True
        :param Crea crea_instance: Crea() instance to use when accesing a RPC
    """
    def __init__(self, author, skip_own=True, lazy=False, full=True, crea_instance=None):
        self.crea = crea_instance or shared_crea_instance()
        if not self.crea.is_connected():
            return None
        self.crea.rpc.set_next_node_on_empty_reply(True)
        state = self.crea.rpc.get_state("/@%s/recent-replies" % author)
        replies = state["accounts"][author].get("recent_replies", [])
        comments = []
        for reply in replies:
            post = state["content"][reply]
            if skip_own and post["author"] == author:
                continue
            comments.append(Comment(post, lazy=lazy, full=full, crea_instance=self.crea))
        super(RecentReplies, self).__init__(comments)


class RecentByPath(list):
    """ Obtain a list of votes for an account

        :param str account: Account name
        :param Crea crea_instance: Crea() instance to use when accesing a RPC
    """
    def __init__(self, path="promoted", category=None, lazy=False, full=True, crea_instance=None):
        self.crea = crea_instance or shared_crea_instance()
        if not self.crea.is_connected():
            return None
        self.crea.rpc.set_next_node_on_empty_reply(True)
        state = self.crea.rpc.get_state("/" + path)
        replies = state["discussion_idx"][''].get(path, [])
        comments = []
        for reply in replies:
            post = state["content"][reply]
            if category is None or (category is not None and post["category"] == category):
                comments.append(Comment(post, lazy=lazy, full=full, crea_instance=self.crea))
        super(RecentByPath, self).__init__(comments)
