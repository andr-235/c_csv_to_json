import sys
import traceback
import os

def log_error(error_msg: str):
    try:
        log_dir = os.path.join(os.path.expanduser("~"), "csv_json_generator_logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "error.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Error: {error_msg}\n")
            f.write(traceback.format_exc())
    except Exception as log_err:
        try:
            with open("error.log", "a", encoding="utf-8") as f:
                f.write(f"Error logging failed: {log_err}\nOriginal: {error_msg}\n")
        except:
            pass

if __name__ == "__main__":
    try:
        log_error("Starting application...")
        from csvjsonapp.app import main
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
