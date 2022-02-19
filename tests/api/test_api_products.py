import pytest
import json

@pytest.mark.asyncio
class TestApiProducts:

    API_URL: str = '/latest/products'

    async def test_get_all_products(self, client, test_db) -> None:
        response = client.get(self.API_URL)
        assert response.status_code == 200
        assert response.json() == []
    
    async def test_get_all_products_with_query_string(self, client, test_db):
        products_data = [
            {
                'name': 'Item1',
                'description': 'Description 1'
            },
            {
                'name': 'Item2',
                'description': 'Description 2'
            },
        ]
        for product_data in products_data:
            response = client.post(self.API_URL, data=json.dumps(product_data))
            assert response.status_code == 201, 'Product should be created.'

        response = client.get(self.API_URL + '?query_string=Item1')
        assert response.status_code == 200, 'Product should be found.'
        assert len(response.json()) == 1, 'Should be ONE product'
        assert response.json()[0].get('name') == products_data[0].get('name'), 'The name should be the query_string value.'

    async def test_get_all_products_with_query_string_empty_result(self, client, test_db) -> None:
        products_data = [
            {
                'name': 'Item1',
                'description': 'Description 1'
            },
            {
                'name': 'Item2',
                'description': 'Description 2'
            },
        ]
        for product_data in products_data:
            response = client.post(self.API_URL, data=json.dumps(product_data))
            assert response.status_code == 201, 'Product should be created.'

        response = client.get(self.API_URL + '?query_string=Item4')
        assert response.status_code == 200, 'Product should be found.'
        assert len(response.json()) == 0, 'Should be ZERO products'
        assert response.json() == [], 'Should be an EMPTY list.'

    async def test_get_product(self, client, test_db) -> None:
        expected_product_data = {
            'id': 1,
            'name': 'Item1',
            'description': 'Description 1'
        }
        product_data = {
            'name': 'Item1',
            'description': 'Description 1'
        }

        response = client.post(self.API_URL, data=json.dumps(product_data))
        assert response.status_code == 201, 'Product should be created.'

        response = client.get(self.API_URL + '/1')
        assert response.status_code == 200, 'Should be found.'
        assert response.json() == expected_product_data
    
    async def test_get_product_not_found(self, client, test_db) -> None:
        response = client.get(self.API_URL + '/1')
        assert response.status_code == 404, 'Should not be found.'

    async def test_post_product(self, client, test_db) -> None:
        expected_product_data = {
            'id': 1,
            'name': 'Item1',
            'description': 'Description 1'
        }
        product_data = {
            'name': 'Item1',
            'description': 'Description 1'
        }

        response = client.post(self.API_URL, data=json.dumps(product_data))
        assert response.status_code == 201
        assert response.json() == expected_product_data
    
    async def test_patch_product(self, client, test_db) -> None:
        new_product_data = {
            'name': 'Item 1 EDITED',
            'description': 'Description 1'
        }
        product_data = {
            'name': 'Item1',
            'description': 'Description 1'
        }

        response = client.post(self.API_URL, data=json.dumps(product_data))
        assert response.status_code == 201, 'Should be created.'
        product_id = response.json().get('id')
        new_product_data['id'] = product_id

        response = client.patch(self.API_URL + '/' + str(product_id), data=json.dumps(new_product_data))
        assert response.status_code == 200, 'Should be updated.'
        assert response.json() == new_product_data
    

    async def test_patch_product_not_found(self, client, test_db) -> None:
        new_product_data = {
            'id': 2,
            'name': 'Item 1 EDITED',
            'description': 'Description 1'
        }
        product_data = {
            'name': 'Item1',
            'description': 'Description 1'
        }

        response = client.post(self.API_URL, data=json.dumps(product_data))
        assert response.status_code == 201, 'Should be created.'
        product_id = new_product_data.get('id')

        response = client.patch(self.API_URL + '/' + str(product_id), data=json.dumps(new_product_data))
        assert response.status_code == 404, 'Should not be found.'
        assert response.json() == {'detail': 'Product not found'}
    
    async def test_delete_product(self, client, test_db) -> None:
        product_data = {
            'name': 'Item1',
            'description': 'Description 1'
        }
        response = client.post(self.API_URL, data=json.dumps(product_data))
        assert response.status_code == 201, 'Should be created.'
        product_id = response.json().get('id')

        response = client.delete(self.API_URL + '/'+ str(product_id))
        assert response.status_code == 200, 'Should be deleted.'
        response = client.get(self.API_URL + '/' + str(product_id))
        assert response.status_code == 404, 'Should not be found.'
    
    async def test_delete_product_not_found(self, client, test_db) -> None:
        response = client.delete(self.API_URL + '/1')
        assert response.status_code == 404, 'Should not be found.'
        
        

    