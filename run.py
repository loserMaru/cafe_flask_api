from app import create_app

if __name__ == "__main__":
    # Создание приложения и его запуск
    app = create_app()
    app.run(debug=True)
