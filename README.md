# Cipher-65 : Mini Block Cipher Algorithm (SPN)

## Description du projet
Ce projet consiste à concevoir et implémenter un **Mini Block Cipher** comme système cryptographique éducatif.  
Le cipher utilise une structure SPN (Substitution-Permutation Network) pour illustrer les concepts de **confusion et diffusion** des chiffrements symétriques.  

**Objectifs :**
- Comprendre la structure des ciphers réels comme AES et DES.
- Expérimenter avec S-Box, P-Box, Mix-MDS et key scheduling.
- Tester la sécurité statistique du chiffrement (entropy, SAC, corrélation, Hamming distance).

---

## Structure de l’algorithme

1. **S-Box (Substitution Box)**
   - Remplace chaque nibble (4 bits) selon une table prédéfinie.
   - Assure la **confusion**.

2. **P-Box (Permutation Box)**
   - Réorganise les bits du bloc pour assurer la **diffusion**.

3. **Mix-MDS**
   - Mélange linéaire fort basé sur ROT et XOR.
   - Similaire à MixColumns dans AES.

4. **Key Expansion**
   - Génère 9 sous-clés à partir de la clé maître via rotation.

5. **Chiffrement (Encrypt)**
   - Initial XOR avec la sous-clé 0.
   - 8 rounds : S-Box → P-Box → Mix-MDS → XOR sous-clé.

6. **Déchiffrement (Decrypt)**
   - Rounds inverses avec les sous-clés et fonctions inverses.

---

## Analyse statistique

| Metric | Symbole | Interprétation |
|--------|--------|----------------|
| Shannon Entropy | H(X) | Mesure de l’aléatoire du ciphertext, idéal proche de 4 |
| Corrélation | rxy | Corrélation entre plaintext et ciphertext, idéal proche de 0 |
| Strict Avalanche | SAC | % de bits modifiés si 1 bit du plaintext change, idéal 50% |
| Hamming Distance | H | Nombre de bits différents entre plaintext et ciphertext |
| Fréquence | Sn | Vérifie équilibre entre 0s et 1s |
| Temps | µs | Temps pour 100 chiffrement/déchiffrement |

---

## Exemples de sortie

```text
Clé: 0x0123456789ABCDEF | Message: 0x1122334455667788
Chiffré: 0xA1B2C3D4E5F67890
Temps d'exécution : 1234.56 µs
Test de Fréquence Sn : -2 (Biais faible)
Corrélation rxy : 0.0032
Entropie H(X) : 3.98
SAC (Avalanche) : 49.12%
Distance de Hamming : 32 bits