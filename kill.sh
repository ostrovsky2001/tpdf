while true
        do
        next_save=$(stat -c '%y' table.xlsx)
        pgrep python >text.txt
        x=$(cat text.txt)
        if [ "$first_save" != "$next_save" ]
                then
                first_save=$(stat -c '%y' table.xlsx)
                kill $x
        fi
	sleep 1
done
