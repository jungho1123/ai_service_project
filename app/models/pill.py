# app/models/pill.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Pill(Base):
    __tablename__ = "pills"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(String, unique=True, nullable=False, index=True)
    dl_name = Column(String)
    dl_material = Column(String)
    dl_company = Column(String)
    di_company_mf = Column(String)
    di_class_no = Column(String)
    di_etc_otc_code = Column(String)
    di_edi_code = Column(String)
    item_seq = Column(Integer)
    img_key = Column(String)