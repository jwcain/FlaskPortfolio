coverage run -m pytest
coverage report

read -p "Generate HTML? [y/n]" yn

case $yn in
    y ) echo "Generating";;
    * ) exit;;

esac
coverage html
explorer '.\htmlcov\index.html'
exit