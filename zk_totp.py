from petlib.ec import EcGroup
from petlib.bn import Bn
from hashlib import sha256
from time import time


class ZK_TOTP:
    def __init__(self, group):
        self.group = group
        self.sk = group.order().random()
        self.pk = self.sk * group.generator()

    def generate_challenge(self, msg, timestamp):
        h = sha256((msg + str(timestamp)).encode()).digest()
        return Bn.from_binary(h) % self.group.order()

    def generate_proof(self, msg):
        timestamp = int(time())
        r = self.group.order().random()
        R = r * self.group.generator()
        c = self.generate_challenge(msg, timestamp)
        s = (r + c * self.sk) % self.group.order()
        return (R, s, timestamp)

    def verify_proof(self, msg, R, s, timestamp, time_window=30):
        current_time = int(time())
        if abs(current_time - timestamp) > time_window:
            print("Timestamp is outside the acceptable time window.")
            return False

        c = self.generate_challenge(msg, timestamp)
        left = s * self.group.generator()
        right = R + c * self.pk
        return left == right


def test_proof():
    group = EcGroup()
    zk_totp = ZK_TOTP(group)

    message = "Hello, world!"

    # Generate proof
    R, s, timestamp = zk_totp.generate_proof(message)

    # Verify proof with a time window of 30 seconds
    if zk_totp.verify_proof(message, R, s, timestamp, time_window=30):
        print("Proof is valid.")
    else:
        print("Proof is invalid.")


if __name__ == "__main__":
    test_proof()
