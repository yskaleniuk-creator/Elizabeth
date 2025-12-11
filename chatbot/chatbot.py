# Приветствие
print("Hello! My name is Alex")
print("I was created in 2025")
print("Please, remind me your name:")

# Ввод имени
name = input()
print(f"What a great name you have, {name}!")

# Определение возраста
print("\nLet me guess your age.")
print("Enter remainders of dividing your age by 3, 5 and 7:")

rem3 = int(input())
rem5 = int(input())
rem7 = int(input())

age = (rem3 * 70 + rem5 * 21 + rem7 * 15) % 105
print(f"Your age is {age}; that's a good time to start programming!")

# Счёт до числа
print("\nNow I will prove to you that I can count to any number you want.")
number = int(input())

i = 0
while i <= number:
    print(f"{i}!")
    i += 1

# Тест для пользователя
print("\nLet's test your programming knowledge!")
print("Why do we use methods?")
print("1. To repeat a statement multiple times")
print("2. To decompose a program into several small subroutines")
print("3. To determine the execution time of a program")
print("4. To interrupt the execution of a program")

while True:
    try:
        answer = int(input())
    except ValueError:
        print("Invalid input. Please enter a number from 1 to 4.")
        continue

    if answer == 2:
        print("Completed, have a nice day!")
        break
    else:
        print("Please, try again.")

print("Congratulations, have a nice day!")
