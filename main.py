from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any, Union
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurar el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost","*"],  # Reemplaza "http://localhost" con el origen de tu aplicación JavaScript
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)



# Definimos la clase de usuario
class Usuario(BaseModel):
    usuario: str
    contraseña: int
    tok1: str
    tok2: str
    tok3: str

# Creamos una clase para la base de datos
class BaseDeDatos:
    def __init__(self):
        self.db: List[Usuario] = []

    # Método para obtener todos los usuarios
    def obtener_usuarios(self) -> List[Usuario]:
        return self.db

    # Método para obtener un usuario por su nombre de usuario
    def obtener_usuario(self, nombre_usuario: str) -> Union[Usuario, None]:
        for usuario in self.db:
            if usuario.usuario == nombre_usuario:
                return usuario
        return None

    # Método para editar un usuario
    def editar_usuario(self, nombre_usuario: str, nueva_info: Dict[str, Any]) -> bool:
        for usuario in self.db:
            if usuario.usuario == nombre_usuario:
                usuario_dict = usuario.dict()
                usuario_dict.update(nueva_info)
                usuario_nuevo = Usuario(**usuario_dict)
                self.db.remove(usuario)
                self.db.append(usuario_nuevo)
                return True
        return False

    # Método para crear un nuevo usuario
    def crear_usuario(self, nuevo_usuario: Dict[str, Any]) -> bool:
        if "usuario" in nuevo_usuario and "contraseña" in nuevo_usuario and \
           "tok1" in nuevo_usuario and "tok2" in nuevo_usuario and "tok3" in nuevo_usuario:
            usuario = Usuario(**nuevo_usuario)
            self.db.append(usuario)
            return True
        return False

# Creamos una instancia de la base de datos
db = BaseDeDatos()

# Ruta para obtener todos los usuarios
@app.get("/usuarios/", response_model=List[Usuario])
async def obtener_usuarios():
    return db.obtener_usuarios()

# Ruta para obtener un usuario por su nombre de usuario
@app.get("/usuarios/{usuario}", response_model=Usuario)
async def obtener_usuario(usuario: str):
    usuario_encontrado = db.obtener_usuario(usuario)
    if usuario_encontrado is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_encontrado

# Ruta para editar un usuario por su nombre de usuario
@app.put("/usuarios/{usuario}", response_model=dict)
async def editar_usuario(usuario: str, nueva_info: dict):
    if db.editar_usuario(usuario, nueva_info):
        return {"mensaje": "Usuario actualizado correctamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Ruta para crear un nuevo usuario
@app.post("/usuarios/", response_model=dict)
async def crear_usuario(nuevo_usuario: dict):
    if db.crear_usuario(nuevo_usuario):
        return {"mensaje": "Usuario creado correctamente"}
    raise HTTPException(status_code=400, detail="No se pudo crear el usuario")

