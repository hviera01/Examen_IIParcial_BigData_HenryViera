import os
import pandas as pd

def cargar_csv_en_chunks(nombres, chunksize):
    for n in nombres:
        if os.path.exists(n):
            return pd.read_csv(n, chunksize=chunksize)
    raise FileNotFoundError("No se encontró ninguno de los archivos: " + ", ".join(nombres))

def main():
    chunks = cargar_csv_en_chunks(["ventas.csv", "Ventas.csv"], chunksize=1000)
    total_final_global = 0.0
    ventas_por_producto = {}
    contribucion_chunks = []
    if isinstance(chunks, pd.DataFrame):
        chunks = [chunks]
    for i, chunk in enumerate(chunks, start=1):
        if "Precio_Unitario" in chunk.columns:
            precio_col = "Precio_Unitario"
        elif "PrecioUnitario" in chunk.columns:
            precio_col = "PrecioUnitario"
        else:
            raise KeyError("No se encontró la columna de precio unitario")
        cantidad_col = "Cantidad"
        total_col = "Total"
        chunk[cantidad_col] = pd.to_numeric(chunk[cantidad_col], errors="coerce").fillna(0)
        chunk[precio_col] = pd.to_numeric(chunk[precio_col], errors="coerce").fillna(0)
        chunk[total_col] = pd.to_numeric(chunk[total_col], errors="coerce").fillna(0)
        chunk["Subtotal"] = chunk[cantidad_col] * chunk[precio_col]
        chunk["Tasa_Impuesto"] = 0.0
        chunk.loc[chunk[total_col] < 5000, "Tasa_Impuesto"] = 0.10
        chunk.loc[(chunk[total_col] >= 5000) & (chunk[total_col] <= 20000), "Tasa_Impuesto"] = 0.15
        chunk.loc[chunk[total_col] > 20000, "Tasa_Impuesto"] = 0.18
        chunk["Impuesto"] = chunk[total_col] * chunk["Tasa_Impuesto"]
        chunk["Total_Final"] = chunk[total_col] + chunk["Impuesto"]
        suma_chunk = chunk["Total_Final"].sum()
        total_final_global += suma_chunk
        contribucion_chunks.append((i, suma_chunk))
        totales_por_producto = chunk.groupby("Producto")["Total_Final"].sum()
        for producto, monto in totales_por_producto.items():
            ventas_por_producto[producto] = ventas_por_producto.get(producto, 0) + float(monto)
    top_5 = sorted(ventas_por_producto.items(), key=lambda x: x[1], reverse=True)[:5]
    if contribucion_chunks:
        chunk_mayor = max(contribucion_chunks, key=lambda x: x[1])[0]
    else:
        chunk_mayor = None
    print("Total Final Global:", total_final_global)
    print("Top 5 productos más vendidos:")
    for producto, monto in top_5:
        print(producto, monto)
    print("Chunk con mayor contribución en ventas:", chunk_mayor)

if __name__ == "__main__":
    main()
