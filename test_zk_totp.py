import unittest
from time import sleep
from petlib.ec import EcGroup
from zk_totp import ZK_TOTP


class TestZK_TOTP(unittest.TestCase):
    def setUp(self):
        self.group = ZK_TOTP(EcGroup())

    def test_proof_verification(self):
        message = "Hello, world!"

        # Generate proof
        R, s, timestamp = self.group.generate_proof(message)

        # Verify proof with a valid time window
        self.assertTrue(
            self.group.verify_proof(message, R, s, timestamp, time_window=30)
        )

        # Verify proof with an expired time window
        sleep(2)  # Simulate a 2-second delay
        self.assertFalse(
            self.group.verify_proof(message, R, s, timestamp, time_window=1)
        )

    def test_invalid_proof(self):
        message = "Hello, world!"
        other_group = ZK_TOTP(EcGroup())  # Create another SchnorrProof instance

        # Generate proof from another group
        R, s, timestamp = other_group.generate_proof(message)

        # Verify the proof with the original group
        self.assertFalse(
            self.group.verify_proof(message, R, s, timestamp, time_window=30)
        )

    def test_timeout_verification(self):
        message = "Hello, world!"

        # Generate proof with a timestamp
        R, s, timestamp = self.group.generate_proof(message)

        # Wait for a longer time than the time window
        sleep(7)  # Simulate a 7-second delay

        # Verify proof with a time window, expecting failure due to timeout
        self.assertFalse(
            self.group.verify_proof(message, R, s, timestamp, time_window=5)
        )


if __name__ == "__main__":
    unittest.main()
