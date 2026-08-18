zahl1 = float(input("Gib die erste Zahl ein: "))
operator = input("Gib +, -, * oder / ein: ")
zahl2 = float(input("Gib die zweite Zahl ein: "))

if operator == "+":
    ergebnis = zahl1 + zahl2
elif operator == "-":
    ergebnis = zahl1 - zahl2
elif operator == "*":
    ergebnis = zahl1 * zahl2
elif operator == "/":
    if zahl2 != 0:
        ergebnis = zahl1 / zahl2
    else:
        ergebnis = "Fehler: Division durch 0!"
else:
    ergebnis = "Ungültiger Operator!"

print("Ergebnis:", ergebnis)
