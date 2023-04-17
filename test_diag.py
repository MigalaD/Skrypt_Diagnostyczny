import obd

# połączenie z złączem OBD2
connection = obd.OBD()

# Funkcja interpretująca kody błędów
def interpretuj_kod_bledu(kod_bledu):
    kody_bledow = {
        "P0001": "Kontrola regulacji paliwa układu 'A' otwarcie",
        "P0002": "Kontrola regulacji paliwa układu 'A' zakres/nieprawidłowe działanie",
        "P0003": "Kontrola regulacji paliwa układu 'A' wydajność",
        # dalsze kody błędów i opisy
        # trzeba dodać listę kodów przypisaną dla danego auta
    }

    # sprawdzenie, czy kod błędu znajduje się w słowniku
    if kod_bledu in kody_bledow:
        # jeśli tak, zwróć opis kodu błędu
        return kody_bledow[kod_bledu]
    else:
        # jeśli nie, zwróć informację o nieznanym kodzie błędu
        return "Nieznany kod błędu: {}".format(kod_bledu)

# pobranie listy błędów
errors = connection.query(obd.commands.GET_DTC)

# wyświetlenie listy błędów z ich opisami
def wyswietl_liste_bledow():
    print("Lista błędów:")
    for code in errors.value:
        opis_bledu = interpretuj_kod_bledu(code)
        print("{} - {}".format(code, opis_bledu))

# pobranie i wyświetlenie stanów poszczególnych czujników
def wyswietl_stany_czujnikow():
    print("Stany czujników:")
    response = connection.query(obd.commands.STATUS)
    print(response.value)

# pobranie i wyświetlenie aktualnych wartości parametrów diagnostycznych
def aktualne_wartosci():
    print("Aktualne wartości parametrów:")
    print("Prędkość obrotowa wału korbowego:", connection.query(obd.commands.RPM).value)
    print("Temperatura silnika:", connection.query(obd.commands.COOLANT_TEMP).value)
    print("Napięcie akumulatora:", connection.query(obd.commands.BATTERY_VOLTAGE).value)
    print("Ciśnienie w kolektorze ssącym:", connection.query(obd.commands.INTAKE_PRESSURE).value)

# przeprowadzenie testu ABS i wyświetlenie wyniku
def test_abs():
    print("Przeprowadzanie testu ABS...")
    response = connection.query(obd.commands.ABS_TEST)
    if response.value == "OK":
        print("Test zakończony powodzeniem")
    else:
        print("Test zakończony niepowodzeniem")

# przeprowadzenie testu sondy lambda i wyświetlenie wyniku
def test_lambda():
    print("Przeprowadzanie testu sondy lambda...")
    response = connection.query(obd.commands.O2_TEST)
    if response.value == "OK":
        print("Test zakończony powodzeniem")
    else:
        print("Test zakończony niepowodzeniem")

# przeprowadzenie testu napięcia akumulatora i wyświetlenie wyniku
def test_akumulatora():
    print("Przeprowadzanie testu napięcia akumulatora...")
    response = connection.query(obd.commands.BATTERY_VOLTAGE)
    voltage = float(response.value.magnitude)
    if voltage > 12.6:
        print(f"Napięcie akumulatora wynosi {voltage}V - OK")
    elif voltage > 12.4:
        print(f"Napięcie akumulatora wynosi {voltage}V - Uwaga: niskie napięcie")
    else:
        print(f"Napięcie akumulatora wynosi {voltage}V - Uwaga: bardzo niskie napięcie")

# pobranie aktualnej prędkości pojazdu i wyświetlenie wyniku w km/h
def aktualna_predkosc():
    print("Pobieranie aktualnej prędkości pojazdu...")
    response = connection.query(obd.commands.SPEED)
    speed = response.value.to('kph').magnitude
    print(f"Aktualna prędkość pojazdu: {speed} km/h")

#kasowanie błędów zapisanych w sterowniku silnika
def kasowanie_bledow():
    # kasowanie błędów
    print("Kasowanie błędów...")
    response = connection.query(obd.commands.CLEAR_DTC)
    print(response.value)

    # ponowne pobranie listy błędów, powinna być pusta
    errors = connection.query(obd.commands.GET_DTC)

    # wyświetlenie listy błędów
    print("Lista błędów po kasowaniu:")
    for code in errors.value:
        print(code)

#menu wyboru działań
print("Wybierz działanie: \n"
      "1. Wyświetl listę błędów\n"
      "2. Wyświetl stany czujników\n"
      "3. Wyświetl aktualne wartości\n"
      "4. Test ABS\n"
      "5. Test Lambda\n"
      "6. Test akumulatora\n"
      "7. Aktualna prędkość\n"
      "8. Kasowanie błędów\n"
      "9. Wyjście\n")
wybor = input()
if wybor == 1:
    wyswietl_liste_bledow()
elif wybor == 2:
    wyswietl_stany_czujnikow()
elif wybor == 3:
    aktualne_wartosci()
elif wybor == 4:
    test_abs()
elif wybor == 5:
    test_lambda()
elif wybor == 6:
    test_akumulatora()
elif wybor == 7:
    aktualna_predkosc()
elif wybor == 8:
    kasowanie_bledow()
elif wybor == 9:
    print("Wyjście")
    exit()
else:
    print("Nie znana wartość")
