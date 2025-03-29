# Drzewka — AVL, BST, HMIN

Projekt w języku Python umożliwiający budowę i operacje na strukturach drzewiastych: AVL, BST oraz kopcu minimalnym (HMIN). Program obsługuje dane wejściowe z klawiatury i plików, a także oferuje szereg funkcji diagnostycznych i analitycznych.

---

## Funkcje zaimplementowane

- Budowa drzew:
  - BST (algorytm FCFS — First Come First Served)
  - AVL (z użyciem bisekcji, z wcześniej posortowanej listy)
  - HMIN (kopiec minimalny jako drzewo + heapsort)

- Operacje na drzewach:
  - Wyszukiwanie minimum i maksimum wraz ze ścieżką
  - Sprawdzenie poziomu węzła i wypisanie wszystkich elementów na tym poziomie
  - Wypisanie elementów w porządku malejącym
  - Preorder, obliczenie wysokości i usunięcie poddrzewa wskazanego przez użytkownika
  - Wizualizacja drzewa w konsoli

- Interfejs:
  - Menu tekstowe
  - Obsługa danych z klawiatury i pliku

---

## Funkcje do zaimplementowania

- [ ] Algorytm równoważenia drzewa BST (DSW lub usuwanie korzenia)
- [ ] Preorder drzewa **przed i po** zrównoważeniu
- [ ] Pomiar czasu działania operacji:
  - Tworzenie drzewa
  - Wyszukiwanie elementu maksymalnego
  - Równoważenie drzewa BST
- [ ] Generator danych testowych:
  - Ciągi losowe
  - Ciągi posortowane
- [ ] Automatyczne testy porównawcze dla różnych `n`
- [ ] Eksport wyników testów

---
