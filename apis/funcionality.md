# Main

This is a FastAPI application designed for Watson Assistant functionalities

## Code Description

### Project Structure

- **main.py:** The main script that contains the FastAPI application, API endpoints, and business logic.
- **helpers/:** Directory containing helper modules:
  - `TwilioAdapter.py`: Module for interacting with the Twilio API for sending messages.
  - `OTPGenerator.py`: Module for generating OTPs.
  - `Cloudant.py`: Module for interacting with IBM Cloudant database.
- **dotenv:** Directory containing the `.env` file for environment variable configuration.
- **otpValidity.json:** JSON file to store OTP metadata.

### Dependencies

- **FastAPI:** Web framework for building APIs.
- **Twilio:** Library for interacting with the Twilio API.
- **Pydantic:** Data validation and settings management using Python type hints.
- **Cloudant:** IBM Cloudant library for Python.

### Functionality

- **`root()` (GET /):** Basic endpoint returning a "Hello World" message.

- **`clientData(data)`:** Function to retrieve client details from the Cloudant database based on the distributor ID.

- **`generate_and_send_otp(data)`:** Function to generate and send OTP via Twilio.

- **`auth(data)`:** Function to authenticate the user based on the received OTP.

- **`engine(request_data)` (POST /engine):** Main engine endpoint to handle different cases. It includes cases such as fetching client details, sending OTP, and authentication.
