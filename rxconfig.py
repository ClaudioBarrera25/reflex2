import reflex as rx
import os 
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
DATABASE_URL = f"postgresql://postgres:{PASSWORD}@db.tvwdfnmrkrlyalffpdiu.supabase.co:5432/postgres"
DATABASE_URL = f"postgresql+psycopg2://postgres:{PASSWORD}@db.tvwdfnmrkrlyalffpdiu.supabase.co:5432/postgres?sslmode=require"
DATABASE_URL = f"postgresql+psycopg2://postgres:{PASSWORD}@db.tvwdfnmrkrlyalffpdiu.supabase.co:5432/postgres?sslmode=require"


DATABASE_URL = f"postgresql://postgres.jlrjgnzyltqgotnqkuzd:{PASSWORD}@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
DATABASE_URL = f"postgresql://postgres.jlrjgnzyltqgotnqkuzd:{PASSWORD}@aws-0-us-west-1.pooler.supabase.com:5432/postgres"



config = rx.Config(
    app_name="reflex2",
    db_url=DATABASE_URL,
    api_url="http://reflex-production-eb39.up.railway.app:8000"
)