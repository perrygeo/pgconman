#!/usr/bin/env python3
# Requires Python 3.5+

import json
from os.path import expanduser


def get_pgpass_path():
    return expanduser("~/.pgpass")


KEYS = ["hostname", "port", "database", "username", "password"]


def get_available_connections(remove_passwords=True):
    path = expanduser("~/.pgpass")
    with open(path, "r") as fh:
        for line in fh.readlines():
            if not line.strip().startswith("#"):
                conn = dict(zip(KEYS, line.strip().split(":")))
                if remove_passwords:
                    del conn["password"]
                yield conn


def make_conn_string(hostname, port, database, username, **extras):
    return f"postgresql://{username}@{hostname}:{port}/{database}"


def export_lines(hostname, port, database, username, alias):
    conn_string = make_conn_string(hostname, port, database, username)
    lines = [
        f'export PGHOST="{hostname}"',
        f'export PGPORT="{port}"',
        f'export PGDATABASE="{database}"',
        f'export PGUSER="{username}"',
        f'export POSTGRESQL_CONNECTION="{conn_string}"',
        f'export PG_CONNECTION_ALIAS="{alias}"',
        "unset PGPASSWORD",
    ]
    return lines


def main():
    try:
        with open(expanduser("~/.pg_connection_aliases.json"), "r") as fh:
            contents = fh.read()
        aliases = json.loads(contents)
    except FileNotFoundError:
        aliases = {}

    conns = list(get_available_connections())
    print("Select a postgresql connection by number:\n")
    for i, conn in enumerate(conns):
        conn_string = make_conn_string(**conn)
        alias = aliases.get(conn_string, "")
        print(f"({i}) {alias: <10}\t{conn_string}")
    selected_value = int(input("\n"))
    assert selected_value in range(len(conns)), "Not a valid connection number"

    selected_conn = conns[selected_value]
    selected_conn_string = make_conn_string(**selected_conn)

    alias = aliases.get(selected_conn_string, None)
    if not alias:
        selected_alias = input(
            f"Alias for this connection: (optional, currently {alias})\n"
        )
        if selected_alias:
            alias = selected_alias.strip()
            aliases[selected_conn_string] = alias
            with open(expanduser("~/.pg_connection_aliases.json"), "w") as fh:
                fh.write(json.dumps(aliases))

    outputs = export_lines(**selected_conn, alias=alias)
    with open(expanduser("~/.pg_active_connection_env.sh"), "w") as fh:
        fh.write("\n".join(outputs))
        print("\n".join(outputs))


if __name__ == "__main__":
    # function pgconman { python parse_pgpass.py; source ~/.pg_active_connection_env.sh; }
    main()
