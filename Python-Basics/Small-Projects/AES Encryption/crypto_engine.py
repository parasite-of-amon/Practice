
from __future__ import annotations
import os
import secrets
from typing import Optional, Callable

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

MAGIC = b"ME\x01\x00"
VERSION = 1
SALT_LEN = 16
NONCE_LEN = 12
TAG_LEN = 16
PBKDF2_ITERS = 300_000
KEY_LEN = 32
CHUNK_SIZE = 1024 * 1024  # 1 MiB


class CryptoError(Exception):
    """UI-friendly crypto error."""


def _derive_key(password: str, salt: bytes) -> bytes:
    if not isinstance(password, str) or not password:
        raise CryptoError("Secret key (password) cannot be empty.")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LEN,
        salt=salt,
        iterations=PBKDF2_ITERS,
    )
    return kdf.derive(password.encode("utf-8"))


def _default_out_path(in_path: str, mode: str) -> str:
    directory, fname = os.path.split(in_path)
    if mode == "encrypt":
        return os.path.join(directory, fname + ".enc")
    else:
        if fname.lower().endswith(".enc"):
            fname = fname[: -4]
        else:
            fname = fname + ".dec"
        return os.path.join(directory, fname)


def encrypt_file(
    password: str,
    in_path: str,
    out_path: Optional[str] = None,
    progress: Optional[Callable[[float], None]] = None,
    is_cancelled: Optional[Callable[[], bool]] = None,
) -> str:
    """
    Stream-encrypt a file with AES-256-GCM.
    - progress: callback receiving 0..1
    - is_cancelled: callback returning True to abort
    Returns output path.
    """
    if not os.path.isfile(in_path):
        raise CryptoError("Input file not found.")

    out_path = out_path or _default_out_path(in_path, "encrypt")
    if os.path.abspath(in_path) == os.path.abspath(out_path):
        raise CryptoError("Input and output paths cannot be the same.")

    total = os.path.getsize(in_path)
    done = 0

    salt = secrets.token_bytes(SALT_LEN)
    nonce = secrets.token_bytes(NONCE_LEN)
    key = _derive_key(password, salt)

    try:
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce))
        encryptor = cipher.encryptor()
    except Exception as e:
        raise CryptoError(f"Encryption init failed: {e}")

    try:
        with open(in_path, "rb") as f_in, open(out_path, "wb") as f_out:
            # Header
            f_out.write(MAGIC)
            f_out.write(bytes([VERSION]))
            f_out.write(salt)
            f_out.write(nonce)

            if progress:
                progress(0.0)

            while True:
                if is_cancelled and is_cancelled():
                    raise CryptoError("Operation cancelled.")
                chunk = f_in.read(CHUNK_SIZE)
                if not chunk:
                    break
                ct_chunk = encryptor.update(chunk)
                if ct_chunk:
                    f_out.write(ct_chunk)

                done += len(chunk)
                if progress:
                    progress(min(done / total if total else 1.0, 0.999))

            # Finalize + tag
            ct_final = encryptor.finalize()
            if ct_final:
                f_out.write(ct_final)
            f_out.write(encryptor.tag)

        if progress:
            progress(1.0)

    except CryptoError:
        # Cleanup partial output on cancel or crypto error
        try:
            if os.path.exists(out_path):
                os.remove(out_path)
        except Exception:
            pass
        raise
    except Exception as e:
        try:
            if os.path.exists(out_path):
                os.remove(out_path)
        except Exception:
            pass
        raise CryptoError(f"Encryption failed: {e}")

    return out_path


def decrypt_file(
    password: str,
    in_path: str,
    out_path: Optional[str] = None,
    progress: Optional[Callable[[float], None]] = None,
    is_cancelled: Optional[Callable[[], bool]] = None,
) -> str:
    """
    Stream-decrypt a file previously produced by encrypt_file.
    - progress: callback receiving 0..1
    - is_cancelled: callback returning True to abort
    Returns output path.
    """
    if not os.path.isfile(in_path):
        raise CryptoError("Input file not found.")

    try:
        with open(in_path, "rb") as f:
            header = f.read(len(MAGIC) + 1 + SALT_LEN + NONCE_LEN)
    except Exception as e:
        raise CryptoError(f"Failed to read file: {e}")

    if len(header) != len(MAGIC) + 1 + SALT_LEN + NONCE_LEN:
        raise CryptoError("File is too short or corrupted.")

    off = 0
    if header[off:off + len(MAGIC)] != MAGIC:
        raise CryptoError("Invalid file format (magic mismatch).")
    off += len(MAGIC)
    version = header[off]; off += 1
    if version != VERSION:
        raise CryptoError(f"Unsupported version: {version}.")
    salt = header[off:off + SALT_LEN]; off += SALT_LEN
    nonce = header[off:off + NONCE_LEN]; off += NONCE_LEN

    key = _derive_key(password, salt)

    file_size = os.path.getsize(in_path)
    header_len = len(MAGIC) + 1 + SALT_LEN + NONCE_LEN
    if file_size < header_len + TAG_LEN:
        raise CryptoError("Corrupted file: missing authentication tag.")
    ct_len = file_size - header_len - TAG_LEN

    # Read tag
    try:
        with open(in_path, "rb") as f:
            f.seek(file_size - TAG_LEN)
            tag = f.read(TAG_LEN)
    except Exception:
        raise CryptoError("Failed to read authentication tag.")

    try:
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag))
        decryptor = cipher.decryptor()
    except Exception as e:
        raise CryptoError(f"Decryption init failed: {e}")

    out_path = out_path or _default_out_path(in_path, "decrypt")
    if os.path.abspath(in_path) == os.path.abspath(out_path):
        raise CryptoError("Input and output paths cannot be the same.")

    processed = 0
    try:
        with open(in_path, "rb") as f_in, open(out_path, "wb") as f_out:
            f_in.seek(header_len)

            if progress:
                progress(0.0)

            remaining = ct_len
            while remaining > 0:
                if is_cancelled and is_cancelled():
                    raise CryptoError("Operation cancelled.")
                to_read = CHUNK_SIZE if remaining >= CHUNK_SIZE else remaining
                chunk = f_in.read(to_read)
                if not chunk:
                    raise CryptoError("Unexpected EOF while reading ciphertext.")
                pt_chunk = decryptor.update(chunk)
                if pt_chunk:
                    f_out.write(pt_chunk)

                processed += len(chunk)
                remaining -= len(chunk)
                if progress:
                    denom = ct_len if ct_len else 1
                    progress(min(processed / denom, 0.999))

            pt_final = decryptor.finalize()
            if pt_final:
                f_out.write(pt_final)

        if progress:
            progress(1.0)

    except CryptoError:
        try:
            if os.path.exists(out_path):
                os.remove(out_path)
        except Exception:
            pass
        raise
    except Exception:
        try:
            if os.path.exists(out_path):
                os.remove(out_path)
        except Exception:
            pass
        # Keep generic for safety
        raise CryptoError("Decryption failed. The secret key may be incorrect or the file is corrupted.")

    return out_path
