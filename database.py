import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_connection() -> psycopg.Connection:
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def initialize_database() -> None:
    create_table_query = """
        CREATE TABLE IF NOT EXISTS chat_messages (
            id BIGSERIAL PRIMARY KEY,
            session_id VARCHAR(100) NOT NULL,
            role VARCHAR(20) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)


def save_message(session_id: str, role: str, content: str) -> None:
    insert_query = """
        INSERT INTO chat_messages (session_id, role, content)
        VALUES (%s, %s, %s);
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                insert_query,
                (session_id, role, content),
            )


def load_messages(session_id: str) -> list[dict[str, str]]:
    select_query = """
        SELECT role, content
        FROM chat_messages
        WHERE session_id = %s
        ORDER BY created_at ASC, id ASC;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(select_query, (session_id,))
            rows = cursor.fetchall()

    return [
        {
            "role": role,
            "content": content,
        }
        for role, content in rows
    ]

def clear_messages(session_id: str) -> None:
    delete_query = """
        DELETE FROM chat_messages
        WHERE session_id = %s;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(delete_query, (session_id,))


if __name__ == "__main__":
    initialize_database()
    print("Database table initialized successfully.")