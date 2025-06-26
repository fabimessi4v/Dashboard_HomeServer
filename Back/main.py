from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import psutil
from datetime import datetime
from typing import List, Dict, Optional
import uvicorn

app = FastAPI(
    title="Disk Monitor API",
    description="API para monitoreo de espacio en disco en tiempo real",
    version="1.0.0"
)

# Configurar CORS para permitir peticiones desde cualquier origen (frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para validación de respuestas
class DiskInfo(BaseModel):
    path: str
    total_gb: float
    used_gb: float
    free_gb: float
    usage_percent: float

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    uptime_seconds: float

# Variable global para tracking del inicio del servicio
service_start_time = datetime.now()

def obtener_info_disco(ruta: str) -> Optional[DiskInfo]:
    """
    Entradas: ruta (string) - Ruta del disco a analizar
    Salidas: DiskInfo o None si hay error
    Descripción: Obtiene información detallada de uso de disco para una ruta específica
    """
    try:
        if not os.path.exists(ruta):
            return None
            
        uso = shutil.disk_usage(ruta)
        total_gb = uso.total / (1024**3)
        used_gb = uso.used / (1024**3)
        free_gb = uso.free / (1024**3)
        usage_percent = round((uso.used / uso.total) * 100, 2)

        # Retorna Clase DiskInfo
        return DiskInfo(
            path=ruta,
            total_gb=round(total_gb, 2),
            used_gb=round(used_gb, 2),
            free_gb=round(free_gb, 2),
            usage_percent=usage_percent
        )
    except Exception as e:
        print(f"Error obteniendo información de disco para {ruta}: {e}")
        return None


@app.get("/", tags=["Info"])
async def root():
    """
    Entradas: Ninguna
    Salidas: Información básica de la API
    Descripción: Endpoint raíz con información de la API
    """
    return {
        "message": "Disk Monitor API",
        "version": "1.0.0",
        "endpoints": {
            "/disks/path/{disk_path}": "Obtener información de un disco específico",
            "/health": "Estado de salud de la API"
        }
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Entradas: Ninguna
    Salidas: Estado de salud de la API
    Descripción: Endpoint para verificar el estado de la API
    """
    uptime = (datetime.now() - service_start_time).total_seconds()
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        uptime_seconds=round(uptime, 2)
    )

@app.get("/disks/path/{disk_path:path}", response_model=DiskInfo, tags=["Disks"])
async def get_disk_by_path(disk_path: str):
    """
    Entradas: disk_path (string) - Ruta del disco a consultar
    Salidas: Información específica del disco solicitado
    Descripción: Obtiene información de uso de disco para una ruta específica
    """
    # Agregar "/" al inicio si no lo tiene
    if not disk_path.startswith("/"):
        disk_path = "/" + disk_path
        
    disk_info = obtener_info_disco(disk_path)
    
    if not disk_info:
        raise HTTPException(
            status_code=404, 
            detail=f"No se pudo obtener información del disco en la ruta: {disk_path}"
        )
    
    return disk_info

def print_startup_info():
    """
    Entradas: Ninguna
    Salidas: Imprime información de inicio en consola
    Descripción: Muestra información sobre cómo acceder a la API
    """
    print("=" * 60)
    print("🚀 DISK MONITOR API - FastAPI")
    print("=" * 60)
    print("📍 API Base URL:")
    print("   http://localhost:8000")
    print()
    print("📚 Documentación interactiva:")
    print("   http://localhost:8000/docs")
    print("   http://localhost:8000/redoc")
    print()
    print("🔌 Endpoints principales:")
    print("   GET /disks              - Todos los discos")
    print("   GET /disks/path/{path}  - Disco específico")
    print("   GET /health             - Estado de la API")
    print()
    print("🌐 Para acceso desde la red, usa:")
    try:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"   http://{local_ip}:8000")
    except Exception as e:
        print("   http://[TU_IP]:8000")
    print()
    print("⚠️  CORS habilitado para desarrollo")
    print("=" * 60)

if __name__ == "__main__":
    print_startup_info()
    
    # Configuración del servidor
    uvicorn.run(
        "main:app",  # Cambia "main" por el nombre de tu archivo
        host="0.0.0.0",  # Permite acceso desde la red
        port=8000,
        reload=True,  # Recarga automática en desarrollo
        log_level="info"
    )