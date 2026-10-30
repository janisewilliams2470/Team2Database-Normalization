print("--- SCRIPT HAS STARTED ---")
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, ForeignKey, Text, Boolean
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    publication_date = Column(String(50))
    source_file = Column(String(255))
    
    findings = relationship("Finding", back_populates="report")

class Facility(Base):
    __tablename__ = 'facilities'
    id = Column(Integer, primary_key=True)
    canonical_name = Column(String(150), unique=True, nullable=False) # Handles variations like "24085 LUGO"
    voltage_kv = Column(Float)
    facility_type = Column(String(50))
    
    findings = relationship("Finding", back_populates="facility")

class Contingency(Base):
    __tablename__ = 'contingencies'
    id = Column(Integer, primary_key=True)
    contingency_code = Column(String(50), unique=True, nullable=False) # e.g., P6, N-1-1
    category = Column(String(50))
    description = Column(Text)
    
    findings = relationship("Finding", back_populates="contingency")

class Scenario(Base):
    __tablename__ = 'scenarios'
    id = Column(Integer, primary_key=True)
    scenario_name = Column(String(100), unique=True, nullable=False) # e.g., 2028 Summer Peak
    study_year = Column(Integer)
    condition_type = Column(String(50))

class Mitigation(Base):
    __tablename__ = 'mitigations'
    id = Column(Integer, primary_key=True)
    mitigation_text = Column(Text, nullable=False)
    solution_type = Column(String(50)) # RAS, BESS, etc.
    
    findings = relationship("Finding", back_populates="mitigation")

class Evidence(Base):
    __tablename__ = 'evidence'
    id = Column(Integer, primary_key=True)
    finding_id = Column(Integer, ForeignKey('findings.id'))
    source_document = Column(String(255))
    page_number = Column(Integer)
    table_reference = Column(String(100))
    
    finding = relationship("Finding", back_populates="evidence_records")

class Finding(Base):
    __tablename__ = 'findings'
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('reports.id'))
    facility_id = Column(Integer, ForeignKey('facilities.id'))
    contingency_id = Column(Integer, ForeignKey('contingencies.id'))
    scenario_id = Column(Integer, ForeignKey('scenarios.id'))
    mitigation_id = Column(Integer, ForeignKey('mitigations.id'), nullable=True)
    
    # Dual-value strategy for messy inputs
    raw_value = Column(String(50))        # Preserves exact text (e.g., "119.0%", "<100", "NotConv")
    parsed_value = Column(Float)          # Clean numerical representation
    status_flag = Column(String(50))      # OVERLOAD, BELOW_LIMIT, NOT_CONVERGED
    
    report = relationship("Report", back_populates="findings")
    facility = relationship("Facility", back_populates="findings")
    contingency = relationship("Contingency", back_populates="findings")
    scenario = relationship("Scenario", back_populates="findings")
    mitigation = relationship("Mitigation", back_populates="findings")
    evidence_records = relationship("Evidence", back_populates="finding")

def init_db(db_url="sqlite:///power_system_reliability.db"):
    engine = create_engine(db_url, echo=False)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

if __name__ == "__main__":
    init_db()
    print("Database schema created successfully!")