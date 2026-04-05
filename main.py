import os
import psycopg2
import sys
import math
from datetime import datetime, timezone
from dotenv import load_dotenv

try:
    load_dotenv("database.env")
    DATABASE_URL = os.getenv("DATABASE_URL")
    connection = psycopg2.connect(DATABASE_URL)
    DB_CONNECTED = True
except Exception:
    print("Running in DEMO MODE (No Database)")
    DB_CONNECTED = False
    fake_db = []
# Functions


def slot_checker():
    if DB_CONNECTED:
        cursor = connection.cursor()
        query1 = "SELECT COUNT(*) from tickets WHERE is_active = TRUE;"
        cursor.execute(query1)
        result = cursor.fetchone()
        slots = result[0]
        cursor.close()
    else:
        slots = len(fake_db)

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
    if DB_CONNECTED:
        cursor = connection.cursor()
        query2 = ("INSERT into tickets (plate) VALUES(%s) RETURNING id")
        cursor.execute(query2, (plate,))
        connection.commit()
        fetched = cursor.fetchone()
        ticket_id = fetched[0]
        cursor.close()
    else:
        ticket_id = len(fake_db) + 1
        fake_db.append({
            "id": ticket_id,
            "plate": plate,
            "entry_time": datetime.now(timezone.utc),
            "is_active": True
        })
    print(f"Success! Your ticket is {ticket_id}")


def exit():
    ticket_number = input("Enter your ticket number : ")
    if DB_CONNECTED:
        cursor = connection.cursor()
        query3 = "SELECT entry_time from tickets WHERE id = %s and is_active = TRUE;"
        cursor.execute(query3, (ticket_number,))
        result = cursor.fetchone()
        if result is None:
            print("Ticket not found.")
            cursor.close()
            return
        entrytime = result[0].replace(tzinfo=timezone.utc)
    else:
        ticket = next((x for x in fake_db if str(
            x["id"]) == ticket_number and x["is_active"]), None)
        if ticket is None:
            print("Ticket not found in Demo Mode.")
            return
        entrytime = ticket["entry_time"]

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
        print("You must pay to exit.")
        confirm = input("Confirm payment? yes/no : ").lower()

    if DB_CONNECTED:
        update_query = """
                        UPDATE tickets 
                        SET is_active = FALSE, exit_time = %s, amount_paid = %s 
                        WHERE id = %s;"""
        cursor.execute(update_query, (exittime, total_due, ticket_number))
        connection.commit()
        cursor.close()
    else:
        ticket["is_active"] = False

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
