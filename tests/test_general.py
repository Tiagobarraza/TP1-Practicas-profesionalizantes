# tests/test_general.py
import pytest
from fastapi.testclient import TestClient
from app.main import app  # Importación desde el paquete app/[cite: 2]
from app.database import db_usuarios, db_productos  # Importamos las listas en memoria[cite: 2]

client = TestClient(app)

# Fixture para limpiar las listas en memoria antes de cada test
@pytest.fixture(autouse=True)
def reset_db():
    db_usuarios.clear()
    db_productos.clear()
    yield

# ==========================================
# EJERCICIO 1: Pruebas del Componente Usuarios
# ==========================================

def test_1_1_registro_exitoso():
    # Validar que al enviar un JSON con los datos requeridos devuelva 201 Created[cite: 2].
    response = client.post("/users", json={"username": "usuario_valido", "edad": 25})
    assert response.status_code == 201

def test_1_2_fallo_validacion_esquema():
    # Comprobar que un usuario inválido (edad < 18) devuelve 422 Unprocessable Entity[cite: 2].
    response = client.post("/users", json={"username": "user123", "edad": 15})
    assert response.status_code == 422

def test_1_3_control_de_duplicados():
    # Validar que si el usuario ya existe, responda con 400 Bad Request[cite: 2].
    client.post("/users", json={"username": "mismo_usuario", "edad": 30})
    response_duplicado = client.post("/users", json={"username": "mismo_usuario", "edad": 30})
    assert response_duplicado.status_code == 400

def test_1_4_busqueda_por_id_y_parametros():
    # Para buscar, primero insertamos manualmente un usuario en nuestra BD simulada
    db_usuarios.append({"id": 1, "username": "testuser", "edad": 25})

    # Comprobar ID existente devuelve 200 OK y categoría por defecto "general"[cite: 2].
    response_ok = client.get("/users/1")
    assert response_ok.status_code == 200
    assert response_ok.json().get("categoria") == "general"

    # Validar que si el ID no existe devuelva 404 Not Found[cite: 2].
    response_not_found = client.get("/users/99")
    assert response_not_found.status_code == 404

    # Verificar validación Path Parameter (user_id > 0) devuelve 422[cite: 2].
    response_invalido = client.get("/users/0")
    assert response_invalido.status_code == 422

# ==========================================
# EJERCICIO 2: Pruebas sobre Seguridad e Inyección Local
# ==========================================

def test_2_1_acceso_concedido_token_correcto():
    # Enviar petición POST con el token correcto retorna 201 Created[cite: 2].
    response = client.post(
        "/products?token=nivel-intermedio-2026", 
        json={"nombre": "Teclado Mecánico", "precio": 50000}
    )
    assert response.status_code == 201

def test_2_2_acceso_denegado_token_incorrecto():
    # Enviar petición POST con token erróneo o ausente retorna 401 Unauthorized[cite: 2].
    response_erroneo = client.post(
        "/products?token=token-falso", 
        json={"nombre": "Mouse", "precio": 15000}
    )
    assert response_erroneo.status_code == 401

    response_ausente = client.post(
        "/products", 
        json={"nombre": "Monitor", "precio": 120000}
    )
    assert response_ausente.status_code == 401

# ==========================================
# EJERCICIO 3: Pruebas de Bloqueo Perimetral Global
# ==========================================

def test_3_1_proteccion_por_enrutador():
    # Petición GET para listar productos (sin Depends manual) retorna 401 Unauthorized sin token[cite: 2].
    response = client.get("/products")
    assert response.status_code == 401