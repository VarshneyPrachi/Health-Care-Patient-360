import sys

import pandas as pd
import numpy as np
import sklearn
import sqlalchemy
import pymysql

print("=" * 60)
print("HEALTHCARE PATIENT 360")
print("Environment Test")
print("=" * 60)

print(f"Python       : {sys.version.split()[0]}")
print(f"Pandas       : {pd.__version__}")
print(f"NumPy        : {np.__version__}")
print(f"Scikit-learn : {sklearn.__version__}")
print(f"SQLAlchemy   : {sqlalchemy.__version__}")
print(f"PyMySQL      : {pymysql.__version__}")

print("=" * 60)
print("Environment is ready!")
print("=" * 60)