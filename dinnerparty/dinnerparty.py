import random

# --- Безопасный ввод количества друзей ---
while True:
    try:
        num_friends = int(input("Enter the number of friends joining (including you):\n> "))
        break
    except ValueError:
        print("Please enter a valid integer.")

if num_friends <= 0:
    print("No one is joining for the party")
else:
    print("Enter the name of every friend (including you), each on a new line:")
    friends = {}

    for _ in range(num_friends):
        name = input()
        friends[name] = 0

    # --- Безопасный ввод суммы ---
    while True:
        try:
            total_amount = float(input("Enter the total amount:\n> "))
            break
        except ValueError:
            print("Please enter a valid number.")

    split_amount = round(total_amount / num_friends, 2)

    for friend in friends:
        friends[friend] = split_amount

    use_lucky = input('Do you want to use the "Who is lucky?" feature? Write Yes/No:\n> ')

    if use_lucky == "Yes":
        lucky_one = random.choice(list(friends.keys()))
        print(f"{lucky_one} is the lucky one!")

        if num_friends > 1:
            new_split = round(total_amount / (num_friends - 1), 2)
            for friend in friends:
                friends[friend] = 0 if friend == lucky_one else new_split
        else:
            friends[lucky_one] = 0
    else:
        print("No one is going to be lucky")

    print(friends)
