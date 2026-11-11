"""One-time database setup.

Usage:
    python setup_db.py            # create tables only
    python setup_db.py --seed     # create tables + 40 demo employees
"""
import argparse
import random
from datetime import date, timedelta

from core import crud
from core.config import DB_PATH, DEPARTMENTS
from core.database import init_db

FIRST = ["Aarav", "Asha", "Rohan", "Priya", "Vikram", "Neha", "Karan", "Sneha", "Arjun", "Meera",
         "Rahul", "Anjali", "Ishaan", "Divya", "Sameer", "Pooja"]
LAST = ["Sharma", "Verma", "Gupta", "Singh", "Patel", "Iyer", "Reddy", "Nair", "Mehta", "Kapoor"]
TITLES = {"Engineering": ["Software Engineer", "Senior Engineer", "QA Engineer"],
          "Human Resources": ["HR Executive", "Recruiter"], "Finance": ["Accountant", "Analyst"],
          "Marketing": ["Marketing Executive", "Content Strategist"],
          "Sales": ["Sales Executive", "Account Manager"], "Operations": ["Ops Manager", "Coordinator"],
          "Support": ["Support Engineer", "Customer Success"], "Legal": ["Legal Counsel"],
          "IT": ["SysAdmin", "Network Engineer"]}
BASE_SALARY = {"Engineering": 900000, "Finance": 700000, "Legal": 800000, "IT": 650000}


def seed(n: int = 40) -> None:
    random.seed(42)
    added = 0
    for i in range(1, n + 1):
        dept = random.choice(DEPARTMENTS)
        first, last = random.choice(FIRST), random.choice(LAST)
        ok, _ = crud.add_employee({
            "emp_code": f"EMP{i:03d}", "first_name": first, "last_name": last,
            "email": f"{first}.{last}{i}@example.com".lower(),
            "phone": f"+91 98{random.randint(10000000, 99999999)}",
            "department": dept, "designation": random.choice(TITLES[dept]),
            "salary": BASE_SALARY.get(dept, 500000) + random.randint(0, 40) * 10000,
            "hire_date": (date.today() - timedelta(days=random.randint(30, 365 * 8))).isoformat(),
            "status": random.choices(["Active", "On Leave", "Resigned"], [85, 8, 7])[0],
        })
        added += ok
    print(f"Seeded {added} demo employees.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", action="store_true", help="insert demo data")
    args = parser.parse_args()
    init_db()
    print(f"Database ready at {DB_PATH}")
    if args.seed:
        seed()
