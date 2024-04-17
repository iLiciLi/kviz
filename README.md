KOMANDE ZA POKRETANJE FRONTEND DELA :<br />
---
cd frontend<br />
npm install<br />
npm run dev<br />

KOMANDE ZA POKRETANJE BACKEND DELA :
---
cd backend<br />
<br />
**{Ako nemate virtualenv i flask instaliran, onda nakon cd backend uradite sledece} : <br />**
pip install flask<br />
pip install virtualenv<br />
python -m virtualenv env<br />
Set-ExecutionPolicy Unrestricted -Scope Process<br />
.\env\Scripts\activate<br />
**~unutar (env) kucate komandu :<br />**
flask --app flaskr run --debug<br />
<br />
**{Ako imate virtualenv i flask, onda} :<br />**
python -m virtualenv env<br />
Set-ExecutionPolicy Unrestricted -Scope Process<br />
.\env\Scripts\activate<br />
**~unutar (env) kucate komandu :<br />**
flask --app flaskr run --debug<br />
