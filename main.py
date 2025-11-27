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
        import src.csvjsonapp.app
        import src.csvjsonapp.csv_reader
        import src.csvjsonapp.json_generator
        import src.csvjsonapp.json_writer
        import src.csvjsonapp.logger
        import src.csvjsonapp.photo_finder
        import src.csvjsonapp.template_loader
        import src.csvjsonapp.template_processor
        import src.csvjsonapp.interfaces
        
        current_dir = os.getcwd()
        
        if hasattr(sys, '_MEIPASS'):
            base_dir = sys._MEIPASS
        else:
            try:
                base_dir = os.path.dirname(os.path.abspath(__file__))
            except:
                base_dir = current_dir
        
        possible_paths = [current_dir, base_dir]
        for path_dir in possible_paths:
            src_path = os.path.join(path_dir, "src", "csvjsonapp")
            if os.path.exists(src_path):
                if path_dir not in sys.path:
                    sys.path.insert(0, path_dir)
                break
        else:
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)
            if base_dir not in sys.path and base_dir != current_dir:
                sys.path.insert(0, base_dir)
        
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

