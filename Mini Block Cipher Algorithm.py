import time
import math
import numpy as np
from collections import Counter


SBOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
SBOX_INV = [SBOX.index(x) for x in range(16)]


PBOX = [
    15, 6, 19, 21, 54, 43, 33, 0, 61, 48, 22, 1, 38, 49, 11, 2,
    50, 27, 4, 35, 62, 13, 28, 7, 44, 18, 59, 32, 5, 56, 10, 39,
    17, 42, 53, 24, 8, 45, 20, 57, 12, 63, 3, 36, 31, 55, 26, 9,
    51, 14, 41, 23, 60, 25, 46, 30, 16, 37, 58, 47, 52, 29, 40, 34
]
PBOX_INV = [PBOX.index(x) for x in range(64)]



def rot_l(val, shift, bits=64):
    """Opération de Rotation Circulaire Gauche (ROT)"""
    return ((val << shift) & ((1 << bits) - 1)) | (val >> (bits - shift))

def apply_sbox(state, box):
    """Substitution : utilise AND pour isoler les nibbles de 4 bits"""
    res = 0
    for i in range(16):
        nibble = (state >> (i * 4)) & 0xF  # Opération AND masque
        res |= (box[nibble] << (i * 4))
    return res

def apply_pbox(state, box):
    """Permutation bit à bit"""
    res = 0
    for i in range(64):
        bit = (state >> i) & 1
        res |= (bit << box[i])
    return res

def mix_mds(state):
    """Fonction de mélange MDS utilisant XOR et ROT"""
   
    state = state ^ rot_l(state, 13)
    state = state ^ rot_l(state, 33)
    return state & 0xFFFFFFFFFFFFFFFF

def key_expansion(master_key):
    """Génération de 9 sous-clés via l'opération ROT_KEY"""
    subkeys = []
    current_key = master_key
    for i in range(9):
        subkeys.append(current_key)
        current_key = rot_l(current_key, 7) 
    return subkeys



def encrypt(plaintext, key):
    subkeys = key_expansion(key)
    
    state = plaintext ^ subkeys[0]
    
   
    for i in range(1, 9):
        state = apply_sbox(state, SBOX)
        state = apply_pbox(state, PBOX)
        state = mix_mds(state)
        state = state ^ subkeys[i]
    return state

def decrypt(ciphertext, key):
    subkeys = key_expansion(key)
    state = ciphertext
    for i in range(8, 0, -1):
        state = state ^ subkeys[i]
        state = mix_mds(state)
        state = apply_pbox(state, PBOX_INV)
        state = apply_sbox(state, SBOX_INV)
    return state ^ subkeys[0]

def run_full_analysis(plain, key):
    start = time.perf_counter()
    for _ in range(100):
      cipher = encrypt(plain, key)
      decrypt(cipher, key)

    end = time.perf_counter()
    exec_time = (end - start) * 1_000_000

    bits = [(cipher >> i) & 1 for i in range(64)]
    sn = sum([1 if b == 1 else -1 for b in bits])

    p_bits = np.array([(plain >> i) & 1 for i in range(64)])
    c_bits = np.array([(cipher >> i) & 1 for i in range(64)])
    correlation = np.corrcoef(p_bits, c_bits)[0, 1]
   
    hex_c = format(cipher, '016x')
    counts = Counter(hex_c)
    entropy = -sum((count/16) * math.log2(count/16) for count in counts.values())

    total_flipped = 0
    for i in range(64):
        c_mod = encrypt(plain ^ (1 << i), key)
        total_flipped += bin(cipher ^ c_mod).count('1')
    sac_score = (total_flipped / (64 * 64)) * 100
    return {
        "cipher": cipher,
        "time": exec_time,
        "sn": sn,
        "rxy": correlation,
        "entropy": entropy,
        "sac": sac_score,
        "hamming": bin(plain ^ cipher).count('1')
    }


if __name__ == "__main__":
    m_key = 0x0123456789ABCDEF
    m_text = 0x1122334455667788
    
    res = run_full_analysis(m_text, m_key)
    
    print(f"--- RÉSULTATS MINI-PROJET #65 ---")
    print(f"Clé: {hex(m_key)} | Message: {hex(m_text)}")
    print(f"Chiffré: {hex(res['cipher'])}")
    print(f"-"*40)
    print(f"1. Temps d'exécution : {res['time']:.2f} µs")
    print(f"2. Test de Fréquence Sn : {res['sn']} (Biais des bits)")
    print(f"3. Corrélation rxy : {res['rxy']:.4f} (Proche de 0 = Idéal)")
    print(f"4. Entropie H(X) : {res['entropy']:.4f}")
    print(f"5. SAC (Avalanche) : {res['sac']:.2f}% (Idéal: 50%)")
    print(f"6. Distance de Hamming : {res['hamming']} bits")