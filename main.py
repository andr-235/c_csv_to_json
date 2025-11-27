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
        print(f"ERROR: {error_msg}", file=sys.stderr, flush=True)
        print(traceback.format_exc(), file=sys.stderr, flush=True)
    except:
        pass

if __name__ == "__main__":
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        current_dir = os.getcwd()
        
        if os.path.exists(os.path.join(base_dir, "src")):
            sys.path.insert(0, base_dir)
        
        if os.path.exists(os.path.join(current_dir, "src")) and current_dir != base_dir:
            sys.path.insert(0, current_dir)
        
        from src.csvjsonapp.app import main
        import flet as ft
        ft.app(target=main)
    except Exception as e:
        error_msg = f"Критическая ошибка: {e}\n\n{traceback.format_exc()}"
        log_error(error_msg)
        try:
            import flet as ft
            def error_main(page: ft.Page):
                page.window.width = 900
                page.window.height = 700
                page.add(
                    ft.Text("Ошибка запуска", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.RED),
                    ft.Text(error_msg, size=10, selectable=True, expand=True),
                    ft.ElevatedButton("Закрыть", on_click=lambda _: page.window.close())
                )
                page.update()
            ft.app(target=error_main)
        except:
            print(error_msg, file=sys.stderr, flush=True)
        sys.exit(1)

