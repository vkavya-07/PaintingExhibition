import httpx
import datetime

client = httpx.Client()

r = client.post('http://127.0.0.1:8001/paintings/', json={'createdBy':'TestAdmin','size':'10x10','isAvailableForSale':True,'price':50.0}, headers={'x-role':'admin'})
print('POST', r.status_code, r.text)

r = client.get('http://127.0.0.1:8001/paintings/', headers={'x-role':'user'})
print('GET', r.status_code, r.text)

data = r.json()
if data:
    pid = data[0]['id']
    soldDate = datetime.datetime.now(datetime.timezone.utc).isoformat()
    r = client.patch(f'http://127.0.0.1:8001/paintings/{pid}/buy', json={'soldTo':'Buyer','soldDate':soldDate}, headers={'x-role':'user'})
    print('BUY', r.status_code, r.text)

    r = client.get('http://127.0.0.1:8001/paintings/sold', headers={'x-role':'admin'})
    print('SOLD', r.status_code, r.text)
else:
    print('No paintings returned in GET')
