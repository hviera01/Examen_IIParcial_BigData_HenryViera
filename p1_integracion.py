import os
import pandas as pd

def cargar_csv(nombres):
    for n in nombres:
        if os.path.exists(n):
            return pd.read_csv(n)
    raise FileNotFoundError("No se encontró ninguno de los archivos: " + ", ".join(nombres))

def convertir_numerico(df, columna):
    if columna not in df.columns:
        return df
    serie = pd.to_numeric(df[columna], errors="coerce")
    promedio = serie.mean()
    serie = serie.fillna(promedio)
    df[columna] = serie
    return df

def main():
    ventas = cargar_csv(["ventas.csv", "Ventas.csv"])
    clientes = cargar_csv(["clientes.csv", "Clientes.csv"])
    productos = cargar_csv(["productos.csv", "Productos.csv"])
    if "Precio_Unitario" in ventas.columns:
        precio_col = "Precio_Unitario"
    elif "PrecioUnitario" in ventas.columns:
        precio_col = "PrecioUnitario"
    else:
        raise KeyError("No se encontró la columna de precio unitario")
    cantidad_col = "Cantidad"
    total_col = "Total"
    ventas = convertir_numerico(ventas, cantidad_col)
    ventas = convertir_numerico(ventas, precio_col)
    ventas = convertir_numerico(ventas, total_col)
    ventas["Cliente"] = ventas["Cliente"].astype(str)
    ventas["Producto"] = ventas["Producto"].astype(str)
    clientes["Cliente"] = clientes["Cliente"].astype(str)
    productos["Producto"] = productos["Producto"].astype(str)
    filas_iniciales = len(ventas)
    ventas = ventas[ventas["Producto"].isin(productos["Producto"])]
    filas_despues_producto = len(ventas)
    ventas = ventas[ventas["Cliente"].isin(clientes["Cliente"])]
    filas_finales = len(ventas)
    rechazadas = filas_iniciales - filas_finales
    df_merged = ventas.merge(clientes, on="Cliente", how="inner")
    df_merged = df_merged.merge(productos, on="Producto", how="inner")
    print("Filas iniciales:", filas_iniciales)
    print("Filas después de validar producto:", filas_despues_producto)
    print("Filas finales:", filas_finales)
    print("Filas rechazadas:", rechazadas)
    print(df_merged.head(10))

if __name__ == "__main__":
    main()
