from fusionauth.fusionauth_client import FusionAuthClient

from app import app, db, AppError

fa = None

def setup_fa():
    # Delete User For A Given ID
    global fa

    if fa is None:
        fa = FusionAuthClient(app.config['API_KEY'], app.config['FA_INTERNAL_URL'])
    return fa
