from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ResultadoCarrera(Base):
    __tablename__ = 'resultados'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Datos identificativos
    edicion = Column(Integer, nullable=False)
    nombre = Column(String, nullable=False) # Al ser SQLite no hace falta que indiquemos la longitud del campo
    dorsal = Column(String, nullable=True)
    posicion = Column(Integer)
    tiempo_str = Column(String) 
    tiempo_min = Column(Float)
    sexo = Column(String)
    categoria = Column(String)
    location = Column(String)
    distancia = Column(String)
    date = Column(String)

    # Evitar duplicados
    __table_args__ = (
        UniqueConstraint('edicion', 'nombre', 'tiempo_str', name='_corredor_edicion_uc'),
    )