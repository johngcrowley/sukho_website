import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Load .env file as Environment Variables
load_dotenv()

class Config(object):

    DEBUG = False

    #General Config
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_ENV = os.environ.get("FLASK_ENV")
    SECRET_KEY = os.environ.get("SECRET_KEY")


    #GOOGLE SHEETS API client_secret.json 
    def create_keyfile_dict():
        variables_keys = {
            "type": os.environ.get("SHEET_TYPE"),
            "project_id": os.environ.get("SHEET_PROJECT_ID"),
            "private_key_id": os.environ.get("SHEET_PRIVATE_KEY_ID"),
            "private_key": os.environ.get("SHEET_PRIVATE_KEY"),
            "client_email": os.environ.get("SHEET_CLIENT_EMAIL"),
            "client_id": os.environ.get("SHEET_CLIENT_ID"),
            "auth_uri": os.environ.get("SHEET_AUTH_URI"),
            "token_uri": os.environ.get("SHEET_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.environ.get("SHEET_AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": os.environ.get("SHEET_CLIENT_X509_CERT_URL")
        }
        return variables_keys

    #Call Google Sheets API
    scopes = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(create_keyfile_dict(),scopes)
    client = gspread.authorize(creds)
    google_sh = client.open("test")
    spreadsheet_key = '1DG3-SL2-qz0b58yE4wdQ2eE6SGg4p5-CY3MGJtlsRuA'
    wks_name = ['Marigny','Uptown']

class ProductionConfig(Config):
    DEBUG = False
    #DB Config
    SQLALCHEMY_DATABASE_URI = os.environ.get("PRODUCTION_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    #DB Config
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False