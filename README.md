#  Transformare Regex in DFA

Transforma expresii regulate in DFA si testeaza eficient siruri de intrare.  
Proiect simplu, educativ si robust pentru teoria limbajelor formale si automate.

---

##  Functionalitati

1.  Parsare expresii regulate
2.  Inserare concatenare explicita
3.  Conversie in postfix (notatie poloneza inversa)
4.  Constructie NFA (Automat Finit Nedeterminist)
5.  Conversie NFA ➜ DFA
6.  Verificare siruri pe DFA
7.  Raportare cazuri incorecte

---

##  Structura Proiectului
├── LFA-Assignment2 #Scriptul principal  
├── LFA-Assignment2_Regex_DFA_v2.json #Teste

---

##  Cum se ruleaza

1. Asigura-te ca ai **Python 3** instalat.
2. Cloneaza acest repo.
3. Ruleaza scriptul:
   ``` python LFA-Assignment2.py ```
4. Introdu numele fisierului JSON cu testele (fara extensie .json), sau apasa Enter pentru a folosi implicitul:   

---

## Exemplu de fisier json:
```
[
  {
    "regex": "a(b|c)*",
    "test_strings": [
      { "input": "a", "expected": true },
      { "input": "ab", "expected": true },
      { "input": "accc", "expected": true },
      { "input": "b", "expected": false }
    ]
  }
]
```

---

## Decizii de Implementare

1. Concatenare explicita: Inseram simbolul . intre caractere adiacente care implica concatenare (ab ➜ a.b)
2. Forma postfixata: Transformam expresia in postfix pentru a usura constructia NFA
3. Automate finite: NFA-ul este construit recursiv pe baza postfixului, apoi transformat in DFA folosind algoritmul subset construction
4. Folosirea frozenset: Starile DFA sunt identificate unic prin frozenset de stari NFA
