import requests


HOST = 'http://127.0.0.1:5000'

response = requests.post(f'{HOST}/users/', json={'name2': 'user_1', 'password': '1234'})
print(response.status_code)
print(response.text)


# response = requests.get(f'{HOST}/users/1')
# print(response.status_code)
# print(response.text)
#
# response = requests.patch(f'{HOST}/users/1', json={'name': 'user_1_v3'})
# print(response.status_code)
# print(response.text)
#
# response = requests.get(f'{HOST}/users/1')
# print(response.status_code)
# print(response.text)
#
# response = requests.delete(f'{HOST}/users/1')
# print(response.status_code)
# print(response.text)
