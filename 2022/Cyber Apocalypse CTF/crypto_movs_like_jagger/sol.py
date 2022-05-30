from ecdsa import ellipticcurve as ecc
import requests
import json

a = -35
b = 98
p = 434252269029337012720086440207
Gx = 16378704336066569231287640165
Gy = 377857010369614774097663166640
ec_order = 434252269029337012720086440208
order_factor = 2**4 * 3 * 73 * 88591 * 3882601 * 360301137196997

E = ecc.CurveFp(p, a, b)
G = ecc.Point(E, Gx, Gy, ec_order)

#url = 'http://138.68.175.87:31488'
url = 'http://138.68.150.120:30625'
response = requests.get(url+'/api/coordinates')

coordinates = json.loads(response.text)

print(json.dumps(coordinates))

q_x = int(coordinates['departed_x'],16)
q_y = int(coordinates['departed_y'],16)
p_x = int(coordinates['present_x'],16)
p_y = int(coordinates['present_y'],16)
Q = ecc.Point(E, q_x, q_y)
P = ecc.Point(E, p_x, p_y)

pr = 1760565499543992808 

D = pr*P

payload = {
    "destination_x":hex(D.x()),
    "destination_y":hex(D.y())
}

print(json.dumps(payload))

response = requests.post(url+'/api/get_flag', json=payload)
print(f"[{response.status_code}]: {response.text}")


D = pr*Q
payload = {
    "destination_x":hex(D.x()),
    "destination_y":hex(D.y())
}
response = requests.post(url+'/api/get_flag', json=payload)
print(f"[{response.status_code}]: {response.text}")

#HTB{I7_5h0075_,1t_m0v5,_wh47_15_i7?}
