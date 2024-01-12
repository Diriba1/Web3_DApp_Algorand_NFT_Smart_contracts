from algosdk import mnemonic


def passphrase_from_private_key(private_key):
    """Return passphrase from provided private key."""
    return mnemonic.from_private_key(private_key)