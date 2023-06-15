update:
	@echo "\033[1;36m-\033[0m \033[0;32mrestart gunicorn\033[0m"
	sudo systemctl restart gunicorn
	@echo "\033[1;36m-\033[0m \033[0;32mdaemon-reload\033[0m"
	sudo systemctl daemon-reload
	@echo "\033[1;36m-\033[0m \033[0;32mgunicorn socket and service restart\033[0m"
	sudo systemctl restart gunicorn.socket gunicorn.service
	@echo "\033[1;36m-\033[0m \033[0;32mrestart nginx\033[0m"
	sudo nginx -t && sudo systemctl restart nginx

pull:
	@echo "\033[1;36m-\033[0m \033[0;32mpull changes\033[0m"
	git checkout deploy
	git pull gitflic deploy

requirements:
	@echo "\033[1;36m-\033[0m \033[0;32mupload requirements\033[0m"
	./env/bin/pip install -r requirements.txt

migrate:
	@echo "\033[1;36m-\033[0m \033[0;32mmigrate\033[0m"
	./env/bin/python3 manage.py makemigrations
	./env/bin/python3 manage.py migrate

initgroups:
	@echo "\033[1;36m-\033[0m \033[0;32mupdate groups permissions\033[0m"
	./env/bin/python3 manage.py initgroups

pull_update: pull update

pull_groups_update: pull initgroups update

full_update: pull requirements migrate initgroups update

help:
	@echo "Makefile is a tool to simplify or to organize code for compilation.\n"
	
	@echo "Usage:\n\
	\t make <command>\n"

	@echo "The commands are:\n\n\
	\t\033[1;36mupdate\033[0m           	- to restart gunicorn and nginx\n\
	\t\033[1;36mpull\033[0m             	- pull commits\n\
	\t\033[1;36mrequirements\033[0m     	- upload requirements\n\
	\t\033[1;36minitgroups\033[0m     		- update groups permissions\n\
	\t\033[1;36mpull_update\033[0m      	- for both pull and update\n\
	\t\033[1;36mmigrate\033[0m          	- make makemigrations and migrate\n\
	\t\033[1;36mpull_groups_update\033[0m   - git pull, initgroups, restart server\n\
	\t\033[1;36mfull_update\033[0m      	- git pull, upload requirements and initgroups, restart server\n"