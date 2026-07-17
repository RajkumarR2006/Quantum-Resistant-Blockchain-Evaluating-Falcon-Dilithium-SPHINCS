# Quantum-Resistant Blockchain: Evaluating Falcon, Dilithium & SPHINCS+

![IEEE Acceptance](https://img.shields.io/badge/IEEE_IATMSI--2026-Accepted_Oral_Presentation-blue)
![Python 3.10](https://img.shields.io/badge/Python-3.10-green)

## 📌 Abstract
Up to date blockchain protocols primarily depend on digital signature schemes like RSA and ECC, that are built on traditional cryptography[cite: 6]. These cryptography algorithms are at risk by quantum algorithms such as Shor's and Grover's, that form part of the latest advances in quantum computing[cite: 6]. To mitigate this risk of vulnerability, post-quantum cryptography (PQC) techniques that are safe from both classical and quantum attacks must be used[cite: 6]. This project evaluates post-quantum digital signature schemes in blockchain protocols to show how PQC reduces the threat of quantum adversaries and enables the development of secure, decentralized financial systems[cite: 6].

## 🏗️ The Hybrid Cryptographic Model
To balance day-to-day efficiency with worst-case resilience, this system explores a hybrid cryptographic model[cite: 6]:
*   A fast, compact algorithm like Falcon is used for routine transactions to keep latency and storage costs low[cite: 6].
*   A more conservative and computationally heavier algorithm, SPHINCS+, is reserved as a fallback for critical operations or when a compromise is suspected[cite: 6].
*   This approach allows the system to operate efficiently under normal conditions yet retain an extra layer of protection for high-value or emergency scenarios[cite: 6].

## 🔬 Methodology & Experimental Setup
The framework features a mock blockchain testbed developed in Python, integrating classical (RSA-2048, ECC-256) and post-quantum (Falcon-512, Dilithium2, SPHINCS+) cryptographic schemes[cite: 6]. 

*   **Architecture:** Features modular pluggable signature algorithms, block creation with SHA-256 hashing, adjustable Proof-of-Work, and a hybrid signing protocol[cite: 6].
*   **Hardware Setup:** Simulations were performed on an Intel(R) Core(TM) i5-1035G1 processor (1.00 GHz) with 4 physical cores, 8 logical threads, and 8.00 GB of DDR4 RAM[cite: 6].
*   **Software Environment:** Executed on Windows 11 Pro (Version 23H2) using Python 3.10 and the `liboqs-python` (v0.12.0) library[cite: 6].
*   **Measurement Protocol:** Each cryptographic operation (Key Generation, Signing, Verification) was executed for 10,000 iterations to capture the arithmetic mean and standard deviation[cite: 6].

## 📊 Performance Results

### End-to-End Latency & Throughput
The post-quantum lattice-based algorithms achieved the lowest latencies and highest throughputs in the test environment[cite: 6].

| Algorithm | End-to-End Latency (ms) | Throughput (tx/s) |
| :--- | :--- | :--- |
| **RSA-2048** | 51.50 | 152.50 |
| **ECC-256** | 2.74 | 324.24 |
| **Dilithium** | 1.17 | 720.23 |
| **Falcon** | 1.20 | 784.14 |
| **SPHINCS+** | 6.98 | 140.65 |

*Note: Data derived from 10,000 iterations per operation[cite: 6].*

### Storage Requirements (Key and Signature Size)
Classical methods require less disk space, but offer no quantum security[cite: 6]. Among the quantum-safe methods, Falcon proved to be the most optimal for conserving bandwidth[cite: 6].

| Algorithm | Public Key Size (Bytes) | Signature Size (Bytes) |
| :--- | :--- | :--- |
| **RSA-2048** | 270 | 256 |
| **ECC-256** | 64 | 64 |
| **Dilithium2** | 1312 | 2420 |
| **SPHINCS+** | 32 | 7856 |
| **Falcon-512** | 897 | 666 |

## 🚀 Future Work
Falcon offers superior performance in speed and size due to its tunable security parameters, while SPHINCS+ ranks highest in pure quantum resistance[cite: 6]. Future work will focus on transitioning this mock testbed into a real-world, active blockchain environment to assess system-wide effects[cite: 6]. This includes analyzing how larger PQC signature sizes impact block propagation time, fork chances, and state bloat, as well as examining side-channel resiliency of Falcon's floating-point arithmetic[cite: 6].
