# Feistel Cipher URL Shortener

A collision-free URL shortener that obfuscates auto-incremented database IDs using a symmetric Feistel cipher before Base62 encoding. This prevents URL enumeration attacks and business metric leaks without the database overhead of hash-collision checks.

## Core Design

1. **Write Path:** Long URL $\rightarrow$ DB Insert $\rightarrow$ Sequential ID (e.g., `105`) $\rightarrow$ Feistel Cipher $\rightarrow$ Scrambled ID (e.g., `94820`) $\rightarrow$ Base62 Encode $\rightarrow$ Short Code (`b9X`).
2. **Read Path:** Short Code (`b9X`) $\rightarrow$ Base62 Decode $\rightarrow$ Scrambled ID (`94820`) $\rightarrow$ Inverse Feistel $\rightarrow$ Sequential ID (`105`) $\rightarrow$ Direct DB Primary Key Lookup.

By using a bijective (one-to-one) format-preserving cipher, the system guarantees zero ID collisions, eliminating the need for iterative "loop-and-check" database queries during URL generation.

## Architectural Trade-Offs

* **Why Feistel + Base62:** Traditional hashing algorithms (MD5/SHA) cause collisions that require expensive database lookups at scale. Exposing raw sequential IDs invites scraping. This approach balances $O(1)$ database lookup speeds with cryptographic obfuscation.
* **Limitations:** Introduces minor CPU overhead for bitwise operations per request. The block size must be constrained to keep the encoded output string short.

## Mathematical Core

The cipher splits the integer bit-block into left ($L$) and right ($R$) halves, executing over $i$ rounds:

$$L_i = R_{i-1}$$
$$R_i = L_{i-1} \oplus F(R_{i-1}, K_i)$$

The round function $F$ utilizes a pseudo-random bit-shuffling mechanism driven by a static internal key $K$.
