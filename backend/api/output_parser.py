# backend/api/output_parser.py

from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class LegalAnswer(BaseModel):
    answer: str = Field(..., description="Respuesta legal en lenguaje claro.")
    sources: list[str] = Field(default=[], description="Listado de fuentes utilizadas.")

legal_output_parser = PydanticOutputParser(pydantic_object=LegalAnswer)
