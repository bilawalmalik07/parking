import os
import psycopg2
import sys
import math
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv("database.env")
DATABASE_URL = os.getenv("DATABASE_URL")
connection = psycopg2.connect(DATABASE_URL)

# Functions


def slot_checker():
    cursor = connection.cursor()
    query1 = "SELECT COUNT(*) from tickets WHERE is_active = TRUE;"
    cursor.execute(query1)
    result = cursor.fetchone()
    slots = result[0]
    cursor.close()
    if slots < 50:
        return True
    else:
        return False


def entry():
    name = input("Enter your name : ")
    print(f"Welcome {name}!!!")
    space = slot_checker()
    if space == False:
        print(f"Sorry {name}! We are full.")
        print("Byeee ! have a good day")
        sys.exit()
    plate = input("Enter your Plate number : ")
    cursor = connection.cursor()
    query2 = ("INSERT into tickets (plate) VALUES(%s) RETURNING id")
    cursor.execute(query2, (plate,))
    connection.commit()
    fetched = cursor.fetchone()
    ticket_id = fetched[0]
    cursor.close()
    print(f"Success! Your ticket is {ticket_id}")


def exit():
    ticket_number = input("Enter your ticket number : ")
    cursor = connection.cursor()
    query3 = "SELECT entry_time from tickets WHERE id = %s and is_active = TRUE;"
    cursor.execute(query3, (ticket_number,))
    result = cursor.fetchone()
    if result is None:
        print("Ticket not found.")
        cursor.close()
        return
    entrytime = result[0].replace(tzinfo=timezone.utc)
    exittime = datetime.now(timezone.utc)
    duration = exittime-entrytime
    total_minutes = duration.total_seconds()/60
    hours = total_minutes/60
    blocks = math.ceil(hours/2)
    total_due = blocks*5
    print(f"Hours:  {hours:.1f}")
    print(f"Blocks: {blocks}")
    print(f"Pay:    ${total_due}")

    confirm = input("Confirm payment? yes/no : ").lower()
    while confirm != "yes":
        print("Gate is still closed. You must pay to exit.")
        confirm = input("Confirm payment? yes/no : ").lower()
    update_query = """
        UPDATE tickets 
        SET is_active = FALSE, exit_time = %s, amount_paid = %s 
        WHERE id = %s;
        """
    cursor.execute(update_query, (exittime, total_due, ticket_number))
    connection.commit()
    print("Payment successful. Have a nice day!")


def main():
    while True:
        print("\n--- Parking System ---")
        choice = input("1. Enter Lot\n2. Exit Lot\n3. Quit\nSelection: ")

        if choice == "1":
            entry()
        elif choice == "2":
            exit()
        elif choice == "3":
            break
        else:
            print("Invalid selection. Try again.")


if __name__ == "__main__":
    main()
