from libs.bottle import route, static_file, run

@route('/installations/<numero>')
def installation(numero):
    return {'numero': numero, 'nom' : 'installation ' + numero}

@route('/installations')
def installations():
	return { 'installations' : [
    	{'numero': '1', 'nom' : 'installation 1'},
    	{'numero': '2', 'nom' : 'installation 2'},
    	{'numero': '3', 'nom' : 'installation 3'}
    ]}

@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

run(host='localhost', port=8080)