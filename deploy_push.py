import sqlite3
import subprocess
import os
import argparse
import sys

DB_FILE = "servers.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            host TEXT NOT NULL,
            user TEXT NOT NULL,
            remote_path TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_server(name, host, user, remote_path):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO servers (name, host, user, remote_path)
        VALUES (?, ?, ?, ?)
    """, (name, host, user, remote_path))
    conn.commit()
    conn.close()
    print(f"\n✅ Server '{name}' added.\n")

def list_servers():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, host, user, remote_path FROM servers")
    rows = cursor.fetchall()
    print("\n📋 Registered Servers:")
    for row in rows:
        print(f"{row[0]}. {row[1]} ({row[2]}) -> {row[4]}")
    conn.close()
    print()

def push_to_server(server_id, local_folder):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT host, user, remote_path FROM servers WHERE id = ?", (server_id,))
    server = cursor.fetchone()
    conn.close()

    if not server:
        print("❌ Server ID not found.\n")
        return

    host, user, remote_path = server
    destination = f"{user}@{host}:{remote_path}"

    print(f"\n⏳ Pushing '{local_folder}' to {destination} ...")
    try:
        subprocess.run(["rsync", "-avz", "--delete", local_folder + "/", destination], check=True)
        print("✅ Push completed.\n")
    except subprocess.CalledProcessError:
        print("❌ Push failed.\n")

def interactive_menu():
    RED = "\033[31m"
    BLUE = "\033[34m"
    RESET = "\033[0m"
    GREEN = "\033[32m"
    while True:
        print (RED+"                                                                                                                                                                                                               ")
        print ("                                                                                                                                                                                                               ")
        print ("                                                                                                                                                                                                               ")
        print ("        ░▒▓███████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░       ░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░        ")
        print ("        ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        ")
        print ("       ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        ")
        print ("         ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        ")
        print ("              ░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        ")
        print ("              ░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        ")
        print ("       ░▒▓███████▓▒░   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░          ░▒▓█▓▒░   ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓████████▓▒░ ")
        print ("                                                                                                                                                                                                                 ")
        print ("    ░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░ ")
        print ("                                                                                                                                                                                                               ")
        print(RESET+"📦 Choose option 1-4")
        print("1. Add new server")
        print("2. List servers")
        print("3. Push folder to server")
        print("4. Exit")
        print("")
        print(BLUE+"==================================================")
        print("      _           ____         __        ")
        print("     | |__ _  _  |__  |  _ __ /  \ _ __  ")
        print("     | '_ \ || |   / / || / _| () | '  \ ")
        print("     |_.__/\_, |  /_/ \_,_\__|\__/|_|_|_|")
        print("           |__/                          ")
        print("==================================================")
        print(GREEN)
        choice = input("\nSelect option [1-4]: ").strip()

        if cphoice == "1":
            name = input("Server name: ")
            host = input("Host (e.g., 192.168.1.10): ")
            user = input("User (e.g., ubuntu): ")
            remote = input("Remote path (e.g., /var/www/html/): ")
            add_server(name, host, user, remote)
        elif choice == "2":
            list_servers()
        elif choice == "3":
            list_servers()
            try:
                server_id = int(input("Enter Server ID to push to: "))
                folder = input("Local folder path to push: ").strip()
                push_to_server(server_id, folder)
            except ValueError:
                print("❌ Invalid input.\n")
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.\n")

def main():
    init_db()

    parser = argparse.ArgumentParser(description="Deploy folder to registered server")
    subparsers = parser.add_subparsers(dest="command")

    add_cmd = subparsers.add_parser("add", help="Add a new server")
    add_cmd.add_argument("--name", required=True)
    add_cmd.add_argument("--host", required=True)
    add_cmd.add_argument("--user", required=True)
    add_cmd.add_argument("--remote", required=True)

    list_cmd = subparsers.add_parser("list", help="List servers")

    push_cmd = subparsers.add_parser("push", help="Push folder to server")
    push_cmd.add_argument("--id", type=int, required=True)
    push_cmd.add_argument("--folder", required=True)

    # If no arguments, show menu
    if len(sys.argv) == 1:
        interactive_menu()
    else:
        args = parser.parse_args()
        if args.command == "add":
            add_server(args.name, args.host, args.user, args.remote)
        elif args.command == "list":
            list_servers()
        elif args.command == "push":
            push_to_server(args.id, args.folder)
        else:
            parser.print_help()

if __name__ == "__main__":
    main()