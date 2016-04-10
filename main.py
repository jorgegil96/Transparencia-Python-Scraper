from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import http.client
import urllib.parse
from urllib.error import HTTPError
import csv

cuentaTotal = 0
registros = []
errores = []

def formURL(sec, dep):
	return "http://sgi.nl.gob.mx/Nomina_2015/BusquedaPorDependencia.aspx?SecretariaId=" + sec + "&DependenciaId=" + dep + "&EntidadId=1004&ConceptoId=301&Anio=2016&MesId=1"

def getNomina(URL, sec):
	page = urlopen(URL)
	soup = BeautifulSoup(page, "html.parser")
	depName = soup.find(id='lblDependencia').string
	print (depName)

	nomina = []
	failed = False

	for tr in soup.find_all("tr", class_='DataGrid_Item'):
		nomina.append([tr.td.string, tr.td.next_sibling.string, tr.td.next_sibling.next_sibling.string])
	for tr in soup.find_all("tr", class_='DataGrid_AlternatingItem'):
		nomina.append([tr.td.string, tr.td.next_sibling.string, tr.td.next_sibling.next_sibling.string])

	paginas = len(soup.find(id='ddlPagina').find_all('option'))

	#print("Paginas: " + str(paginas))

	for i in range(0, paginas - 1):

		eventvalidation = soup.find_all(id='__EVENTVALIDATION')[0]['value']
		viewstate = soup.find_all(id='__VIEWSTATE')[0]['value']

		params = {	
			'__EVENTTAGET' : 'lnkSiguiente',
			'__EVENTARGUMENT' : '',
			'__LASTFOCUS' : '',
			'__VIEWSTATE' : viewstate,
			'__EVENTVALIDATION' : eventvalidation,
			'ddlAnio' : '2016',
			'ddlMes' : '1',
			'ddlPagina' : i + 1
		}

		headers = {
			'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
			'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
			'Content-Type': 'application/x-www-form-urlencoded'
		}

		uri = "http://sgi.nl.gob.mx/Nomina_2015/BusquedaPorDependencia.aspx?"

		encodedParams = urllib.parse.urlencode(params)
		encodedParams = encodedParams.encode('utf-8')
		req = Request(uri, encodedParams, headers)
		try:
			f = urlopen(req)
			soup = BeautifulSoup(f, "html.parser")
			for tr in soup.find_all("tr", class_='DataGrid_Item'):
				nomina.append([tr.td.string, tr.td.next_sibling.string, tr.td.next_sibling.next_sibling.string])
			for tr in soup.find_all("tr", class_='DataGrid_AlternatingItem'):
				nomina.append([tr.td.string, tr.td.next_sibling.string, tr.td.next_sibling.next_sibling.string])
		except HTTPError as e:
			failed = True
			content = e.read()
			errores.append([sec, depName, i])
			print("HTTP ERROR")
			#print("HTTP ERROR: ", content)
	if failed:
		print("FAILED")
		return []
	else:
		return nomina


# Dependencias Centrales y Tribunales Administrativos
# -------------------------------------------------------------------
secIDs = ['16', '15', '11', '1', '12', '2', '5', '9', '18', '17', '7', '6', '10', '8', '4', '19', '3', '13', '14']
for sec in secIDs:
	#print("+++++SECRETARIA ID: " + sec + " +++++")
	page = urlopen('http://sgi.nl.gob.mx/Nomina_2015/BusquedaPorDependencia.aspx?SecretariaId=' + sec + '&EntidadId=1004&ConceptoId=301&Anio=2016&MesId=1')
	soup = BeautifulSoup(page, "html.parser")

	depURLs = []
	for td in soup.find_all(id='dgPorDependencia')[0].find_all(align='center'):
		depURLs.append("http://sgi.nl.gob.mx/Nomina_2015/" + td.a['href'])

	for dep in depURLs:
		nomina = getNomina(dep, sec)
		registros.extend(nomina)
		#for persona in nomina:
		#	print(persona)
		#print("--------------------------")
# -------------------------------------------------------------------




# Unidades Administrativas
# -------------------------------------------------------------------
secID = '2'
depUA = ['710', '730', '740', '760', '9290']
for d in depUA:
	URL = "http://sgi.nl.gob.mx/Nomina_2015/BusquedaPorDependencia.aspx?SecretariaId=" + secID + "&DependenciaId=" + d + "&EntidadId=1004&ConceptoId=301&Anio=2016&MesId=1"
	registros.extend(getNomina(URL, secID))
# -------------------------------------------------------------------




# Org Descentralizados de participación ciudadana
# -------------------------------------------------------------------
# Registros directos, secID y depID 1a1
secIDs = ['20', '21', '24', '25']
depIDs = ['2440', '2370', '2860', '3090']
for i in range(0, 4):
	URL = "http://sgi.nl.gob.mx/Nomina_2015/BusquedaPorDependencia.aspx?SecretariaId=" + secIDs[i] + "&DependenciaId=" + depIDs[i] + "&EntidadId=1004&ConceptoId=301&Anio=2016&MesId=1"
	registros.extend(getNomina(URL, secIDs[i]))
# Indirecto 1
secID = '23'
depID = '9520'
URL = formURL(secID, depID)
registros.extend(getNomina(URL, secID))
# Indirecto 2
secID = '22'
depIDs = ['8730', '8750', '8740', '9720', '970', '8240', '8720']
for d in depIDs:
	URL = formURL(secID, d)
	registros.extend(getNomina(URL, secID))
# -------------------------------------------------------------------




# Org Descentralizados
# -------------------------------------------------------------------
# Directos (443)
secIDs = ['26', '27', '28']
depIDs = ['800', '860', '3070']
for i in range(0, 3):
	URL = formURL(secIDs[i], depIDs[i])
	registros.extend(getNomina(URL, secIDs[i]))
# Indirecto 1 (282)
secID = '29'
depIDs = ['2390', '1610']
for d in depIDs:
	URL = formURL(secID, d)
	registros.extend(getNomina(URL, secID))
# Indirecto 2
secID = '30'
depIDs = ['3290', '3310', '3280', '3260', '3320']
for d in depIDs:
	URL = formURL(secID, d)
	registros.extend(getNomina(URL, secID))
# -------------------------------------------------------------------



for r in registros:
	print(r)

print ("# Registros: " + str(len(registros)))
print ("# Errores: " + str(len(errores)))
for e in errores:
	print(e)

fl = open('nominamensual6.csv', 'w')
writer = csv.writer(fl)
writer.writerow(['Nombre', 'Puesto', 'Sueldo Mensual'])
for r in registros:
	writer.writerow(r)

fl.close()

