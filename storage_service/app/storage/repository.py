import sqlite3
from contextlib import closing

from app.domain.models import Plane, PlaneCreate


class SQLitePlaneRepository:

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

        with closing(sqlite3.connect(self._db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS planes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    registration TEXT NOT NULL,
                    model TEXT NOT NULL,
                    airline TEXT NOT NULL
                )
            """)
            conn.commit()

    def save(self, plane: PlaneCreate) -> Plane:
        with closing(sqlite3.connect(self._db_path)) as conn:
            cursor = conn.execute(
                """
                INSERT INTO planes (registration, model, airline)
                VALUES (?, ?, ?)
                """,
                (plane.registration, plane.model, plane.airline),
            )

            plane_id = cursor.lastrowid
            conn.commit()

            if plane_id is None:
                raise RuntimeError("Failed to create plane")

        return Plane(
            id=plane_id,
            registration=plane.registration,
            model=plane.model,
            airline=plane.airline,
        )

    def get(self, plane_id: int) -> Plane | None:
        with closing(sqlite3.connect(self._db_path)) as conn:
            cursor = conn.execute(
                """
                SELECT id, registration, model, airline
                FROM planes
                WHERE id = ?
                """,
                (plane_id,),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        return Plane(
            id=row[0],
            registration=row[1],
            model=row[2],
            airline=row[3],
        )
