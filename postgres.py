import datetime

import asyncpg
from opentelemetry import trace
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor

# --------------------------------------
# Allows Auto Instrumentation to kick in
# --------------------------------------
AsyncPGInstrumentor().instrument()

async def talk_to_postgres(name):
    tracer = trace.get_tracer("custom-tracer")
    with tracer.start_as_current_span("talk-to-postgres") as span:
        conn = await asyncpg.connect('postgresql://postgres@localhost/test', password='winona00')
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                name text,
                dob date
            )
        ''')

        await conn.execute('''
            INSERT INTO users(name, dob) VALUES($1, $2)
        ''', name, datetime.date(1984, 3, 1))

        await conn.fetchrow(
            'SELECT * FROM users WHERE name = $1', name)

        await conn.close()