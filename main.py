import os
import time
import random
import sys

sys.setrecursionlimit(10 ** 6)


# =============================================================================
# Klasa reprezentująca węzeł drzewa
# =============================================================================
class Node:
    def __init__(self, value):
        self.key = value
        self.left = None
        self.right = None


# =============================================================================
# Funkcje do budowania i obsługi drzew (BST, AVL, HMIN)
#
# W tym bloku funkcje operują na obiektach klasy Node.
#
# - Funkcja AVL buduje zbalansowane drzewo (AVL) na podstawie posortowanej listy.
# - Funkcja FCFS tworzy BST według kolejności wstawiania (First-Come, First-Served).
# - Funkcje HMIN budują kopiec minimalny jako drzewo.
# =============================================================================
is_HMIN = False

def AVL(lst):
    """
    Buduje drzewo zbalansowane (AVL) z posortowanej listy.
    Element środkowy listy staje się korzeniem, co gwarantuje (przy równomiernym podziale)
    optymalne zbalansowanie drzewa.

    :param lst: Posortowana lista elementów (rosnąco).
    :return: Korzeń zbudowanego drzewa.
    """
    if not lst:
        return None
    mediana = len(lst) // 2
    node = Node(lst[mediana])
    # Rekurencyjne budowanie lewego i prawego poddrzewa
    node.right = AVL(lst[:mediana])
    node.left = AVL(lst[mediana + 1:])
    return node


def FCFS(root, key):
    """
    Wstawia nowy element do BST metodą FCFS (kolejność przybycia).
    Nie wykonuje operacji równoważenia, przez co struktura drzewa zależy od kolejności wstawiania.

    :param root: Korzeń drzewa.
    :param key: Wstawiany klucz.
    :return: Korzeń drzewa po wstawieniu.
    """
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = FCFS(root.left, key)
    else:
        root.right = FCFS(root.right, key)
    return root


def print_preorder(node):
    """
    Wypisuje elementy drzewa metodą pre-order (korzeń, lewo, prawo).

    :param node: Bieżący węzeł.
    """
    if node is None or node.key is None:
        return
    print(node.key, end=" ")
    print_preorder(node.left)
    print_preorder(node.right)


def szukanie_elementu(node, n):
    """
    Szuka węzła o podanym kluczu w BST.

    :param node: Korzeń drzewa.
    :param n: Klucz szukanego węzła.
    :return: Węzeł o kluczu n lub None, jeśli nie znaleziono.
    """
    if node is None:
        return None
    if node.key == n:
        return node
    elif n < node.key:
        return szukanie_elementu(node.left, n)
    else:
        return szukanie_elementu(node.right, n)


def usuwanie(node):
    """
    Usuwa (dezaktywuje) poddrzewo – symuluje usuwanie przez ustawienie kluczy na None
    i zerwanie referencji do dzieci.

    :param node: Korzeń poddrzewa do usunięcia.
    """
    if node is None:
        return
    usuwanie(node.left)
    usuwanie(node.right)
    node.key = None
    node.left = None
    node.right = None


def wypisanie_preorder_podanie_wysokosci_i_usuniecie_poddrzewa(root, n):
    """
    Dla węzła o danym kluczu:
     - wypisuje preorder jego poddrzewa,
     - podaje wysokość poddrzewa,
     - usuwa to poddrzewo.

    :param root: Korzeń całego drzewa.
    :param n: Klucz, którego poddrzewo chcemy przetworzyć.
    """
    node = szukanie_elementu(root, n)
    if node is None:
        print("Nie znaleziono poddrzewa o korzeniu", n)
        return
    print("Preorder poddrzewa:")
    print_preorder(node)
    print("\nWysokość poddrzewa:", wysokosc(node))
    usuwanie(node)
    print("Poddrzewo usunięte.")


def wysokosc(node):
    """
    Oblicza wysokość drzewa (liczbę krawędzi na najdłuższej ścieżce).

    :param node: Bieżący węzeł.
    :return: Wysokość drzewa.
    """
    if node is None:
        return -1
    return 1 + max(wysokosc(node.left), wysokosc(node.right))


def print_tree(node, prefix="", is_left=True):
    """
    Wizualnie wypisuje strukturę drzewa z użyciem znaków graficznych.

    :param node: Bieżący węzeł.
    :param prefix: Ciąg znaków służący do wcięć (ułatwia wizualizację struktury).
    :param is_left: Flaga określająca, czy bieżący węzeł jest lewym dzieckiem.
    """
    if node is not None and node.key is not None:
        print_tree(node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + str(node.key))
        print_tree(node.left, prefix + ("    " if is_left else "│   "), True)


def znajdz_min_i_max(node):
    """
    Znajduje ścieżki (od korzenia) do najmniejszego i największego elementu w BST.
    W drzewie BST minimum znajduje się na skrajnym lewym, a maksimum na skrajnym prawym.

    :param node: Korzeń drzewa.
    :return: Dwie listy – ścieżka do min i ścieżka do max.
    """
    path_min, path_max = [], []
    current = node
    if is_HMIN:
        path_min = [node.key]
    else:
        while current:
            path_min.append(current.key)
            current = current.left
        current = node
    while current:
        path_max.append(current.key)
        current = current.right
    return path_min, path_max


def poziom_i_elementy_na_poziomie(root, key):
    """
    Znajduje poziom (głębokość) węzła o danym kluczu oraz wypisuje wszystkie elementy
    znajdujące się na tym samym poziomie. Przeszukiwanie odbywa się metodą BFS (przeszukiwanie wszerz).

    :param root: Korzeń drzewa.
    :param key: Klucz, którego poziom chcemy ustalić.
    :return: Krotka (poziom, lista elementów na tym poziomie).
    """
    if not root:
        return -1, []
    queue = [(root, 0)]  # para: (węzeł, poziom)
    poziomy = {}
    target_level = -1
    while queue:
        node, lvl = queue.pop(0)
        if lvl not in poziomy:
            poziomy[lvl] = []
        poziomy[lvl].append(node.key)
        if node.key == key:
            target_level = lvl
        if node.left:
            queue.append((node.left, lvl + 1))
        if node.right:
            queue.append((node.right, lvl + 1))
    return target_level, poziomy.get(target_level, [])


def wypisz_malejaco(node):
    """
    Wypisuje elementy drzewa w porządku malejącym.
    W BST odwrotna kolejność in-order (prawo, korzeń, lewo) daje uporządkowanie malejące.

    :param node: Korzeń drzewa.
    """

    def collect_keys(node):
        if node is None:
            return []
        return collect_keys(node.left) + [node.key] + collect_keys(node.right)

    if is_HMIN:
        nodes = list(collect_keys(node))
        heap_sort(nodes)
        print(nodes)
    else:
        if node:
            wypisz_malejaco(node.right)
            print(node.key, end=" ")
            wypisz_malejaco(node.left)


# =============================================================================
# Funkcje do budowy kopca minimalnego (HMIN) jako drzewa
#
# Proces:
# 1. Budujemy kompletne drzewo binarne z listy (odwzorowanie tablicowe)
# 2. Przeprowadzamy "heapify" drzewa metodą postorder, aby przywrócić własność kopca minimalnego.
# =============================================================================

def build_complete_tree(lst, i=0):
    """
    Buduje kompletne drzewo binarne z listy.
    Element o indeksie i staje się korzeniem poddrzewa, a jego dzieci znajdują się
    pod indeksami 2*i+1 i 2*i+2.

    :param lst: Lista elementów.
    :param i: Indeks bieżącego elementu (domyślnie 0 – korzeń).
    :return: Korzeń zbudowanego drzewa.
    """
    if i >= len(lst):
        return None
    node = Node(lst[i])
    node.left = build_complete_tree(lst, 2 * i + 1)
    node.right = build_complete_tree(lst, 2 * i + 2)
    return node


def HMIN(lst):
    """
    Buduje kopiec minimalny (HMIN) z listy.
    Najpierw buduje kompletne drzewo binarne, a następnie przekształca je w kopiec,
    zapewniając, że każdy rodzic ma wartość mniejszą lub równą wartości swoich dzieci.

    :param lst: Lista elementów.
    :return: Korzeń kopca minimalnego.
    """

    global is_HMIN
    is_HMIN = True

    def heapify_tree(node):
        """
        Przekształca drzewo w kopiec minimalny (min-heap) metodą postorder.
        Najpierw heapify dla lewego i prawego poddrzewa, następnie porównanie
        bieżącego węzła z jego dziećmi i ewentualna zamiana, by zapewnić, że
        wartość w węźle jest mniejsza lub równa wartościom w dzieciach.

        :param node: Bieżący węzeł.
        """
        if node is None:
            return
        # Najpierw przetwórz poddrzewa
        heapify_tree(node.left)
        heapify_tree(node.right)
        # Znajdź najmniejszy element spośród node i jego dzieci
        smallest = node
        if node.left is not None and node.left.key < smallest.key:
            smallest = node.left
        if node.right is not None and node.right.key < smallest.key:
            smallest = node.right
        # Jeśli któryś z dzieci jest mniejszy, dokonaj zamiany i heapify na tym dziecku
        if smallest != node:
            node.key, smallest.key = smallest.key, node.key
            heapify_tree(smallest)

    root = build_complete_tree(lst)
    heapify_tree(root)
    return root


# =============================================================================
# Funkcje pomocnicze do operacji na kopcu zrealizowanych w wersji tablicowej.
#
# Aby uniknąć powtórzeń, zdefiniowano jedną funkcję heapify_array wykorzystywaną
# przez heap_sort, która buduje kopiec w tablicy.
# =============================================================================

def tworzenie_kopca(t, n, i):
    najmniejszy=i
    #sprawdzamy czy lewa gałąź istnieje i czy jest mniejsza od korzenia
    if i * 2 + 1 <n and t[i * 2 + 1] < t[najmniejszy]:
        najmniejszy = i * 2 +1

    # sprawdzamy czy lewa gałąź istnieje i czy jest mniejsza od korzenia
    if i * 2 + 2 < n and t[i * 2 + 2] < t[najmniejszy]:
        najmniejszy = i * 2 + 2

    if najmniejszy != i:
        t[i],t[najmniejszy] = t[najmniejszy],t[i]
        # sprawdzamy ponowonie miejsce z ktorym zamienilismy wartosci
        tworzenie_kopca(t,n,najmniejszy)

def heap_sort(t):
    # za pomoca petli i funkcji tworzymy pelny kopiec
    # zaczynyamy od pierwszego rodzica czyli n//2
    for i in range(len(t)//2,-1,-1):
        tworzenie_kopca(t,len(t),i)

    #zaczynamy wlasciwe sortowanie
    for i in range(len(t) - 1, 0, -1):
        t[i],t[0] = t[0],t[i]
        tworzenie_kopca(t,i,0)
    return t


# =============================================================================
# ALGORTYM ROWNOWAŻENIA DRZEWA ITERACYJNYM USUWANIEM WĘZŁÓW
# =============================================================================

def wspolczynik_rownowagi(node):
    """Oblicza współczynnik równowagi """
    if node is None:
        return 0
    return wysokosc(node.left) - wysokosc(node.right)


def znajdz_niezbalansowany_element(root):
    """Znajduje pierwszy niebalansowany węzeł metodą level-order"""
    queue = [root]
    while queue:
        node = queue.pop(0)
        if abs(wspolczynik_rownowagi(node)) > 1:
            return node
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return None


def get_max(node):
    """Znajduje maksymalny węzeł w poddrzewie"""
    while node and node.right:
        node = node.right
    return node


def get_min(node):
    """Znajduje minimalny węzeł w poddrzewie"""
    while node and node.left:
        node = node.left
    return node


def usun_wezel(root, key):
    """Usuwa węzeł o podanym kluczu z BST"""
    if root is None:
        return root
    if key < root.key:
        root.left = usun_wezel(root.left, key)
    elif key > root.key:
        root.right = usun_wezel(root.right, key)
    else:
        # Brak dzieci lub jedno dziecko
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        # Zastepujemy usuwany element wezlem z poddrzewa o najwiekszej wysokosci
        if wysokosc(root.right) > wysokosc(root.left):
            temp = get_min(root.right)
            root.key = temp.key
            root.right = usun_wezel(temp.right, temp.key)
        else:
            temp = get_max(root.left)
            root.key = temp.key
            root.left = usun_wezel(root.left, temp.key)
    return root


def rownowazenie_drzewa(root):
    """Równoważy BST iteracyjnie usuwając i wstawiając węzły"""
    while True:
        unbalanced = znajdz_niezbalansowany_element(root)
        if unbalanced is None:
            break  # Drzewo jest zrównoważone

        element_do_dodania = unbalanced.key
        root = usun_wezel(root, unbalanced.key)  # Usuwamy zastępczy węzeł
        root = FCFS(root, element_do_dodania)  # Wstawiamy go ponownie

    return root


# =============================================================================
# FUNKCJA GENERUJACA
# =============================================================================

def generuj_ciag_losowy(n: int, min_val=1, max_val=1000000):
    ciag = random.sample(range(min_val, max_val), n)
    return ciag


def generuj_ciag_posortowany(n: int, min_val=1, max_val=1000000):
    ciag = sorted(random.sample(range(min_val, max_val), n))
    return ciag


# =============================================================================
# INTERFEJS UŻYTKOWNIKA
# =============================================================================


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def wczytaj_dane_z_klawiatury():
    dane = input("Podaj liczby oddzielone spacją: ")
    return list(map(int, dane.strip().split()))


def wczytaj_dane_z_pliku():
    nazwa = input("Podaj nazwę pliku: ")
    try:
        with open(nazwa, 'r') as f:
            return list(map(int, f.read().strip().split()))
    except FileNotFoundError:
        print("Nie znaleziono pliku.")
        return []


def wczytaj_dane_z_generatora():
    size = [10, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]

    print("wybierz rodzaj drzewa i operacje ")
    print("\nWybierz typ drzewa:")
    print("1. AVL")
    print("2. BST (FCFS)")
    print("3. HMIN")
    drzewo = input("> ")
    print("\nWybierz operację:")
    print("1. Ścieżka do min i max")
    print("2. Równoważenie drzewa iteracyjnym usuwaniem węzłów")
    operacja = input("> ")
    if drzewo == '1':
        if operacja == '1':
            print("wyniki dla ciagu losowego : ")
            for n in size:
                dane = generuj_ciag_losowy(n)
                start_czas = time.time()
                heap_sort(dane)
                root = AVL(dane)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas utworzenia drzewa AVL dla n = {n} wynosi : {czas:.6f} s", end="  ")

                start_czas = time.time()
                path_min, path_max = znajdz_min_i_max(root)
                # print("Min:", path_min)
                # print("Max:", path_max)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas operacji dla n = {n} wynosi : {czas:.6f} s")

            print("wyniki dla ciagu rosnacego : ")
            for n in size:
                dane = generuj_ciag_posortowany(n)
                start_czas = time.time()
                heap_sort(dane)
                root = AVL(dane)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas utworzenia drzewa AVL dla n = {n} wynosi : {czas:.6f} s", end="  ")

                start_czas = time.time()
                path_min, path_max = znajdz_min_i_max(root)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas operacji dla n = {n} wynosi : {czas:.6f} s")
                success = 1
        elif operacja == '2':
            print("wyniki dla ciagu losowego : ")
            for n in size:
                dane = generuj_ciag_losowy(n)
                start_czas = time.time()
                heap_sort(dane)
                root = AVL(dane)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas utworzenia drzewa AVL dla n = {n} wynosi : {czas:.6f} s", end="  ")

                start_czas = time.time()
                r = rownowazenie_drzewa(root)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas operacji dla n = {n} wynosi : {czas:.6f} s")

            print("wyniki dla ciagu rosnacego : ")
            for n in size:
                dane = generuj_ciag_posortowany(n)
                start_czas = time.time()
                heap_sort(dane)
                root = AVL(dane)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas utworzenia drzewa AVL dla n = {n} wynosi : {czas:.6f} s", end="  ")

                start_czas = time.time()
                r = rownowazenie_drzewa(root)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas operacji dla n = {n} wynosi : {czas:.6f} s")
                success = 1
    elif drzewo == '2':
        if operacja == '1':
            print("wyniki dla ciagu losowego : ")
            for n in size:
                dane = generuj_ciag_losowy(n)
                start_czas = time.time()
                root = Node(dane[0])
                for i in dane[1:]:
                    FCFS(root, i)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas utworzenia drzewa BST dla n = {n} wynosi : {czas:.6f} s", end="  ")

                start_czas = time.time()
                path_min, path_max = znajdz_min_i_max(root)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas operacji dla n = {n} wynosi : {czas:.6f} s")

            print("\nwyniki dla ciagu rosnacego : ")
            for n in size:
                dane = generuj_ciag_posortowany(n)
                start_czas = time.time()
                root = Node(dane[0])
                for i in dane[1:]:
                    FCFS(root, i)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas utworzenia drzewa BST dla n = {n} wynosi : {czas:.6f} s", end="  ")

                start_czas = time.time()
                path_min, path_max = znajdz_min_i_max(root)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas operacji dla n = {n} wynosi : {czas:.6f} s")
                success = 1
        elif operacja == '2':
            print("wyniki dla ciagu losowego : ")
            for n in size:
                dane = generuj_ciag_losowy(n)
                start_czas = time.time()
                root = Node(dane[0])
                for i in dane[1:]:
                    FCFS(root, i)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas utworzenia drzewa BST dla n = {n} wynosi : {czas:.6f} s", end="  ")

                start_czas = time.time()
                r = rownowazenie_drzewa(root)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas operacji dla n = {n} wynosi : {czas:.6f} s")

            print("wyniki dla ciagu rosnacego : ")
            for n in size:
                dane = generuj_ciag_posortowany(n)
                start_czas = time.time()
                root = Node(dane[0])
                for i in dane[1:]:
                    FCFS(root, i)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas utworzenia drzewa BST dla n = {n} wynosi : {czas:.6f} s", end="  ")

                start_czas = time.time()
                r = rownowazenie_drzewa(root)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas operacji dla n = {n} wynosi : {czas:.6f} s")
                success = 1

    elif drzewo == '3':
        if operacja == '1':
            print("wyniki dla ciagu losowego : ")
            for n in size:
                dane = generuj_ciag_losowy(n)
                start_czas = time.time()
                root = HMIN(dane)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas utworzenia drzewa HMIN dla n = {n} wynosi : {czas:.6f} s", end="  ")

                start_czas = time.time()
                path_min, path_max = znajdz_min_i_max(root)
                # print("Min:", path_min)
                # print("Max:", path_max)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas operacji dla n = {n} wynosi : {czas:.6f} s")

            print("wyniki dla ciagu rosnacego : ")
            for n in size:
                dane = generuj_ciag_posortowany(n)
                start_czas = time.time()
                root = HMIN(dane)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas utworzenia drzewa HMIN dla n = {n} wynosi : {czas:.6f} s", end="  ")

                start_czas = time.time()
                path_min, path_max = znajdz_min_i_max(root)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas operacji dla n = {n} wynosi : {czas:.6f} s")
                success = 1
        elif operacja == '2':
            print("wyniki dla ciagu losowego : ")
            for n in size:
                dane = generuj_ciag_losowy(n)
                start_czas = time.time()
                root = HMIN(dane)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas utworzenia drzewa HMIN dla n = {n} wynosi : {czas:.6f} s", end="  ")

                start_czas = time.time()
                r = rownowazenie_drzewa(root)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas operacji dla n = {n} wynosi : {czas:.6f} s")

            print("wyniki dla ciagu rosnacego : ")
            for n in size:
                dane = generuj_ciag_posortowany(n)
                start_czas = time.time()
                root = HMIN(dane)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas utworzenia drzewa HMIN dla n = {n} wynosi : {czas:.6f} s", end="  ")

                start_czas = time.time()
                r = rownowazenie_drzewa(root)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"Czas operacji dla n = {n} wynosi : {czas:.6f} s")
                success = 1


def wybierz_dane():
    while True:
        print("\nWybierz źródło danych:")
        print("1. Dane z klawiatury")
        print("2. Dane z pliku")
        print("3. Dane wygenerowane")
        print("0. Wyjście")
        wybor = input("> ")
        if wybor == '1':
            return wczytaj_dane_z_klawiatury()
        elif wybor == '2':
            return wczytaj_dane_z_pliku()
        elif wybor == '3':
            return wczytaj_dane_z_generatora()
        elif wybor == '0':
            exit()
        else:
            print("Nieprawidłowy wybór.")


def wybierz_typ_drzewa(dane):
    while True:
        print("\nWybierz typ drzewa:")
        print("1. AVL")
        print("2. BST (FCFS)")
        print("3. HMIN")
        print("0. Powrót")
        wybor = input("> ")
        if wybor == '1':
            start_czas = time.time()
            heap_sort(dane)
            r = AVL(dane)
            koniec_czas = time.time()
            czas = koniec_czas - start_czas
            print(f"Czas utworzenia drzewa AVL wynosi : {czas:.6f} s")
            return r
        elif wybor == '2':
            start_czas = time.time()
            root = Node(dane[0])
            for n in dane[1:]:
                FCFS(root, n)
            koniec_czas = time.time()
            czas = koniec_czas - start_czas
            print(f"Czas utworzenia drzewa metoda FCFS wynosi : {czas:.6f} s")
            return root
        elif wybor == '3':
            start_czas = time.time()
            r = HMIN(dane)
            koniec_czas = time.time()
            czas = koniec_czas - start_czas
            print(f"Czas utworzenia drzewa metoda HMIN wynosi : {czas:.6f} s")
            return r
        elif wybor == '0':
            return None
        else:
            print("Nieprawidłowy wybór.")


def menu_operacji(root):
    while True:
        print("\nWybierz operację:")
        print("1. Wyświetl drzewo")
        print("2. Ścieżka do min i max")
        print("3. Poziom i elementy dla klucza")
        print("4. Wypisz malejąco")
        print("5. Preorder, wysokość i usunięcie poddrzewa")
        print("6. Równoważenie drzewa iteracyjnym usuwaniem węzłów")
        print("0. Powrót")

        success = 0
        while not success:
            wybor = input("> ")
            start_czas = time.time()
            if wybor == '1':
                print_tree(root)
                success = 1
            elif wybor == '2':
                start_czas = time.time()
                path_min, path_max = znajdz_min_i_max(root)
                print("Min:", path_min)
                print("Max:", path_max)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"\nCzas wykonania wynosi : {czas:.6f} s")
                success = 1
            elif wybor == '3':
                klucz = int(input("Podaj klucz: "))
                poziom, el = poziom_i_elementy_na_poziomie(root, klucz)
                print(f"Poziom: {poziom}, Elementy: {el}")
                success = 1
            elif wybor == '4':
                wypisz_malejaco(root)
                success = 1
            elif wybor == '5':
                klucz = int(input("Podaj klucz korzenia poddrzewa: "))
                wypisanie_preorder_podanie_wysokosci_i_usuniecie_poddrzewa(root, klucz)
                success = 1
            elif wybor == '6':
                start_czas = time.time()
                print("Drzewo przed zrównoważeniem : ")
                print_preorder(root)
                root = rownowazenie_drzewa(root)
                print("\nDrzewo po zrównoważeniu : ")
                print_preorder(root)
                koniec_czas = time.time()
                czas = koniec_czas - start_czas
                print(f"\nCzas wykonania wynosi : {czas:.6f} s")
                success = 1
            elif wybor == '0':
                break
            else:
                print("Nieprawidłowy wybór.")
            if success:
                input()
                clear()
        if wybor == '0':
            break


# Główna pętla programu
def main():
    while True:
        clear()
        dane = wybierz_dane()
        if not dane:
            continue
        root = wybierz_typ_drzewa(dane)
        if root:
            menu_operacji(root)


if __name__ == "__main__":
    main()
