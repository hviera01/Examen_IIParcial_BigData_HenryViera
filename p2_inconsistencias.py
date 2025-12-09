import os
import pandas as pd

def cargar_csv(nombres):
    for n in nombres:
        if os.path.exists(n):
            return pd.read_csv(n)
    raise FileNotFoundError("No se encontró ninguno de los archivos: " + ", ".join(nombres))

def main():
    ventas = cargar_csv(["ventas.csv", "Ventas.csv"])
    if "Precio_Unitario" in ventas.columns:
        precio_col = "Precio_Unitario"
    elif "PrecioUnitario" in ventas.columns:
        precio_col = "PrecioUnitario"
    else:
        raise KeyError("No se encontró la columna de precio unitario")
    cantidad_col = "Cantidad"
    total_col = "Total"
    ventas[cantidad_col] = pd.to_numeric(ventas[cantidad_col], errors="coerce")
    ventas[precio_col] = pd.to_numeric(ventas[precio_col], errors="coerce")
    ventas[total_col] = pd.to_numeric(ventas[total_col], errors="coerce")
    ventas["Subtotal"] = ventas[cantidad_col] * ventas[precio_col]
    ventas["Error_Relativo"] = (ventas["Subtotal"] - ventas[total_col]).abs() / ventas[total_col].abs()
    ventas.loc[ventas[total_col] == 0, "Error_Relativo"] = pd.NA
    inconsistentes = ventas[ventas["Error_Relativo"] > 0.05].copy()
    inconsistentes.to_csv("inconsistencias.csv", index=False)
    total_inconsistentes = len(inconsistentes)
    promedio_error = inconsistentes["Error_Relativo"].astype("float64").mean() if total_inconsistentes > 0 else None
    if total_inconsistentes > 0:
        producto_mas_inconsistente = inconsistentes["Producto"].value_counts().idxmax()
    else:
        producto_mas_inconsistente = None
    print("Total de registros inconsistentes:", total_inconsistentes)
    print("Promedio del error relativo:", promedio_error)
    print("Producto con más inconsistencias:", producto_mas_inconsistente)

if __name__ == "__main__":
    main()
