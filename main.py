import logging as logger
import os
import json
from datetime import datetime
from fastapi import FastAPI
import requests
from pprint import pprint 
from pydantic import BaseModel
import ibm_db

from helpers.TwilioAdapter import MessageClient
from helpers.OTPGenerator import Generate
from helpers.Cloudant import GetClientDetails
from helpers.Cloudant import sp_time, as_spanish, offset_days
from typing import Any

logger.basicConfig(level="DEBUG")

app = FastAPI()

class ClientID(BaseModel):
    id: str

class AuthRequest(BaseModel):
    phoneNo: int
    otp: int

class AuthResponse(BaseModel):
    phone_no: int
    authentication: bool
    client_no: str
    validation_msg: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/getClientDetails")
async def clientData(data: ClientID):
    ## Obtener datos importantes con el ID de distribuidor
    try:
        service = GetClientDetails()
        logger.debug(data.id)
        doc = service.get_doc_by_key(dbName='test-distribuidores',
                          ddoc='clientes',
                          key=str(data.id),
                            view='daily_record')
        logger.debug(doc)
        pay_by_date_dt = datetime.strptime(doc['should_pay_by'], '%Y-%m-%d')

        cst = sp_time(pay_by_date_dt, 0, 'cst')
        
        # print(doc)
        benefits_str = ', '.join([item['name'] for item in doc['benefits']['items'] ])
        
        return {'record': doc,
            'benefits': benefits_str,
            'hubo_respuesta': 1,
            'first_name':doc['name'].split(' ')[0],
            'should_pay_by_date_sp': as_spanish(cst),
            'should_pay_by_date_minus_4_sp': as_spanish(offset_days(cst,-3)),
        }
    except Exception as err:
        return {"Error":f"could not return any function {err}"}


@app.post('/generate_and_send_otp/')
def generate_and_send_otp(phoneNo: str):
	logger.debug("GenerateAndSendOTP -> inside POST Method")

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

	return metadata, 200


@app.post("/auth", response_model=AuthResponse)
async def auth(request_data: AuthRequest):
    phoneNo = request_data.phoneNo
    otp = request_data.otp

    with open('otpValidity.json', 'r') as fs:
        otpFile = json.loads(fs.read())

    otpGeneratedTime = datetime.strptime(otpFile.get('time'), '%H:%M')

    nowTime = datetime.now()

    delta = nowTime - otpGeneratedTime
    timeDiff = int(delta.seconds / 60)

    authenticated = False
    validationMsg = ""


    if int(otpFile.get('otp')) != otp:
        validationMsg = "Invalid OTP"
    elif timeDiff > 5:
        validationMsg = "OTP Expired"
    else:
        authenticated = True
        validationMsg = "OTP Validated"

    return {
        "phone_no": phoneNo,
        "authentication": authenticated,
        "validation_msg": validationMsg
    }

port = os.getenv('VCAP_APP_PORT', '80')
if __name__ == "__main__":
    logger.debug("Starting the Application")
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=True)