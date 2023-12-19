# Zkouška 23/24

- 5 příkladů na různá kódování: Huffmanovo, Aritmetické, LZW, MTF, BWT

## Huffmanovo kódování
### Kódování
1. Zjisti relativní četnosti znaků
   - např. pro ABRAKADABRA jsou četnosti:
     - A (5x - 0,46)
     - B (2x - 0,18)
     - R (2x - 0,18)
     - K (1x - 0,09)
     - D (1x - 0,09)
2. Vytvoř tabulku dle četností
3. Posledním dvěma slovům přiřad číslo
    - jedna pokud má vyšší pravděpodobnost,
    - nula pokud má nižší pravděpodobnost
    
4. Tyto dvě poslední četnosti se sečtou a vytvoří se z nich nové slovo
![obrazek](https://github.com/Bahamut731lp/MT/assets/27443880/c05dd349-35f8-4e1c-8120-1a4e2cc71b12)

5. Opakuj bod 3 až 5, dokud ti nezbydou pouze dvě slova
6. Vytvoř výsledné kódy tak, že jdeš z pravé strany tabulky doleva a píšeš čísla, ve kterých je písmeno obsaženo, dokud nedojdeš k jemu samotnému
  - Např. písmeno R má kód 1 (KBDR) 0 (R)
  - Např. písmeno B má kód 1 (KBDR) 1 (KBD) 1 (B)
  - Např. písmeno A má kód 0 (A)
  - ...

7. Nahraď jednotlivé znaky výslednými kódy

### Dekódování
1. Musíš mít slovník znaků a jakým kódům odpovídají
2. Hledej nejdelší sekvenci, která odpovídá nějakému znaku
3. Tu zapiš a pokračuj s dekódováním


#
