# pgconman

A basic terminal user interface for managing environment variables related to PostgreSQL connections.

```
$ pgconman
Select a postgresql connection by number:

(0) local      postgresql://postgres@localhost:5432/postgres
(1) production postgresql://superuser@work-db:5432/project1
```

Selecting a database will set the appropriate environment variables

```
0

export PGHOST="localhost"
export PGPORT="5432"
export PGDATABASE="postgres"
export PGUSER="postgres"
export POSTGRESQL_CONNECTION="postgresql://postgres@localhost:5432/postgres"
export PG_CONNECTION_ALIAS="local"
unset PGPASSWORD
```

to allow `psql` to connect without additional arguments

```bash
$ psql  # use PG_* environment variables + the .pgpass file
```

## Goals

1. Uses `.pgpass` to define the available connections.
2. Provides an interactive terminal interface to select from the available connections.
3. Sets the appropriate `PG_*` environment variables based on selection.
4. Distributed as a single standalone script to simplify dependency management.


## Requirements

* A `python3` interpreter (version 3.5+)
* A unix shell (tested in Bash)
* A `.pgpass` file with your postgres connection info
* A `~/bin` directory to put the script (substitute for your bin directory of choice in the examples below)

## Installation

1. Download the script

```
wget -O ~/bin/pgconman.py https://...
```

2. Paste the following in your terminal or shell startup (e.g. `~/.bashrc`)

```
function pgconman {
    python3 ~/bin/pgconman.py
    source ~/.pg_active_connection_env.sh
}
```
