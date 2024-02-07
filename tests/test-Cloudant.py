
import sys
sys.path.append('../')
import unittest
import os
from dotenv import load_dotenv
from ibmcloudant.cloudant_v1 import CloudantV1
from cronJob_uploadUniqueClientInfo import save_data_Cloudant,\
                                    delete_all_documents,\
                                        get_unique_clients_latest_data
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from ibmcloudant.cloudant_v1 import CloudantV1
import logging
from dotenv import  load_dotenv

load_dotenv()

credentials = {'CLOUDANT_API_KEY':os.environ.get("CLOUDANT_API_KEY"),
                'CLOUDANT_URL':os.environ.get("CLOUDANT_URL")}
authenticator = IAMAuthenticator(apikey=credentials['CLOUDANT_API_KEY'])
service = CloudantV1(authenticator=authenticator)
service.set_service_url(credentials['CLOUDANT_URL'])

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

class TestSaveDataCloudant(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        credentials = {
            'CLOUDANT_API_KEY': os.environ.get("CLOUDANT_API_KEY"),
            'CLOUDANT_URL': os.environ.get("CLOUDANT_URL")
        }

        cls.authenticator = IAMAuthenticator(apikey=credentials['CLOUDANT_API_KEY'])
        cls.service = CloudantV1(authenticator=cls.authenticator)
        cls.service.set_service_url(credentials['CLOUDANT_URL'])

    def setUp(self):
        self.mock_credit_data1 =  {'status': 1, 'available_footwear': 151034.19, 'available_financial': 57869.8, 'available_credit_line': 119034.19, 'current_loan': 41600, 'current_loan_detail': {'dateStart': '2023-09-21', 'numberPurchase': '21256621', 'amountPurchase': '32000.00', 'interest': '9600.00', 'purchaseAmountTotal': 41600, 'loanTerm': '12', 'numberAmortization': '8', 'numberAmortizationLoanTerm': '8/12', 'due': 17331, 'paymentAmount': 3467, 'dateEnd': '2024-03-20', 'paymentDates': ['2023-10-20', '2023-10-22', '2023-10-22', '2023-11-06', '2023-11-06', '2023-11-07', '2023-11-21', '2023-11-21', '2023-12-06', '2023-12-06', '2023-12-06', '2023-12-20', '2023-12-20', '2023-12-20', '2024-01-05', '2024-01-05', '2024-01-05', '2024-01-21', '2024-01-21']}, 'has_have_loan': 1, 'can_have_loan': 0, 'loan_options': [], 'credit_type': 'Tradicional', 'credit_score_name': '', 'credit_line': 352000, 'credit_status': 3, 'financial_credit_line': 211200, 'toPay': 28973, 'released': 33435.78, 'discount': 4462.78, 'cutoff_date': '2024-01-20', 'payment_date': '2024-02-05', 'distributor': 'SOFIA MENA GUERRERO', 'period': [{'number': 457, 'charged': 33435.78, 'balance': 33435.78, 'discount': 4462.78, 'balanceDiscount': 28973.01, 'payed': 0, 'maxDueDaysForDiscount': 0, 'percentDiscount': 13.35}], 'insurance_folio': '620006', 'distributor_insurance': '216.96', 'insurance_benefits': {'items': [{'name': 'Seguro de vida'}, {'name': 'Servicio funeral directo ¡NUEVO!'}, {'name': 'Seguro contra robo hasta $50,000'}]}, 'free_footwear': 0, 'financial_balance': 0}
        self.mock_credit_data2 =  {'status': 1, 'available_footwear': 132566.08, 'available_financial': 132566.08, 'available_credit_line': -217433.92, 'current_loan': 0, 'current_loan_detail': [], 'has_have_loan': 0, 'can_have_loan': 1, 'loan_options': [{'interest': '20.00', 'id_interest': '67', 'id_branch': '2', 'period': '8', 'period_amount': 222852.8, 'interest_amount': 44570.56, 'loan_amount': 60000}, {'interest': '25.00', 'id_interest': '68', 'id_branch': '2', 'period': '10', 'period_amount': 278566, 'interest_amount': 69641.5, 'loan_amount': 60000}, {'interest': '30.00', 'id_interest': '69', 'id_branch': '2', 'period': '12', 'period_amount': 334279.19999999995, 'interest_amount': 100283.75999999998, 'loan_amount': 60000}], 'credit_type': 'Tradicional', 'credit_score_name': '', 'credit_line': 2100000, 'credit_status': 3, 'financial_credit_line': 1470000, 'toPay': 199708.65, 'released': 235452.67, 'discount': 35744.02, 'cutoff_date': '2024-01-20', 'payment_date': '2024-02-06', 'distributor': "COMERCIAL D'PORTENIS SA DE CV X X", 'period': [{'number': 457, 'charged': 238293.42, 'balance': 235452.67, 'discount': 35744.02, 'balanceDiscount': 199708.66, 'payed': 2840.7499999999995, 'maxDueDaysForDiscount': 0, 'percentDiscount': 15}], 'insurance_folio': '257482', 'distributor_insurance': '300.72', 'insurance_benefits': {'items': [{'name': 'Seguro de vida'}, {'name': 'Seguro contra robo 5%'}, {'name': 'Indemnización beneficiario $200,000'}]}, 'free_footwear': 0, 'financial_balance': 0}
        self.mock_credit_data3 = {'status': 1, 'available_footwear': 753829.13, 'available_financial': 741256.13, 'available_credit_line': 426970.33, 'current_loan': 0, 'current_loan_detail': [], 'has_have_loan': 0, 'can_have_loan': 1, 'loan_options': [{'interest': '20.00', 'id_interest': '67', 'id_branch': '2', 'period': '8', 'period_amount': 123668.032, 'interest_amount': 24733.6064, 'loan_amount': 60000}, {'interest': '25.00', 'id_interest': '68', 'id_branch': '2', 'period': '10', 'period_amount': 154585.04, 'interest_amount': 38646.26, 'loan_amount': 60000}, {'interest': '30.00', 'id_interest': '69', 'id_branch': '2', 'period': '12', 'period_amount': 185502.048, 'interest_amount': 55650.614400000006, 'loan_amount': 60000}], 'credit_type': 'Tradicional', 'credit_score_name': '', 'credit_line': 1961152.8, 'credit_status': 3, 'financial_credit_line': 1372806.96, 'toPay': 107882.8, 'released': 126794.12, 'discount': 18911.32, 'cutoff_date': '2024-01-20', 'payment_date': '2024-02-06', 'distributor': 'PETRA GARCIA PERAZA', 'period': [{'number': 457, 'charged': 126797.78, 'balance': 126794.12, 'discount': 18911.32, 'balanceDiscount': 107882.8, 'payed': 3.6599999999999997, 'maxDueDaysForDiscount': 0, 'percentDiscount': 14.91}], 'insurance_folio': '562330', 'distributor_insurance': '722.32', 'insurance_benefits': {'items': [{'name': 'Seguro de vida'}, {'name': 'Servicio funeral directo ¡NUEVO!'}, {'name': 'Seguro contra robo hasta $50,000'}, {'name': 'Indemnización beneficiario $200,000'}]}, 'free_footwear': 0, 'financial_balance': 0}
        
        self.mock_client_data1 = {'status': 1, 'total': 1, 'distributors': [{'number': '0070055874', 'distributor': 'SOFIA MENA GUERRERO', 'email': 'Test@hotmail.com', 'branch': 'SALTILLO CENTRO', 'city': 0, 'state': 0, 'reference_banorte': '072744030007961396', 'credit_score': '', 'addresses': [{'id_address': '144838', 'street': 'TORRE DE TULIPANES', 'house_number': '153', 'apartment_number': 0, 'zipcode': '25110', 'neighborhood': 'VALLE DE LAS TORRES', 'settlement': 'SALTILLO', 'city': 'SALTILLO', 'state': 'COAHUILA DE ZARAGOZA', 'residence_time': 0, 'current': '1', 'concat': 'TORREDETULIPANES153'}], 'phones': [{'number': '8441256653', 'type': 'Celular'}]}]}
        self.mock_client_data2 = {'status': 1, 'total': 1, 'distributors': [{'number': '0070097933', 'distributor': "COMERCIAL D'PORTENIS SA DE CV X X", 'email': 'prueba@gmail.com', 'branch': 'MAZATLAN CENTRO', 'city': 0, 'state': 0, 'reference_banorte': '072744030006211102', 'credit_score': '', 'addresses': [{'id_address': '5055378', 'street': 'MELCHOR OCAMPO', 'house_number': '1005', 'apartment_number': 0, 'zipcode': '82000', 'neighborhood': 'Centro', 'settlement': 'Mazatlán', 'city': 'Mazatlán', 'state': 'Sinaloa', 'residence_time': '30', 'current': '1', 'concat': 'MELCHOROCAMPO1005'}], 'phones': [{'number': '6699155300', 'type': 'Trabajo'}]}]}
        self.mock_client_data3 = {'status': 1, 'total': 1, 'distributors': [{'number': '0070000599', 'distributor': 'PETRA GARCIA PERAZA', 'email': 'Test@hotmail.com', 'branch': 'MAZATLAN CENTRO', 'city': 0, 'state': 0, 'reference_banorte': '072744030006203000', 'credit_score': '', 'addresses': [{'id_address': '1748381', 'street': 'C. PRIVADA DUMBO', 'house_number': 'S/N', 'apartment_number': '7', 'zipcode': '82030', 'neighborhood': 'MONTUOSA', 'settlement': 'MAZATLÁN', 'city': 'MAZATLÁN', 'state': 'SINALOA', 'residence_time': 0, 'current': '1', 'concat': 'C.PRIVADADUMBOS/N'}], 'phones': [{'number': '6691228249', 'type': 'Celular'}]}]}
                
    def test_save_data_cloudant_production_scenario1(self):
        save_data_Cloudant( 
                            [self.mock_client_data1],
            [self.mock_credit_data1],
                              prod=False)
        
    def test_save_data_cloudant_production_scenario2(self):
        save_data_Cloudant( 
                            [self.mock_client_data2],
            [self.mock_credit_data2],
                              prod=False)
        
    def test_save_data_cloudant_production_scenario3(self):
        save_data_Cloudant( 
                            [self.mock_client_data3],
            [self.mock_credit_data3],
                              prod=False)
        
    def test_update_data_cloudant_production(self):
        delete_all_documents(False)
        get_unique_clients_latest_data(False)

    def test_update_data_cloudant_production_FULL(self):
        
        client_APIdata = [self.mock_client_data1, self.mock_client_data2, self.mock_client_data3]  
        credit_APIdata = [self.mock_credit_data1, self.mock_credit_data2, self.mock_credit_data3]           

        save_data_Cloudant(client_APIdata,
                            credit_APIdata, prod=False)
        delete_all_documents(False)
        get_unique_clients_latest_data(False)
        
if __name__ == '__main__':
    unittest.main()
