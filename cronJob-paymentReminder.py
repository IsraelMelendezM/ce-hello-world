import os 
from twilio.rest import Client
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from datetime import datetime, timedelta
import pandas as pd

from dotenv import load_dotenv


def as_spanish(dt: datetime):
    days_name = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
    month_name = ['Enero', 'Febrero','Marzo','Abril', 'Mayo', 'Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    
    wd = days_name[dt.weekday()]
    md = month_name[int(dt.strftime('%m')) - 1]
    dd = int(dt.strftime('%d'))
    yd = dt.year
    
    if dd == 1:
        dd = "primero"
        
    return f'{wd}, {dd} de {md} de {yd}'


def twilio_reminder(clientData:dict):
    
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID") #Israel enterprise account
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN") # Israel Enterprise account
    twilio_client = Client(account_sid, auth_token)
    #
    formatted_date = datetime.strptime(clientData["should_pay_by"], "%Y-%m-%d")

    fecha = as_spanish(formatted_date)
    dinero = clientData["toPayAfterDiscount"]
    nombre = clientData["name"].split(" ")[0]
    numero = str(clientData["phone_number"])	

    number =f"+52{numero}"
    to = "whatsapp:" + number
    from_ = "whatsapp:"+os.environ.get("TRIAL_NUMBER")
    msg = f"""¡Hola {nombre}! Como recordatorio debes una cantidad de: ${dinero} MXN para el día {fecha}.
    ¿Te redirijo a la app para pagar de una vez?"""

    try:
        message = twilio_client.messages.create(to=to, from_=from_, body=msg)
        response = message.sid if message.sid else ''
        print("Twilio msg response:", response)
    except Exception as e:
        print('Could not send whatsapp notification to', number)
        print('Could not send whatsapp TwilioException', str(e))

def main():
    load_dotenv()
    CLOUDANT_URL = os.environ.get("CLOUDANT_URL")
    CLOUDANT_API_KEY =os.environ.get("CLOUDANT_API_KEY") 
    DB = "test-distribuidores"
    authenticator = IAMAuthenticator(CLOUDANT_API_KEY)
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(CLOUDANT_URL)

    response = client.post_all_docs(
        db=DB,
        include_docs=True,
        ).get_result()
        
    docs = []
    for item in response['rows']:
        if '_design' not in item['doc']['_id']:
            docs.append(item['doc'])
            
    df = pd.DataFrame(docs)
    clientData = df.to_dict(orient='records')
    print(df)
    for doc in clientData:

        try: 
            # print(doc)
            due_date = datetime.strptime(doc["should_pay_by"], "%Y-%m-%d")- timedelta(days=2)
            todays_date = datetime.now()
            
            if (due_date-todays_date).days == 0:
                ...
                # twilio_reminder(doc)
        except Exception as err:
            print(err, "error sending message through Twilio")
main()
