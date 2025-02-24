from .crypto import (
    kdfa,
    kdfe,
    public_to_key,
    _get_digest,
    symdef_to_crypt,
)
from .types import *
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.ec import (
    ECDH,
    generate_private_key,
    EllipticCurvePublicKey,
)
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.ciphers import modes, Cipher
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.hashes import HashAlgorithm
from typing import Optional, Tuple, Type

import secrets


def generate_rsa_seed(
    key: RSAPublicKey, hashAlg: int, label: bytes
) -> Tuple[bytes, bytes]:
    halg = _get_digest(hashAlg)
    if halg is None:
        raise ValueError(f"unsupported digest algorithm {hashAlg}")
    seed = secrets.token_bytes(halg.digest_size)
    mgf = padding.MGF1(halg())
    padd = padding.OAEP(mgf, halg(), label)
    enc_seed = key.encrypt(seed, padd)
    return (seed, enc_seed)


def generate_ecc_seed(
    key: EllipticCurvePublicKey, hashAlg: int, label: bytes
) -> Tuple[bytes, bytes]:
    halg = _get_digest(hashAlg)
    if halg is None:
        raise ValueError(f"unsupported digest algorithm {hashAlg}")
    ekey = generate_private_key(key.curve, default_backend())
    epubnum = ekey.public_key().public_numbers()
    plength = int(key.curve.key_size / 8)  # FIXME ceiling here
    exbytes = epubnum.x.to_bytes(plength, "big")
    eybytes = epubnum.y.to_bytes(plength, "big")
    epoint = TPMS_ECC_POINT(
        x=TPM2B_ECC_PARAMETER(buffer=exbytes), y=TPM2B_ECC_PARAMETER(buffer=eybytes)
    )
    secret = epoint.marshal()
    shared_key = ekey.exchange(ECDH(), key)
    pubnum = key.public_numbers()
    xbytes = pubnum.x.to_bytes(plength, "big")
    seed = kdfe(hashAlg, shared_key, label, exbytes, xbytes, halg.digest_size * 8)
    return (seed, secret)


def generate_seed(public: TPMT_PUBLIC, label: bytes) -> Tuple[bytes, bytes]:
    key = public_to_key(public)
    if public.type == TPM2_ALG.RSA:
        return generate_rsa_seed(key, public.nameAlg, label)
    elif public.type == TPM2_ALG.ECC:
        return generate_ecc_seed(key, public.nameAlg, label)
    else:
        raise ValueError(f"unsupported seed algorithm {public.type}")


def hmac(halg: HashAlgorithm, hmackey: bytes, enc_cred: bytes, name: bytes) -> bytes:
    h = HMAC(hmackey, halg(), backend=default_backend())
    h.update(enc_cred)
    h.update(name)
    return h.finalize()


def encrypt(cipher: Type[AES], key: bytes, data: bytes) -> bytes:
    iv = len(key) * b"\x00"
    ci = cipher(key)
    ciph = Cipher(ci, modes.CFB(iv), backend=default_backend())
    encr = ciph.encryptor()
    encdata = encr.update(data) + encr.finalize()
    return encdata


def make_credential(
    public: TPM2B_PUBLIC, credential: bytes, name: TPM2B_NAME
) -> Tuple[TPM2B_ID_OBJECT, TPM2B_ENCRYPTED_SECRET]:
    """Encrypts credential for use with activate_credential

    Args:
        public (TPMT_PUBLIC): The public area of the activation key
        credential (bytes): The credential to be encrypted
        name (bytes): The name of the key associated with the credential

    Returns:
        A tuple of (TPM2B_ID_OBJECT, TPM2B_ENCRYPTED_SECRET)

    Raises:
        ValueError: If the public key type is not supported
    """
    if isinstance(public, TPM2B_PUBLIC):
        public = public.publicArea
    if isinstance(credential, bytes):
        credential = TPM2B_DIGEST(buffer=credential)
    if isinstance(name, TPM2B_SIMPLE_OBJECT):
        name = bytes(name)
    seed, enc_seed = generate_seed(public, b"IDENTITY\x00")

    (cipher, symmode, symbits) = symdef_to_crypt(public.parameters.asymDetail.symmetric)
    symkey = kdfa(public.nameAlg, seed, b"STORAGE", name, b"", symbits)

    enc_cred = encrypt(cipher, symkey, credential.marshal())

    halg = _get_digest(public.nameAlg)
    hmackey = kdfa(public.nameAlg, seed, b"INTEGRITY", b"", b"", halg.digest_size * 8)
    outerhmac = hmac(halg, hmackey, enc_cred, name)
    hmacdata = TPM2B_DIGEST(buffer=outerhmac).marshal()

    credblob = TPM2B_ID_OBJECT(credential=hmacdata + enc_cred)
    secret = TPM2B_ENCRYPTED_SECRET(secret=enc_seed)
    return (credblob, secret)


def wrap(
    newparent: TPMT_PUBLIC,
    public: TPM2B_PUBLIC,
    sensitive: TPM2B_SENSITIVE,
    symkey: Optional[bytes] = None,
    symdef: Optional[TPMT_SYM_DEF_OBJECT] = None,
) -> Tuple[TPM2B_DATA, TPM2B_PRIVATE, TPM2B_ENCRYPTED_SECRET]:
    """Wraps key under a TPM key hierarchy

    Args:
        newparent (TPMT_PUBLIC): The public area of the parent
        public (TPM2B_PUBLIC): The public area of the key
        sensitive (TPM2B_SENSITIVE): The sensitive area of the key
        symkey (bytes or None): Symmetric key for inner encryption. Defaults to None. When None
        and symdef is defined a key will be generated based on the key size for symdef.
        symdef (TPMT_SYMDEF_OBJECT): Symmetric algorithm to be used for inner encryption. This should
        be set to aes128CFB since that is what the TPM supports:
        TPMT_SYM_DEF(
          algorithm=TPM2_ALG.AES,
          keyBits=TPMU_SYM_KEY_BITS(sym=128),
          mode=TPMU_SYM_MODE(sym=TPM2_ALG.CFB),
        )

    Returns:
        A tuple of (TPM2B_DATA, TPM2B_PRIVATE, TPM2B_ENCRYPTED_SECRET) which is the encryption key, the
        the wrapped duplicate and the encrypted seed.

    Raises:
        ValueError: If the public key type or symmetric algorithm are not supported
    """
    enckeyout = TPM2B_DATA()
    outsymseed = TPM2B_ENCRYPTED_SECRET()
    sensb = sensitive.marshal()
    name = bytes(public.get_name())
    if symdef and symdef.algorithm != TPM2_ALG.NULL:
        cipher, mode, bits = symdef_to_crypt(symdef)
        if not symkey:
            klen = int(bits / 8)
            symkey = secrets.token_bytes(klen)
        halg = _get_digest(public.publicArea.nameAlg)
        h = hashes.Hash(halg(), backend=default_backend())
        h.update(sensb)
        h.update(name)
        innerint = TPM2B_DIGEST(buffer=h.finalize()).marshal()
        encsens = encrypt(cipher, symkey, innerint + sensb)
        enckeyout.buffer = symkey
    else:
        encsens = sensb

    seed, outsymseed.secret = generate_seed(newparent, b"DUPLICATE\x00")
    cipher, _, bits = symdef_to_crypt(newparent.parameters.asymDetail.symmetric)
    outerkey = kdfa(newparent.nameAlg, seed, b"STORAGE", name, b"", bits)
    dupsens = encrypt(cipher, outerkey, encsens)

    halg = _get_digest(newparent.nameAlg)
    hmackey = kdfa(
        newparent.nameAlg, seed, b"INTEGRITY", b"", b"", halg.digest_size * 8
    )
    outerhmac = hmac(halg, hmackey, dupsens, name)
    hmacdata = TPM2B_DIGEST(buffer=outerhmac).marshal()

    duplicate = TPM2B_PRIVATE(buffer=hmacdata + dupsens)

    return (enckeyout, duplicate, outsymseed)
