from creapy.instance import shared_crea_instance

from .exceptions import WitnessDoesNotExistsException


class Witness(dict):
    """ Read data about a witness in the chain

        :param str account_name: Name of the witness
        :param Crea crea_instance: Crea() instance to use when accesing a RPC
        :param bool lazy: Use lazy loading

    """
    def __init__(
        self,
        witness,
        crea_instance=None,
        lazy=False
    ):
        self.crea = crea_instance or shared_crea_instance()
        self.cached = False
        self.witness = witness

        if not lazy:
            self.refresh()

    def refresh(self):
        witness = self.crea.rpc.get_witness_by_account(self.witness)
        if not witness:
            raise WitnessDoesNotExistsException
        super(Witness, self).__init__(witness)
        self.cached = True

    def __getitem__(self, key):
        if not self.cached:
            self.refresh()
        return super(Witness, self).__getitem__(key)

    def items(self):
        if not self.cached:
            self.refresh()
        return super(Witness, self).items()
