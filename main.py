import sys
import os
import traceback

def log_error(error_msg: str):
    try:
        log_dir = os.path.join(os.path.expanduser("~"), "csv_json_generator_logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "error.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Error: {error_msg}\n")
            f.write(traceback.format_exc())
    except:
        pass

if __name__ == "__main__":
    try:
        log_error("Starting application...")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(base_dir, "src")
        if os.path.exists(src_dir):
            sys.path.insert(0, base_dir)
        log_error(f"Base dir: {base_dir}, sys.path: {sys.path[:3]}")
        from src.csvjsonapp.app import main
        import flet as ft
        log_error("Imports successful, starting Flet app...")
        ft.app(target=main)
    except Exception as e:
        error_msg = f"Критическая ошибка: {e}"
        log_error(error_msg)
        try:
            print(error_msg)
            print(traceback.format_exc())
            input("Нажмите Enter для выхода...")
        except:
            pass
        sys.exit(1)

