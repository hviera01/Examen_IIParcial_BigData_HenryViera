import os
import pandas as pd

def cargar_csv(nombres):
    for n in nombres:
        if os.path.exists(n):
            return pd.read_csv(n)
    raise FileNotFoundError("No se encontró ninguno de los archivos: " + ", ".join(nombres))

def main():
    ventas = cargar_csv(["ventas.csv", "Ventas.csv"])
    clientes = cargar_csv(["clientes.csv", "Clientes.csv"])
    if "Precio_Unitario" in ventas.columns:
        precio_col = "Precio_Unitario"
    elif "PrecioUnitario" in ventas.columns:
        precio_col = "PrecioUnitario"
    else:
        raise KeyError("No se encontró la columna de precio unitario")
    ventas["Total"] = pd.to_numeric(ventas["Total"], errors="coerce").fillna(0)
    ventas[precio_col] = pd.to_numeric(ventas[precio_col], errors="coerce").fillna(0)
    ventas["Cliente"] = ventas["Cliente"].astype(str)
    clientes["Cliente"] = clientes["Cliente"].astype(str)
    df = ventas.merge(clientes, on="Cliente", how="inner")
    df_group = df.groupby(["Cliente", "Producto", "Ciudad", "Categoria_Cliente"], as_index=False).agg(
        Total_Ventas=("Total", "sum"),
        PrecioUnitario_Promedio=(precio_col, "mean"),
        Cantidad_Compras=("Total", "count")
    )
    df_group = df_group.sort_values(by=["Ciudad", "Total_Ventas"], ascending=[True, False])
    df_group.to_csv("reporte_multinivel.csv", index=False)
    ciudad_totales = df_group.groupby("Ciudad")["Total_Ventas"].sum()
    if not ciudad_totales.empty:
        ciudad_mayor = ciudad_totales.idxmax()
    else:
        ciudad_mayor = None
    variedad = df.groupby("Cliente")["Producto"].nunique()
    if not variedad.empty:
        cliente_mayor_variedad = variedad.idxmax()
    else:
        cliente_mayor_variedad = None
    print("Ciudad con mayor volumen total:", ciudad_mayor)
    print("Cliente con mayor variedad de productos:", cliente_mayor_variedad)

if __name__ == "__main__":
    main()
