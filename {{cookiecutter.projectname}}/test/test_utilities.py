from core.utilities.utilities import AESCipher


def test_encryption():
    assert AESCipher().encrypt("someplaintext?") == "/cfSnOmMIXCcMUQajOE+Qw=="


def test_decryption():
    assert AESCipher().decrypt("mgtlRNWm40HbZs6xZygemg==") == "secret message"

