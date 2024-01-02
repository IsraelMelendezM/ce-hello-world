from fastapi import APIRouter, Query, HTTPException
from datetime import datetime, timedelta
from pydantic import BaseModel
import ibm_db
import json
from database.UserTable import UserTable

router = APIRouter()

class AuthRequest(BaseModel):
    phoneNo: int
    otp: int

class AuthResponse(BaseModel):
    phone_no: int
    authentication: bool
    policy_no: str
    validation_msg: str

def connect_to_db():
    # Replace these values with your actual Db2 connection details
    conn_str = "DATABASE=mydb;HOSTNAME=myhost;PORT=myport;PROTOCOL=TCPIP;UID=myuser;PWD=mypassword;"
    conn = ibm_db.connect(conn_str, '', '')
    return conn

def execute_query(conn, sql):
    stmt = ibm_db.exec_immediate(conn, sql)
    result = []
    while ibm_db.fetch_row(stmt):
        result.append(ibm_db.result(stmt, 0))
    return result

@router.get("/auth", response_model=AuthResponse)
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

    sql = f"SELECT policy_no FROM UserTable WHERE phone_no={phoneNo}"
    
    try:
        conn = connect_to_db()
        response = execute_query(conn, sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        ibm_db.close(conn)

    if int(otpFile.get('otp')) != otp:
        validationMsg = "Invalid OTP"
        returnPolicyNo = response[0] if response else None
    elif timeDiff > 5:
        validationMsg = "OTP Expired"
        returnPolicyNo = response[0] if response else None
    else:
        authenticated = True
        validationMsg = "OTP Validated"
        returnPolicyNo = response[0] if response else None

    return {
        "phone_no": phoneNo,
        "authentication": authenticated,
        "policy_no": returnPolicyNo,
        "validation_msg": validationMsg
    }