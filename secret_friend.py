from dotenv import load_dotenv

import os, random, smtplib
from collections import namedtuple

load_dotenv()

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")

Participant = namedtuple("Participant", ("name", "email"))

participants_count = int(input("Quantas pessoas irão participar? "))
participants = []

for i in range(1, participants_count + 1):
    name = input(f"Insira o nome do participante {i}: ")
    email = input(f"Insira o email do participante {i}: ")
    participants.append(Participant(name, email))


def generate_list(participants, participants_count):
    random.shuffle(participants)
    secret_list = []

    for i, participant in enumerate(participants):
        if i < participants_count - 1:
            secret_list.append([participant, participants[i + 1]])
        else:
            secret_list.append([participants[-1], participants[0]])

    return secret_list


def send_emails(secret_list):
    with smtplib.SMTP(host="smtp-mail.outlook.com", port=587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, os.environ.get("PASSWORD"))

        for result in secret_list:
            secret_friend = result[1]
            sender = f"Amigo Secreto <{SENDER_EMAIL}>"
            receiver = f"{result[0].name} <{result[0].email}>"

            message = f"Subject: Seu amigo secreto!\nTo: {receiver}\nFrom: {sender}\n\nSeu amigo secreto: {secret_friend.name}."
            server.sendmail(sender, receiver, message)


secret_list = generate_list(participants, participants_count)
send_emails(secret_list)
print("Emails enviados!")
