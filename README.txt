Ademas del python manage.py migrate por favor ejecuta,
python manage.py loaddata apps/authenticate/fixtures/groups.json con eso se deberan crear los dos grupos en la base de datos.

Cristian, estos dos comandos en la carpeta del proyecto hace que para ese proyecto cambies los datos de usuario y email

git config --local user.name her_username
git config --local user.email her_email

usa estas 
nombre: Julian
username: juliangarnica98
email: juliang1012@gmail.com
pass: Julian981012

y con esto haces push

git push https://username:password@myrepository.biz/repo.git --all 

Example

git push https://riesgoba:Millos0225@github.com/juliangarnica98/ProyectoIngSof.git --all

Instalar por requirements

pip install -r requirements.txt