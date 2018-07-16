import requests
from flask import Flask,render_template,request

url = "https://fortnite-public-api.theapinetwork.com/prod09/users/id"
payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'Authorization': "e8d20d92631995b6d22e5d1ec0b21411"
    }
    
app= Flask (__name__)

@app.route('/',methods=['GET','POST'])
def index():
	player_one = None
	player_one_stats = {}
	errormsg = None
	if request.method =='POST':
		player_one = request.form.get('UserName')
		platform = request.form.get('platform')
		try:
			response = requests.request("POST", url, data=payload.format(player_one), headers=headers)
		except requests.exceptions.RequestException as e:
			print (e)
		if 'error' in response.json() and response.json()['error']:
			player_one=None
			errormsg = response.json()['errorMessage']
		else:
			uid = response.json()['uid']
			print (response.text)
			player_one_stats = getUserData(uid,str(platform))

	return render_template('index.html', player_one = player_one, player_one_stats = player_one_stats, errormsg = errormsg)

def getUserData(userid,platformtype):

	url = "https://fortnite-public-api.theapinetwork.com/prod09/users/public/br_stats"
	payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"user_id\"\r\n\r\n"+userid+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"platform\"\r\n\r\n"+platformtype+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"window\"\r\n\r\nalltime\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
	headers = {
	'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
	'Authorization': "e8d20d92631995b6d22e5d1ec0b21411"
	}
	try:
		res = requests.request("POST", url, data=payload, headers=headers)
	except requests.exceptions.RequestException as e:
		print (e)
		
	if 'error' in res.json() and res.json()['error']:
		print (res.text)
		return {}
	else:
		result = res.json()['totals']
		return result

if __name__ == '__main__':
	app.run(debug=True)
