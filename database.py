import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


load_dotenv()


def get_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

    except Error as error:
        print(f"Database connection error: {error}")
        return None


def get_channels():
    connection = get_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, channel_number, name, category, country, language
            FROM channels
            ORDER BY channel_number
        """)

        channels = cursor.fetchall()

        cursor.close()
        connection.close()

        return channels

    except Error as error:
        print(f"Error loading channels: {error}")
        connection.close()
        return []


def register_history(channel_id, action):
    connection = get_connection()

    if connection is None:
        return

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO history (channel_id, action)
            VALUES (%s, %s)
        """, (channel_id, action))

        connection.commit()

        cursor.close()
        connection.close()

    except Error as error:
        print(f"Error registering history: {error}")
        connection.close()


def get_history(limit=20):
    connection = get_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                history.id,
                channels.channel_number,
                channels.name,
                history.action,
                history.created_at
            FROM history
            JOIN channels
                ON history.channel_id = channels.id
            ORDER BY history.created_at DESC
            LIMIT %s
        """, (limit,))

        history = cursor.fetchall()

        cursor.close()
        connection.close()

        return history

    except Error as error:
        print(f"Error loading history: {error}")
        connection.close()
        return []


def get_statistics():
    connection = get_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                channels.channel_number,
                channels.name,
                COUNT(history.id) AS times_selected
            FROM channels
            LEFT JOIN history
                ON channels.id = history.channel_id
                AND history.action = 'channel_change'
            GROUP BY channels.id, channels.channel_number, channels.name
            ORDER BY times_selected DESC
        """)

        statistics = cursor.fetchall()

        cursor.close()
        connection.close()

        return statistics

    except Error as error:
        print(f"Error loading statistics: {error}")
        connection.close()
        return []


def get_summary_statistics():
    connection = get_connection()

    if connection is None:
        return {
            "channel_changes": 0,
            "volume_changes": 0,
            "power_actions": 0
        }

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(
                    CASE
                        WHEN action = 'channel_change'
                        THEN 1
                    END
                ) AS channel_changes,

                COUNT(
                    CASE
                        WHEN action IN (
                            'volume_increase',
                            'volume_decrease'
                        )
                        THEN 1
                    END
                ) AS volume_changes,

                COUNT(
                    CASE
                        WHEN action IN (
                            'power_on',
                            'power_off'
                        )
                        THEN 1
                    END
                ) AS power_actions

            FROM history
        """)

        summary = cursor.fetchone()

        cursor.close()
        connection.close()

        return summary

    except Error as error:
        print(f"Error loading summary statistics: {error}")
        connection.close()

        return {
            "channel_changes": 0,
            "volume_changes": 0,
            "power_actions": 0
        }