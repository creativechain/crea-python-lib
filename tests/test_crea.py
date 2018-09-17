import unittest

from creapy.post import Post
from creapy.crea import Crea
from creapy.exceptions import (
    MissingKeyError,
    InsufficientAuthorityError,
    VotingInvalidOnArchivedPost
)

identifier = "@tridex/creapy"
testaccount = "tridex"
wif = {
    "active": "5KkUHuJEFhN1RCS3GLV7UMeQ5P1k5Vu31jRgivJei8dBtAcXYMV",
    "posting": "5KkUHuJEFhN1RCS3GLV7UMeQ5P1k5Vu31jRgivJei8dBtAcXYMV",
    "owner": "5KkUHuJEFhN1RCS3GLV7UMeQ5P1k5Vu31jRgivJei8dBtAcXYMV"
}
crea = Crea(nobroadcast=True, keys=wif)


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Testcases, self).__init__(*args, **kwargs)
        self.post = Post(identifier, crea_instance=crea)

    def test_getOpeningPost(self):
        self.post._getOpeningPost()

    def test_reply(self):
        try:
            self.post.reply(body="foobar", title="", author=testaccount, meta=None)
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_upvote(self):
        try:
            self.post.upvote(voter=testaccount)
        except VotingInvalidOnArchivedPost:
            pass
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_downvote(self, weight=-100, voter=testaccount):
        try:
            self.post.downvote(voter=testaccount)
        except VotingInvalidOnArchivedPost:
            pass
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_edit(self):
        try:
            crea.edit(identifier, "Foobar")
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_post(self):
        try:
            crea.post("title", "body", meta={"foo": "bar"}, author=testaccount)
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_create_account(self):
        try:
            crea.create_account("jared-create",
                                 creator=testaccount,
                                 password="foobar foo bar hello world",
                                 storekeys=False
                                 )
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_transfer(self):
        try:
            crea.transfer("jared", 10, "CREA", account=testaccount)
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_withdraw_vesting(self):
        try:
            crea.withdraw_vesting(10, account=testaccount)
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_transfer_to_vesting(self):
        try:
            crea.transfer_to_vesting(10, to=testaccount, account=testaccount)
        except InsufficientAuthorityError:
            pass
        except MissingKeyError:
            pass

    def test_get_replies(self):
        crea.get_replies(author=testaccount)

    def test_get_posts(self):
        crea.get_posts()

    def test_get_balances(self):
        crea.get_balances(testaccount)

    def test_getPost(self):
        self.assertEqual(Post("@jared/creapy", crea_instance=crea).url,
                         "/creapy/@jared/creapy")
        self.assertEqual(Post({"author": "@jared", "permlink": "creapy"}, crea_instance=crea).url,
                         "/creapy/@jared/creapy")


if __name__ == '__main__':
    unittest.main()
