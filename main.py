import os

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
    node.left = AVL(lst[:mediana])
    node.right = AVL(lst[mediana + 1:])
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


def heap_sort(arr):
    """
    Sortuje tablicę metodą heapsort z użyciem kopca minimalnego.
    Najpierw buduje kopiec (min-heap), a następnie powtarza operację wyciągania najmniejszego
    elementu, umieszczając go na końcu tablicy. Na końcu odwracamy tablicę, aby otrzymać porządek rosnący.

    :param arr: Lista do posortowania.
    :return: Posortowana lista w porządku rosnącym.
    """

    def heapify_array(arr, n, i):
        """
        Przekształca poddrzewo w tablicy (reprezentacja kopca) w kopiec minimalny.
        Dla danego indeksu i sprawdza, czy lewy i prawy potomek mają większe wartości.
        Jeśli nie, zamienia elementy i rekurencyjnie heapify.

        :param arr: Lista reprezentująca kopiec.
        :param n: Rozmiar kopca (część tablicy do rozpatrzenia).
        :param i: Indeks korzenia poddrzewa.
        """
        smallest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] < arr[smallest]:
            smallest = left
        if right < n and arr[right] < arr[smallest]:
            smallest = right
        if smallest != i:
            arr[i], arr[smallest] = arr[smallest], arr[i]
            heapify_array(arr, n, smallest)

    n = len(arr)
    # Budowanie kopca – zaczynamy od ostatniego rodzica.
    for i in range(n // 2 - 1, -1, -1):
        heapify_array(arr, n, i)
    # Wyciągamy elementy z kopca jeden po drugim.
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify_array(arr, i, 0)
    # Kopiec minimalny daje sortowanie malejące – odwracamy, by uzyskać kolejność rosnącą.
    return arr


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

def wybierz_dane():
    while True:
        print("\nWybierz źródło danych:")
        print("1. Dane z klawiatury")
        print("2. Dane z pliku")
        print("0. Wyjście")
        wybor = input("> ")
        if wybor == '1':
            return wczytaj_dane_z_klawiatury()
        elif wybor == '2':
            return wczytaj_dane_z_pliku()
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
            dane.sort()
            return AVL(dane)
        elif wybor == '2':
            root = Node(dane[0])
            for n in dane[1:]:
                FCFS(root, n)
            return root
        elif wybor == '3':
            return HMIN(dane)
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
        print("0. Powrót")

        success = 0
        while not success:
            wybor = input("> ")
            if wybor == '1':
                print_tree(root)
                success = 1
            elif wybor == '2':
                path_min, path_max = znajdz_min_i_max(root)
                print("Min:", path_min)
                print("Max:", path_max)
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
