from modulo_web.utils.export_db_a_json import exportar_sqlite_a_json

def main():
    archivo = exportar_sqlite_a_json()
    print(f"Backup generado en: {archivo}")

if __name__ == "__main__":
    main()