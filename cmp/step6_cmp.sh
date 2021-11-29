for patch in `ls backport`
do
	diff=$(diff upstream/$patch backport/$patch | grep -e changed -e "< -" -e "< +" -e "> -" -e "> +")
	if [[ $diff ]]; then
		echo $patch
		echo $diff
		echo -e "\n"
	fi
done

