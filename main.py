from backend.app import get_app

if __name__ == '__main__':
    print(f'starting from main.py')

    app = get_app()
    print(app.url_map)
    app.run(host='0.0.0.0', port=5000)  # to be able to run in container
