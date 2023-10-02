import unittest
from unittest.mock import patch
from lambda_function import lambda_handler, insert_table

class TestLambdaHandler(unittest.TestCase):

    @patch('lambda_function.requests.get')
    @patch('lambda_function.insert_table')
    def test_lambda_handler(self, mock_insert_table, mock_requests_get):
        # Configurar el comportamiento del mock de requests.get
        mock_requests_get.return_value.json.return_value = {
            'data': {
                'BTC': {
                    'quote': {
                        'USD': {
                            'price': 50000
                        }
                    }
                },
                'ETH': {
                    'quote': {
                        'USD': {
                            'price': 2000
                        }
                    }
                }
            }
        }

        # Ejecutar la función lambda_handler
        response = lambda_handler({}, {})
        data = response['body']

        # Verificar que los precios BTC y ETH sean los esperados
        self.assertEqual(data['BTC_price'], 50000)
        self.assertEqual(data['ETH_price'], 2000)

        # Verificar que la función insert_table fue llamada con los precios correctos
        mock_insert_table.assert_called_once_with(50000, 2000)

    def test_insert_table(self):
        # Configurar el contexto para las pruebas
        with patch('lambda_function.conn') as mock_conn:
            mock_cursor = mock_conn.cursor.return_value
            # Llamar a la función insert_table con valores de prueba
            insert_table(50000, 2000)

            # Verificar que se llamó a execute con la consulta SQL esperada y los valores esperados
            mock_cursor.execute.return_value(
                "INSERT INTO price_table (BTC, ETH) VALUES (%s, %s)",
                (50000, 2000)
            )

if __name__ == '__main__':
    unittest.main()
