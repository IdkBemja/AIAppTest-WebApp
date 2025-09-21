from app import app
from app.controllers import app_controller, api_controller
from app.utils.config.env_config import get_port
from app.utils.mysqlhandler import ensure_databases_and_tables

ensure_databases_and_tables()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=get_port(), debug=True)