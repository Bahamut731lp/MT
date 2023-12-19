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
2. Vytvoř tabulku dle četností, seřaď je od nejvyšší četnosti po nejnižší
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

## Aritmetické kódování
### Kódování
1. Zjisti relativní četnosti znaků
2. Rozděl interval $\left<0,1\right)$ podle kumulativní pravděpodobnosti
   - Např. CBAABCADAC (A - 0.4, B - 0.2, C - 0.3, D - 0.1)
   - A = $\left<0, 0.4\right)$, B = $\left<0.4, 0.6\right)$, C = $\left<0.4, 0.9\right)$, D = $\left<0.9, 1\right)$
3. Postupně ber znaky z výchozího řetězce a omezuj interval $I = \left<0, 1\right)$
   - Známe interval, ve kterém se nachází znak => IZ = <ZL, ZH)
   - Nový interval IN = <L + ZL * (H - L), L + ZH * (H - L))
   - Výsledný interval použij v dalším kroku pro $L$ a $H$
5. Po zakódování všech znaků vyber střední hodnotu výsledného intervalu

### Dekódování
1. Vstupem je číslo $C$ v intervalu $\left<0, 1\right)$
2. Zjisti $K = (C - L) / (H - L)$
3. Zjisti, do intervalu IZ = <ZL, ZH) jakého znaku patří $K$
4. Spočítej nový interval IN = <L + ZL * (H - L), L + ZH * (H - L)

## LZW
### Kódování
1. Vypiš použité znaky ve výchozím řetězci a přiřaď jim čísla (např. pro řetězec abcabcabcabcbcba jsou použité znaky a = 1, b = 2, c = 3)
2. Najdi nejdelší frázi na vstupu, která existuje ve slovníku, na výstup napiš její číslo (v prvním kroku to je a = 1, výstupem je jedna)
3. Vytvoř novou frázi, která vznikne nalezenou frází a přidáním jednoho dalšího znaku ze vstupu
4. Této nové frázi přiřaď číslo

![obrazek](https://github.com/Bahamut731lp/MT/assets/27443880/b5d66417-ae57-4190-9282-db2dfd1009ed)

### Dekódování
1. Přiřaď k číslům abecedu, např. pro vstup 1234567891 bude a = 1, b = 2, c = 3
2. Zjisti, jaká fráze je k číslu přiřazena (např. 1 = a)
3. Vytvoř novou frázi tak, že vezmeš frázi z předchozího kroku a první znak fráze výstupu (v prvním kroku se tedy nedělá)
4. Pokud je číslo na vstupu větší než jakákoliv fráze ve slovníku, tak je *výstupem minulá fráze + její první znak*

![obrazek](https://github.com/Bahamut731lp/MT/assets/27443880/94248eea-cba1-4ebf-93f1-f03cde8f45c7)

## MTF
### Kódování
1. Vytvoř si abecedu, např. "abcdefghijklmnopqrstvwxyz"
2. Postupně ber znaky z výchozí řetězce
   - Najdi, na kolikátém místě je písmeno v abecedě (index)
   - tohle číslo si zapiš do výsledku
   - nalezené písmeno přesuň na začátek abecedy
3. Opakuj bod 2, dokud nemáš zakódovaný celý řetězec

### Dekódování
1. Vytvoř si abecedu, např. "abcdefghijklmnopqrstvwxyz"
2. Postupně ber čísla ze vstupu
   - Číslo říká pořadí v abecedě, takže najdi znak, který má stejné pořadové číslo jako číslo na vstupu
   - Tenhle znak si napiš na výstup
   - Nalezený znak přesuň na začátek abecedy
3. Opakuj bod 2, dokud máš čísla na vstupu

## BWT
### Kódování
1. Ze vstupního řetězce vytvoř matici N*N, kde N je délka vstupního řetězce.
   - Každý řádek je posunut o jeden znak doprava oproti tomu předchozímu
2. Tu matici následně lexograficky seřaď (podle abecedy, duh)
3. Poslední sloupec seřazené matice je výsledek zakódování.
4. Poznamenej si, na kolikátem řádku je původní slovo v seřazené matici

![obrazek](https://github.com/Bahamut731lp/MT/assets/27443880/5296948b-38d0-4aa2-b619-828e2b04d7bb)

### Dekódování
1. Vem vstupní řetězec a lexograficky (podle abecedy) ho seřaď
2. Seřazený řetězec připoj za vstupní řetězec
3. Nově vzniklý řetězec znovu seřaď a poslední písmena toho seřazeného přidej na konec neseřazeného
4. Takhle to opakuj, dokud to neuděláš N-krát
5. Na konci vem číslo řádku z kódování a výsledek na tom samém čísle řádku

![obrazek](https://github.com/Bahamut731lp/MT/assets/27443880/d0ee10ec-5b51-4c26-bc9a-fa8ea39f40a3)
