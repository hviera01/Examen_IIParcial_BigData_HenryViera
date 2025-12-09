import os
import pandas as pd

def cargar_csv(nombres):
    for n in nombres:
        if os.path.exists(n):
            return pd.read_csv(n)
    raise FileNotFoundError("No se encontró ninguno de los archivos: " + ", ".join(nombres))

def sanitize_name(name):
    if not isinstance(name, str):
        name = str(name)
    invalid = '"\'<>:/\\|?*'
    for ch in invalid:
        name = name.replace(ch, "")
    name = name.replace(" ", "_")
    name = name.strip("_")
    if not name:
        name = "desconocido"
    return name

def main():
    ventas = cargar_csv(["ventas.csv", "Ventas.csv"])
    if "Precio_Unitario" in ventas.columns:
        precio_col = "Precio_Unitario"
    elif "PrecioUnitario" in ventas.columns:
        precio_col = "PrecioUnitario"
    else:
        raise KeyError("No se encontró la columna de precio unitario")
    ventas["Total"] = pd.to_numeric(ventas["Total"], errors="coerce").fillna(0)
    ventas[precio_col] = pd.to_numeric(ventas[precio_col], errors="coerce").fillna(0)
    base_dir = "salidas"
    os.makedirs(base_dir, exist_ok=True)
    resumen_global = []
    for producto, grupo in ventas.groupby("Producto"):
        nombre_limpio = sanitize_name(producto)
        carpeta = os.path.join(base_dir, f"Producto={nombre_limpio}")
        os.makedirs(carpeta, exist_ok=True)
        archivo_csv = os.path.join(carpeta, "archivo.csv")
        grupo.to_csv(archivo_csv, index=False)
        total_ventas = grupo["Total"].sum()
        cantidad_registros = len(grupo)
        precio_promedio = grupo[precio_col].mean()
        resumen_txt = os.path.join(carpeta, "resumen.txt")
        with open(resumen_txt, "w", encoding="utf-8") as f:
            f.write(f"Producto: {producto}\n")
            f.write(f"Total de ventas: {total_ventas}\n")
            f.write(f"Cantidad de registros: {cantidad_registros}\n")
            f.write(f"Precio unitario promedio: {precio_promedio}\n")
        resumen_global.append({
            "Producto": producto,
            "Total_Ventas": total_ventas,
            "Cantidad_Registros": cantidad_registros,
            "PrecioUnitario_Promedio": precio_promedio
        })
    df_resumen_global = pd.DataFrame(resumen_global)
    df_resumen_global.to_csv(os.path.join(base_dir, "resumen_global.csv"), index=False)

if __name__ == "__main__":
    main()
