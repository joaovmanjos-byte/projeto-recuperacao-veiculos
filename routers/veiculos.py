from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from models import Veiculo
from schemas import VeiculoEntrada, VeiculoResposta

router = APIRouter(prefix="/veiculos", tags=["Veiculos"])


def buscar_veiculo(id: int, db: Session):
    veiculo = db.get(Veiculo, id)
    if veiculo is None:
        raise HTTPException(status_code=404, detail="Veiculo nao encontrado")
    return veiculo


def salvar(db: Session, veiculo: Veiculo):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Placa ja cadastrada")
    db.refresh(veiculo)
    return veiculo


@router.post(
    "/",
    response_model=VeiculoResposta,
    status_code=status.HTTP_201_CREATED,
)
def cadastrar(dados: VeiculoEntrada, db: Session = Depends(get_db)):
    veiculo = Veiculo(**dados.model_dump())
    db.add(veiculo)
    return salvar(db, veiculo)


@router.get("/", response_model=list[VeiculoResposta])
def listar(marca: str | None = None, db: Session = Depends(get_db)):
    consulta = select(Veiculo)
    if marca is not None:
        consulta = consulta.where(
            Veiculo.marca.ilike(marca.strip())
        )
    return db.scalars(consulta.order_by(Veiculo.id)).all()


@router.get("/{id}", response_model=VeiculoResposta)
def consultar(id: int, db: Session = Depends(get_db)):
    return buscar_veiculo(id, db)


@router.put("/{id}", response_model=VeiculoResposta)
def atualizar(id: int, dados: VeiculoEntrada, db: Session = Depends(get_db)):
    veiculo = buscar_veiculo(id, db)
    for campo, valor in dados.model_dump().items():
        setattr(veiculo, campo, valor)
    return salvar(db, veiculo)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir(id: int, db: Session = Depends(get_db)):
    veiculo = buscar_veiculo(id, db)
    db.delete(veiculo)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
