name=$1

if [ -z $name ]; then
	echo -e "\nUsage:"
	echo -e "  step5_sob.sh [name | email_address]\n"
	exit
fi
cat backport/*.patch | grep Signed-off-by | grep $name
