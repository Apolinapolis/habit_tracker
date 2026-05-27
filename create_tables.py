from app.db import engine
from app.models.db_models import Base

#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("tables created")