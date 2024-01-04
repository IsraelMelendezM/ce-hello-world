import logging as logger
import os
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pprint import pprint 
from pydantic import BaseModel

from typing import Optional
import requests 
from dotenv import load_dotenv
from helpers.TwilioAdapter import MessageClient
from helpers.OTPGenerator import Generate
from helpers.Cloudant import GetClientDetails
from helpers.Cloudant import sp_time, as_spanish, offset_days

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
    validation_msg: str 

# class EngineRequest(BaseModel):
#     arg1: str
#     arg2: str
#     case: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/get_client_details_with_id")
def clientData(id: str):
    ## Obtener datos importantes con el ID de distribuidor
    try:
        service = GetClientDetails()
    except Exception as err:
        return(err)
    logger.debug("DISTRIBUTOR ID",  id)

    doc = service.get_doc_by_key(dbName='test-distribuidores',
                            ddoc='clientes',
                            key=id,
                            view='daily_record')
    if doc is None:
         raise HTTPException(status_code=404, 
                             detail="Distributor ID not found in Database")

    logger.debug(doc)
    pay_by_date_dt = datetime.strptime(doc['should_pay_by'], '%Y-%m-%d')

    cst = sp_time(pay_by_date_dt, 0, 'cst')
    
    # print(doc)
    benefits_str = ', '.join([item['name'] for item in doc['benefits']['items'] ])
    

    with open('clientData.json', 'w') as fs:
        json.dump(doc, fs, indent=2)

    return {'record': doc,
        'benefits': benefits_str,
        'hubo_respuesta': 1,
        'first_name':doc['name'].split(' ')[0],
        'should_pay_by_date_sp': as_spanish(cst),
        'should_pay_by_date_minus_4_sp': as_spanish(offset_days(cst,-3)),
    }


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
def auth(request_data: AuthRequest):
    
    phoneNo = request_data.phoneNo
    otp = request_data.otp

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
    
    return {
        "phone_no": phoneNo,
        "authentication": authenticated,
        "validation_msg": validationMsg
    }

@app.post("/engine")
async def auth(case:str, id: Optional[str] = None,
               phoneNo: Optional[str] = None,
               otp: Optional[str]= None):
    
    load_dotenv()
    host = os.environ.get("HOST")

    if case == "get_client_details_with_id":
        # host = "169.62.228.229:8000"
        ext = ":8000"
        url =  f"http://{host}{ext}/get_client_details_with_id/?={id}"
        try:
            inp_post_response = requests.post(url , 
                                              json={"id":id})
            if inp_post_response .status_code == 200:
                return inp_post_response, 200
            
        except Exception as e:
             return {"error": str(e)}
        
    elif case == "send_otp":    
        ext = ":8000"
        url =  f"http://{host}{ext}/generate_and_send_otp/?={phoneNo}"
        try:
            inp_post_response = requests.post(url , 
                                              json={"phoneNo":phoneNo})
            if inp_post_response .status_code == 200:
                return inp_post_response, 200
            
        except Exception as e:
             return {"error": str(e)}
        
    elif case == "auth":
        ext = ":8000"
        url =  f"http://{host}{ext}/auth/?={phoneNo}&?={otp}"
        try:
            inp_post_response = requests.post(url ,
                                               json={"phoneNo":phoneNo,
                                                     "otp": otp})
            if inp_post_response .status_code == 200:
                return inp_post_response, 200
            
        except Exception as e:
             return {"error": str(e)}
                 
    else:
         return {"error": "No cases ran."}
    

port = os.getenv('VCAP_APP_PORT', '8080')
if __name__ == "__main__":
    logger.debug("Starting the Application")
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=True)