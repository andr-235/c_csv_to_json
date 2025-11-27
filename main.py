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
        
        # Add Lib directory to Python path if it exists (for built app)
        lib_dir = os.path.join(base_dir, "Lib")
        if os.path.exists(lib_dir):
            sys.path.insert(0, lib_dir)
            log_error(f"Added Lib directory to sys.path: {lib_dir}")
        
        log_error(f"Base dir: {base_dir}, sys.path: {sys.path[:5]}")
        
        # Test encodings import before proceeding
        try:
            import encodings
            log_error("encodings module imported successfully")
        except ImportError as ie:
            error_msg = f"Ошибка импорта encodings: {ie}\nПроверьте наличие стандартной библиотеки Python."
            log_error(error_msg)
            try:
                import flet as ft
                def error_main(page: ft.Page):
                    page.add(
                        ft.Text("Ошибка запуска", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.RED),
                        ft.Text(error_msg, size=12, selectable=True, expand=True),
                        ft.Text(f"\nBase dir: {base_dir}\nLib dir exists: {os.path.exists(lib_dir)}", size=10),
                        ft.ElevatedButton("Закрыть", on_click=lambda _: page.window.close())
                    )
                    page.update()
                ft.app(target=error_main)
            except:
                pass
            sys.exit(1)
        
        from src.csvjsonapp.app import main
        import flet as ft
        log_error("Imports successful, starting Flet app...")
        ft.app(target=main)
    except Exception as e:
        error_msg = f"Критическая ошибка: {e}"
        log_error(error_msg)
        log_error(traceback.format_exc())
        try:
            import flet as ft
            def error_main(page: ft.Page):
                page.add(
                    ft.Text("Ошибка запуска", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.RED),
                    ft.Text(error_msg, size=12, selectable=True, expand=True),
                    ft.Text(traceback.format_exc(), size=10, selectable=True, expand=True),
                    ft.ElevatedButton("Закрыть", on_click=lambda _: page.window.close())
                )
                page.update()
            ft.app(target=error_main)
        except:
            try:
                print(error_msg)
                print(traceback.format_exc())
                input("Нажмите Enter для выхода...")
            except:
                pass
        sys.exit(1)

