import logging as logger
import os
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from helpers.TwilioAdapter import MessageClient
from helpers.OTPGenerator import Generate
from helpers.Cloudant import GetClientDetails
from helpers.Cloudant import sp_time, as_spanish, offset_days

logger.basicConfig(level="DEBUG")

app = FastAPI()


class EngineRequest(BaseModel):
    case:str
    id: str = "0070055874"
    phoneNo: str = "8110423455"
    otp: int = 1234


@app.get("/")
async def root():
    return {"message": "Hello World"}

def clientData(data):
    ## Obtener datos importantes con el ID de distribuidor
    try:
        service = GetClientDetails()
    except Exception as err:
        return(err)
    # logger.debug("DISTRIBUTOR ID",  data)
    doc = service.get_doc_by_key(dbName='test-distribuidores',
                            ddoc='clientes',
                            key=data["id"],
                            view='daily_record')
    if doc is None:
         raise HTTPException(status_code=404, 
                             detail="Distributor ID not found in Database")

    # logger.debug(doc)
    pay_by_date_dt = datetime.strptime(doc['should_pay_by'], '%Y-%m-%d')

    cst = sp_time(pay_by_date_dt, 0, 'cst')
    
    # print(doc)
    benefits_str = ', '.join([item['name'] for item in doc['benefits']['items'] ])
    
    return {'record': doc,
        'benefits': benefits_str,
        'hubo_respuesta': 1,
        'first_name':doc['name'].split(' ')[0],
        'should_pay_by_date_sp': as_spanish(cst),
        'should_pay_by_date_minus_4_sp': as_spanish(offset_days(cst,-3))
    }


def generate_and_send_otp(data):
    phoneNo = data["phoneNo"]
    if not phoneNo:
       return {"error": "phoneNo is required"}

    otpObject = Generate()
    otp = otpObject.OTP()

    time = datetime.now()
    logger.debug(type(time))

    message = f"Tu código de verificación es *{otp}*. Por tu seguridad, no lo compartas."
    number = str(phoneNo)

    metadata = {
        "phone_no": number,
        "otp": str(otp),
        "time": time.strftime("%H:%M")
    }

    with open('otpValidity.json', 'w') as fs:
        json.dump(metadata, fs, indent=2)

    try:
        twilioObject = MessageClient()
        twilioObject.send_message(message, number)
        logger.debug(message)
    except Exception as e:
        return {"error": str(e)}

    return metadata


def auth(data):
    
    phoneNo = data["phoneNo"]
    otp = data["otp"]

    with open('otpValidity.json', 'r') as fs:
        otpFile = json.loads(fs.read())

    otpGeneratedTime = datetime.strptime(otpFile.get('time'), '%H:%M')

    nowTime = datetime.now()

    delta = nowTime - otpGeneratedTime
    timeDiff = int(delta.seconds / 60) # in minutes
    logger.debug(timeDiff)

    authenticated = False
    validationMsg = ""
    

    if int(otpFile.get('otp')) != otp:
        validationMsg = "Invalid OTP"
    elif timeDiff > 5:
        validationMsg = "OTP Expired"
    else:
        authenticated = True
        validationMsg = "OTP Validated"
    # TODO: mandar que se validó a Cloudant BD
    return {
        "phone_no": phoneNo,
        "authentication": authenticated,
        "validation_msg": validationMsg
    }

@app.post("/engine")
async def engine(request_data: EngineRequest):
    
    load_dotenv()
    host = os.environ.get("HOST")
    port = os.environ.get("PORT")
    case = request_data.case
    id = request_data.id
    phoneNo = request_data.phoneNo
    otp = request_data.otp

    if case == "get_client_details":
        data = {'id':id}
        try:
            inp_post_response =  clientData( data)
            return inp_post_response
            
        except Exception as e:
             return {"error": str(e)}
        
    elif case == "send_otp":    
        data = {"phoneNo": phoneNo}
        try:
            inp_post_response =  generate_and_send_otp(data)
            return inp_post_response
        
        except Exception as e:
             return {"error": str(e)}
        
    elif case == "auth":
        data = {"phoneNo": str(phoneNo), "otp": int(otp)}

        try:
            inp_post_response =  auth(data)
            return inp_post_response
            
        except Exception as e:
             return {"error": str(e)}
                 
    else:
         return {"error": "No cases ran."}
    

port = os.getenv('VCAP_APP_PORT', '8080')
if __name__ == "__main__":
    logger.debug("Starting the Application")
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=True)