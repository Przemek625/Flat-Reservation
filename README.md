# Git global setup

    git config --global user.name "Przemek"
git config --global user.email "przemyslaw.spychalski@profil-software.com"
 
Create a new repository

git clone git@git.profil-software.com:przemek.spychalski/Flats-reservation.git
cd Flats-reservation
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master

Existing folder or Git repository

cd existing_folder
git init
git remote add origin git@git.profil-software.com:przemek.spychalski/Flats-reservation.git
git add .
git commit
git push -u origin master