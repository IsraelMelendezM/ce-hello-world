from datetime import datetime, timedelta, timezone

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1
import os
import load_dotenv

def offset_days(dt:datetime = None, days:int =0):
    return dt + timedelta(days=days)

def offset_dt(hours: int = 0, name: str = 'custom'):
    offsetTimeDelta = timedelta(hours=hours)
    offsetTZObject = timezone(offsetTimeDelta, name=name)
    return offsetTZObject
    
def sp_time(dt: datetime = None, hours: int = 0, name: str = 'custom'):
    dt_tz = dt.astimezone(offset_dt(hours, 'cst'))
    return dt_tz
            
def as_spanish(dt: datetime):
    days_name = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
    month_name = ['Enero', 'Febrero','Marzo','Abril', 'Mayo', 'Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    
    wd = days_name[dt.weekday()]
    md = month_name[int(dt.strftime('%m')) - 1]
    dd = int(dt.strftime('%d'))
    yd = dt.year
    if dd == 1:
        dd = 'primero'
    return f'{wd}, {dd} de {md} de {yd}'

def get_doc_by_key(
        ddoc: str, 
        view: str, 
        key: str , 
        client: CloudantV1 , 
        dbName: str ,
        **kwargs):
        try:
            _response = client.post_view(
                db=dbName,
                ddoc=ddoc,
                view=view,
                include_docs=True,
                key=key,
                **kwargs)
            print(_response)
            if _response.status_code == 200:
                #_result = _response.result['rows']
                if len(_response.result['rows']) > 0:
                    _result = _response.result['rows'][0]['doc']
                else:
                    _result = None
            else:
                print('post_view failed finding the wdn_id')
                #log more data
        except Exception as err:
            print(f'ApiException getting value {err}')
            raise Exception('get_doc_by_key: Problem getting document by id from view')
            
        return _result


class GetClientDetails:
    def __init__(self) :

        load_dotenv()

        credentials = {'CLOUDANT_API_KEY':os.environ("CLOUDANT_API_KEY"),
                        'CLOUDANT_URL':os.environ("CLOUDANT_URL")}
        
        authenticator = IAMAuthenticator(credentials['CLOUDANT_API_KEY'])
        self.client = CloudantV1(authenticator=authenticator)
        self.client.set_service_url(credentials['CLOUDANT_URL'])

        print("Connected to Cloudant")

    def get_doc_by_key(self, dbName, ddoc, key, view):

        try:
            _response = self.client.post_view(
                db=dbName,
                ddoc=ddoc,
                view=view,
                include_docs=True,
                key=key
                )
            if _response.status_code == 200:
                if len(_response.result['rows']) > 0:
                    _result = _response.result['rows'][0]['doc']
                else:
                    _result = None
            else:
                print('post_view failed finding the wdn_id')
                #log more data
        except Exception as err:
            print(f'ApiException getting value {err}')
            raise Exception('get_doc_by_key: Problem getting document by id from view')
            
        return _result