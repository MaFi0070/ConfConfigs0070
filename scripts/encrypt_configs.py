#!/usr/bin/env python3
import os
import sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

INPUT_FILE = "configs.txt"
OUTPUT_FILE = "configs.enc"


def load_key() -> bytes:
    key_hex = os.environ.get("AES_KEY_HEX")
    if not key_hex:
        sys.exit("خطا: متغیر محیطی AES_KEY_HEX ست نشده (باید از GitHub Secret بیاد).")
    key = bytes.fromhex(key_hex.strip())
    if len(key) != 32:
        sys.exit(f"خطا: کلید باید ۳۲ بایت (۶۴ کاراکتر hex) باشه، طول فعلی: {len(key)} بایت.")
    return key


def main() -> None:
    if not os.path.exists(INPUT_FILE):
        sys.exit(f"خطا: {INPUT_FILE} پیدا نشد.")

    key = load_key()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # نانس تصادفی برای هر اجرا

    with open(INPUT_FILE, "rb") as f:
        plaintext = f.read()

    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    with open(OUTPUT_FILE, "wb") as f:
        f.write(nonce + ciphertext)

    print(f"{INPUT_FILE} ({len(plaintext)} بایت) -> {OUTPUT_FILE} ({len(nonce) + len(ciphertext)} بایت) رمز شد.")


if __name__ == "__main__":
    main()
