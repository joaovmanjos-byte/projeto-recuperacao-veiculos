from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


class VeiculoEntrada(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    placa: str = Field(pattern=r"^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$")
    marca: str = Field(min_length=1, max_length=50)
    modelo: str = Field(min_length=1, max_length=80)
    ano: int = Field(ge=1886, strict=True)
    ativo: bool = Field(strict=True)

    @field_validator("placa", mode="before")
    @classmethod
    def normalizar_placa(cls, valor):
        if isinstance(valor, str):
            return valor.strip().upper().replace("-", "")
        return valor

    @field_validator("ano")
    @classmethod
    def validar_ano(cls, valor):
        if valor > date.today().year + 1:
            raise ValueError("O ano deve ser no maximo o proximo ano.")
        return valor


class VeiculoResposta(VeiculoEntrada):
    model_config = ConfigDict(from_attributes=True)

    id: int
