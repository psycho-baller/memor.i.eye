import psycopg
import sys

DATABASE_URL="postgresql://..."

with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        # if parameter given drop tables (to rollback)
        if len(sys.argv) == 2:
            cur.execute("DROP TABLE Location")
            cur.execute("DROP TABLE Image")
        else:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS Image (
                id serial PRIMARY KEY,
                time timestamp,
                latitude double precision,
                longitude double precision,
                note TEXT DEFAULT '',
                gaze_x double precision,
                gaze_y double precision,
                valid boolean default false,
                embed TEXT
            )
            """)
            cur.execute("""
            CREATE Table IF NOT EXISTS Location (
                time timestamp DEFAULT now() NOT NULL,
                latitude double precision NOT NULL,
                longitude double precision NOT NULL,
                altitude double precision NOT NULL
            )
            """)
