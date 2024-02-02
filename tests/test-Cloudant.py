
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

    def test_save_data_cloudant_production_scenario1(self):
        mock_client_data = {'status': 1, 'total': 1, 'distributors': [{'number': '0070000599', 'distributor': 'PETRA GARCIA PERAZA', 'email': 'Test@hotmail.com', 'branch': 'MAZATLAN CENTRO', 'city': 0, 'state': 0, 'reference_banorte': '072744030006203000', 'credit_score': '', 'addresses': [{'id_address': '1748381', 'street': 'C. PRIVADA DUMBO', 'house_number': 'S/N', 'apartment_number': '7', 'zipcode': '82030', 'neighborhood': 'MONTUOSA', 'settlement': 'MAZATLÁN', 'city': 'MAZATLÁN', 'state': 'SINALOA', 'residence_time': 0, 'current': '1', 'concat': 'C.PRIVADADUMBOS/N'}], 'phones': [{'number': '6691228249', 'type': 'Celular'}]}]}
        mock_credit_data = {'status': 1, 'available_footwear': 753829.13, 'available_financial': 741256.13, 'available_credit_line': 426970.33, 'current_loan': 0, 'current_loan_detail': [], 'has_have_loan': 0, 'can_have_loan': 1, 'loan_options': [{'interest': '20.00', 'id_interest': '67', 'id_branch': '2', 'period': '8', 'period_amount': 123668.032, 'interest_amount': 24733.6064, 'loan_amount': 60000}, {'interest': '25.00', 'id_interest': '68', 'id_branch': '2', 'period': '10', 'period_amount': 154585.04, 'interest_amount': 38646.26, 'loan_amount': 60000}, {'interest': '30.00', 'id_interest': '69', 'id_branch': '2', 'period': '12', 'period_amount': 185502.048, 'interest_amount': 55650.614400000006, 'loan_amount': 60000}], 'credit_type': 'Tradicional', 'credit_score_name': '', 'credit_line': 1961152.8, 'credit_status': 3, 'financial_credit_line': 1372806.96, 'toPay': 107882.8, 'released': 126794.12, 'discount': 18911.32, 'cutoff_date': '2024-01-20', 'payment_date': '2024-02-06', 'distributor': 'PETRA GARCIA PERAZA', 'period': [{'number': 457, 'charged': 126797.78, 'balance': 126794.12, 'discount': 18911.32, 'balanceDiscount': 107882.8, 'payed': 3.6599999999999997, 'maxDueDaysForDiscount': 0, 'percentDiscount': 14.91}], 'insurance_folio': '562330', 'distributor_insurance': '722.32', 'insurance_benefits': {'items': [{'name': 'Seguro de vida'}, {'name': 'Servicio funeral directo ¡NUEVO!'}, {'name': 'Seguro contra robo hasta $50,000'}, {'name': 'Indemnización beneficiario $200,000'}]}, 'free_footwear': 0, 'financial_balance': 0}

        save_data_Cloudant("test.csv", [mock_client_data],
                            [mock_credit_data], prod=False)
    def test_save_data_cloudant_production_scenario2(self):
        mock_client_data = {'status': 1, 'total': 1, 'distributors': [{'number': '0070097933', 'distributor': 'PETRA GARCIA PERAZA', 'email': 'Test@hotmail.com', 'branch': 'MAZATLAN CENTRO', 'city': 0, 'state': 0, 'reference_banorte': '072744030006203000', 'credit_score': '', 'addresses': [{'id_address': '1748381', 'street': 'C. PRIVADA DUMBO', 'house_number': 'S/N', 'apartment_number': '7', 'zipcode': '82030', 'neighborhood': 'MONTUOSA', 'settlement': 'MAZATLÁN', 'city': 'MAZATLÁN', 'state': 'SINALOA', 'residence_time': 0, 'current': '1', 'concat': 'C.PRIVADADUMBOS/N'}], 'phones': [{'number': '6691228249', 'type': 'Celular'}]}]}
        mock_credit_data = {'status': 1, 'available_footwear': 753829.13, 'available_financial': 741256.13, 'available_credit_line': 426970.33, 'current_loan': 0, 'current_loan_detail': [], 'has_have_loan': 0, 'can_have_loan': 1, 'loan_options': [{'interest': '20.00', 'id_interest': '67', 'id_branch': '2', 'period': '8', 'period_amount': 123668.032, 'interest_amount': 24733.6064, 'loan_amount': 60000}, {'interest': '25.00', 'id_interest': '68', 'id_branch': '2', 'period': '10', 'period_amount': 154585.04, 'interest_amount': 38646.26, 'loan_amount': 60000}, {'interest': '30.00', 'id_interest': '69', 'id_branch': '2', 'period': '12', 'period_amount': 185502.048, 'interest_amount': 55650.614400000006, 'loan_amount': 60000}], 'credit_type': 'Tradicional', 'credit_score_name': '', 'credit_line': 1961152.8, 'credit_status': 3, 'financial_credit_line': 1372806.96, 'toPay': 107882.8, 'released': 126794.12, 'discount': 18911.32, 'cutoff_date': '2024-01-20', 'payment_date': '2024-02-06', 'distributor': 'PETRA GARCIA PERAZA', 'period': [{'number': 457, 'charged': 126797.78, 'balance': 126794.12, 'discount': 18911.32, 'balanceDiscount': 107882.8, 'payed': 3.6599999999999997, 'maxDueDaysForDiscount': 0, 'percentDiscount': 14.91}], 'insurance_folio': '562330', 'distributor_insurance': '722.32', 'insurance_benefits': {'items': [{'name': 'Seguro de vida'}, {'name': 'Servicio funeral directo ¡NUEVO!'}, {'name': 'Seguro contra robo hasta $50,000'}, {'name': 'Indemnización beneficiario $200,000'}]}, 'free_footwear': 0, 'financial_balance': 0}

        save_data_Cloudant("test.csv", [mock_client_data],
                            [mock_credit_data], prod=False)
    def test_save_data_cloudant_production_scenario3(self):
        mock_client_data = {'status': 1, 'total': 1, 'distributors': [{'number': '0070000599', 'distributor': 'PETRA GARCIA PERAZA', 'email': 'Test@hotmail.com', 'branch': 'MAZATLAN CENTRO', 'city': 0, 'state': 0, 'reference_banorte': '072744030006203000', 'credit_score': '', 'addresses': [{'id_address': '1748381', 'street': 'C. PRIVADA DUMBO', 'house_number': 'S/N', 'apartment_number': '7', 'zipcode': '82030', 'neighborhood': 'MONTUOSA', 'settlement': 'MAZATLÁN', 'city': 'MAZATLÁN', 'state': 'SINALOA', 'residence_time': 0, 'current': '1', 'concat': 'C.PRIVADADUMBOS/N'}], 'phones': [{'number': '6691228249', 'type': 'Celular'}]}]}
        mock_credit_data = {'status': 1, 'available_footwear': 753829.13, 'available_financial': 741256.13, 'available_credit_line': 426970.33, 'current_loan': 0, 'current_loan_detail': [], 'has_have_loan': 0, 'can_have_loan': 1, 'loan_options': [{'interest': '20.00', 'id_interest': '67', 'id_branch': '2', 'period': '8', 'period_amount': 123668.032, 'interest_amount': 24733.6064, 'loan_amount': 60000}, {'interest': '25.00', 'id_interest': '68', 'id_branch': '2', 'period': '10', 'period_amount': 154585.04, 'interest_amount': 38646.26, 'loan_amount': 60000}, {'interest': '30.00', 'id_interest': '69', 'id_branch': '2', 'period': '12', 'period_amount': 185502.048, 'interest_amount': 55650.614400000006, 'loan_amount': 60000}], 'credit_type': 'Tradicional', 'credit_score_name': '', 'credit_line': 1961152.8, 'credit_status': 3, 'financial_credit_line': 1372806.96, 'toPay': 107882.8, 'released': 126794.12, 'discount': 18911.32, 'cutoff_date': '2024-01-20', 'payment_date': '2024-02-06', 'distributor': 'PETRA GARCIA PERAZA', 'period': [{'number': 457, 'charged': 126797.78, 'balance': 126794.12, 'discount': 18911.32, 'balanceDiscount': 107882.8, 'payed': 3.6599999999999997, 'maxDueDaysForDiscount': 0, 'percentDiscount': 14.91}], 'insurance_folio': '562330', 'distributor_insurance': '722.32', 'insurance_benefits': {'items': [{'name': 'Seguro de vida'}, {'name': 'Servicio funeral directo ¡NUEVO!'}, {'name': 'Seguro contra robo hasta $50,000'}, {'name': 'Indemnización beneficiario $200,000'}]}, 'free_footwear': 0, 'financial_balance': 0}

        save_data_Cloudant("test.csv", [mock_client_data],
                            [mock_credit_data], prod=False)
        
    def test_update_data_cloudant_production(self):
        delete_all_documents(False)
        get_unique_clients_latest_data(False)

if __name__ == '__main__':
    unittest.main()
