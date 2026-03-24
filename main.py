from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from pydantic import BaseModel

app = FastAPI()

class Prato(BaseModel):
    nome: str
    preco: float
    descricao: str
    id_categoria: int
    quantidade: str

#Listar todos os pratos
@app.get("/pratos")
def listar(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM pratos"))
    return [dict(row._mapping) for row in result]

#Inserir um prato
@app.post("/pratos")
def criar_prato(prato: Prato, db: Session = Depends(get_db)):
    query = text("INSERT INTO pratos (nome, preco, descricao, id_categoria, quantidade) VALUES (:nome, :preco, :descricao, :id_categoria, :quantidade)")

    db.execute(query, {
        "nome": prato.nome,
        "preco": prato.preco,
        "descricao": prato.descricao,
        "id_categoria": prato.id_categoria,
        "quantidade": prato.quantidade
    })
    db.commit()

#Buscar um prato
@app.get('/pratos/{id_prato}')
def get_prato(id_prato: int, db: Session = Depends(get_db)):
    query = text("SELECT * FROM pratos WHERE id_prato = :id_prato")

    result = db.execute(query, {"id_prato": id_prato}).fetchone()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prato não encontrado"
        )
    
    return dict(result._mapping)

#Atualizando pratos
@app.put("/pratos/{id_prato}")
def atualizar_prato(id_prato: int, prato: Prato, db: Session = Depends(get_db)):
    
    query_select = text("SELECT * FROM pratos WHERE id_prato = :id_prato")
    result = db.execute(query_select, {"id_prato": id_prato}).fetchone()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prato não encontrado"
        )

    query_update = text("""
        UPDATE pratos
        SET nome = :nome,
            preco = :preco
        WHERE id_prato = :id_prato
    """)

    db.execute(query_update, {
        "nome": prato.nome,
        "preco": prato.preco,
        "id_prato": id_prato
    })

    db.commit()

    return {"mensagem": "Prato atualizado com sucesso"}
    
#Deletando pratos
@app.delete("/pratos/{id_prato}")
def deletar_prato(id_prato: int, prato: Prato, db: Session = Depends(get_db)):

    query = text("SELECT * FROM pratos WHERE id_prato = :id_prato")
    result = db.execute(query, {"id_prato": id_prato}).fetchone()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prato não encontrado"
        )
    
    query_delete = text("DELETE FROM pratos WHERE id_prato = :id_prato")

    db.execute(query_delete, {"id_prato": id_prato})
    db.commit()

    return{"mensagem": "Prato deletado com sucesso"}