import creapy as pstn

_shared_crea_instance = None


def shared_crea_instance():
    """ This method will initialize _shared_crea_instance and return it.
    The purpose of this method is to have offer single default Crea instance that can be reused by multiple classes.
    """
    global _shared_crea_instance
    if not _shared_crea_instance:
        _shared_crea_instance = pstn.Crea()  # todo: add creapy config
    return _shared_crea_instance


def set_shared_crea_instance(crea_instance):
    """ This method allows us to override default Crea instance for all users of
    _shared_crea_instance.
    """
    global _shared_crea_instance
    _shared_crea_instance = crea_instance
