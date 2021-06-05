# sqlPractice.py
# Author: Matthew Talamantes
# Date: June 5, 2021
# Description: A simple program to practice SQLAlchemy and use of databases

from sqlalchemy import (
    create_engine,
    text,
)

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

# commit as you go
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"), [{"x": 1, "y": 1}, {"x": 2, "y": 4}])
    conn.commit()

# begin once
with engine.begin() as conn:
    conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"), [{"x": 6, "y": 8}, {"x": 9, "y": 10}])

# fetch rows
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x}  y: {row.y}")

with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table WHERE x % 2 = :x"), {"x": 0}) # ":x" refers to the value of the "x" key in the following dict
    for row in result:
        print(f"x: {row.x}  y: {row.y}")

# bundling parameters with a statement
stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(y=6)
with engine.connect() as conn:
    result = conn.execute(stmt)
    for row in result:
        print(f"x: {row.x}  y: {row.y}")