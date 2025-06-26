import { useEffect, useState } from "react";
import DiskChart from "./components/diskchart";

function App() {
  const [disks, setDisks] = useState([]);

  useEffect(() => {
    const rutas = ["/home/Disco_4TB", "/home/Disco_500GB"];

    Promise.all(
      rutas.map((ruta) =>
        fetch(`http://192.168.100.248:8000/disks/path${ruta}`)
          .then((res) => {
            if (!res.ok) throw new Error(`Error en ${ruta}`);
            return res.json();
          })
          .then((data) => ({ ...data, id: ruta }))
          .catch((err) => {
            console.error(err);
            return null;
          })
      )
    ).then((results) => {
      setDisks(results.filter((disk) => disk !== null));
    });
  }, []);

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#f3f4f6", color: "#1f2937", padding: "24px" }}>
      <h1 style={{ fontSize: "2rem", fontWeight: "bold", marginBottom: "24px", textAlign: "center" }}>
        📊 Dashboard de Discos
      </h1>

      {disks.length === 0 ? (
        <p style={{ textAlign: "center" }}>Cargando información de los discos...</p>
      ) : (
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",        // para que bajen si no caben
            gap: "24px",
            justifyContent: "center",
          }}
        >
          {disks.map((disk) => (
            <div
              key={disk.id}
              style={{
                backgroundColor: "white",
                borderRadius: "1rem",
                boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
                padding: "16px",
                flexGrow: 1,           // que crezca para ocupar espacio disponible
                flexBasis: "300px",    // ancho base mínimo
                minWidth: "1080px",     // ancho mínimo para que no quede muy chico
                boxSizing: "border-box",
                maxWidth: "1080px",     // opcional, para que no crezca demasiado
              }}
            >
              <h2 style={{ fontSize: "1.25rem", fontWeight: "600", marginBottom: "12px" }}>
                📁 Ruta: {disk.path}
              </h2>
              <p><strong>Total:</strong> {disk.total_gb} GB</p>
              <p><strong>Usado:</strong> {disk.used_gb} GB</p>
              <p><strong>Libre:</strong> {disk.free_gb} GB</p>
              <p><strong>Uso:</strong> {disk.usage_percent}%</p>

              <div style={{ marginTop: "16px" }}>
                <DiskChart diskData={disk} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
