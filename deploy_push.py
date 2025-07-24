import sqlite3
import subprocess
import os
import argparse

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
    print(f"✅ Server '{name}' added.")

def list_servers():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, host, user, remote_path FROM servers")
    rows = cursor.fetchall()
    for row in rows:
        print(f"{row[0]}. {row[1]} ({row[2]}) -> {row[4]}")
    conn.close()

def push_to_server(server_id, local_folder):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT host, user, remote_path FROM servers WHERE id = ?", (server_id,))
    server = cursor.fetchone()
    conn.close()

    if not server:
        print("❌ Server ID not found.")
        return

    host, user, remote_path = server
    destination = f"{user}@{host}:{remote_path}"

    print(f"⏳ Pushing to {destination} ...")
    try:
        subprocess.run(["rsync", "-avz", "--delete", local_folder + "/", destination], check=True)
        print("✅ Push completed.")
    except subprocess.CalledProcessError:
        print("❌ Push failed.")

def main():
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

    args = parser.parse_args()

    init_db()

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