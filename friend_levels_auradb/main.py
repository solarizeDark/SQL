import requests
from neo4j_client import Client

vk_friends_list_url = 'https://api.vk.com/method/friends.get?v=5.131&order=hints&fields=bdate&access_token={}&user_id={}'
vk_token = ''
zero_patient_id = 5

neo4j_uri = 'neo4j+s://6e543956.databases.neo4j.io'
neo4j_user = 'neo4j'
neo4j_pass = ''
neo4j_client = Client(neo4j_uri, neo4j_user, neo4j_pass)

zero_patient = {
	'id': zero_patient_id,
	'first_name': 'Egor',
	'last_name': 'Fedusiv',
	'bdate': '11.4.2001',
	'label': 'PATIENT_ZERO'
}

json_response = requests.get(
	vk_friends_list_url.format(vk_token, zero_patient_id)
).json()

first_level = {}
for person in json_response['response']['items']:
	if not 'bdate' in person.keys():
		person['bdate'] = ''
	person['label'] = 'LEVEL_1'
	neo4j_client.create_friendship(zero_patient, person)
	first_level[person['id']] = person

for key in first_level.keys():
	json_response = requests.get(
		vk_friends_list_url.format(vk_token, key)
	).json()

	cnt = 0
	for level2hand in json_response['response']['items']:
		if cnt > 35:
			break
		if not 'bdate' in level2hand.keys():
			level2hand['bdate'] = ''
		cnt += 1
		level2hand['label'] = 'LEVEL_2'
		neo4j_client.create_friendship(first_level[key], level2hand)