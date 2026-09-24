# Security Tools
## Password Strength Analyzer

Estimate password strength locally without storing or transmitting input. Run it as `pyforge run security.password-strength --arguments '{...}'` or select it from the interactive menu.
## File Hash Checker

Compare a local file digest against an expected value. Run it as `pyforge run security.file-hash-checker --arguments '{...}'` or select it from the interactive menu.
## File Entropy Analyzer

Calculate Shannon entropy for local file bytes. Run it as `pyforge run security.file-entropy --arguments '{...}'` or select it from the interactive menu.
## Basic Secret Pattern Detector

Find and redact likely accidental credentials in text. Run it as `pyforge run security.secret-detector --arguments '{...}'` or select it from the interactive menu.
## Permission Inspector

Explain local file mode bits and risky world-writable access. Run it as `pyforge run security.permissions --arguments '{...}'` or select it from the interactive menu.
## Environment Secret Warning

Identify sensitive environment names while redacting all values. Run it as `pyforge run security.environment-warning --arguments '{...}'` or select it from the interactive menu.
## Security Header Analyzer

Evaluate defensive HTTP response headers supplied by the user. Run it as `pyforge run security.security-headers --arguments '{...}'` or select it from the interactive menu.
## TLS Certificate Information Viewer

Inspect the certificate presented by an authorized TLS host. Run it as `pyforge run security.tls-certificate --arguments '{...}'` or select it from the interactive menu.
