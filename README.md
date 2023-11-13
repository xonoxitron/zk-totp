# zk-totp - Zero-Knowledge Proof Time-Based One-Time Passwords 🔐⌛

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Decription

This repository implements a Python implementation of Zero-Knowledge Proof Time-Based One-Time Passwords (ZK-TOTP) using the petlib library.

## Installation

Make sure you have Python installed on your system. You can install the required dependencies using the following command:


## Usage

### Prerequisites

- Python >= 3.10
- petlib library (install using `pip install petlib` or visit [petlib](https://github.com/gdanez/petlib) for further details)

```bash
pip install -r requirements.txt
```

### Example

```python
from petlib.ec import EcGroup
from zk_totp import ZK_TOTP

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
```

### Running Tests

To run the tests, execute the following command:

```bash
python -m unittest test_zk_totp.py
```

## Contributing

Feel free to contribute by opening issues or submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.