MYSQL=mysql
MYSQL_USER=dfs
MYSQL_PASS=dfspass
MYSQL_DB=dfs
DOMAIN=demo

all: domain

db:
	@$(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)

domain:
	@echo "adding domain $(DOMAIN)"
	@echo "INSERT IGNORE INTO domains(name, folder, url) VALUE('$(DOMAIN)', '$(DOMAIN)', '')" | $(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)
	@echo "INSERT IGNORE INTO servers_domains(server_id, domain_id) SELECT servers.id, domains.id from servers, domains WHERE domains.name = '$(DOMAIN)'" | $(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)

clean:
	@echo "cleaning database"
	@echo "SET FOREIGN_KEY_CHECKS = 0; TRUNCATE files_dirs; SET FOREIGN_KEY_CHECKS = 1;" | $(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)
	@#@echo "SET FOREIGN_KEY_CHECKS = 0; TRUNCATE servers_domains; SET FOREIGN_KEY_CHECKS = 1;" | $(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)
	@echo "SET FOREIGN_KEY_CHECKS = 0; TRUNCATE replicas; SET FOREIGN_KEY_CHECKS = 1;" | $(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)
	@echo "SET FOREIGN_KEY_CHECKS = 0; TRUNCATE dirs; SET FOREIGN_KEY_CHECKS = 1;" | $(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)
	@echo "SET FOREIGN_KEY_CHECKS = 0; TRUNCATE files; SET FOREIGN_KEY_CHECKS = 1;" | $(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)
	@echo "cleaning data"
	@rm -rf test1/data/* test1/tmp/*
	@rm -rf test2/data/* test2/tmp/*
	@rm -rf test3/data/* test3/tmp/*
	@rm -rf test4/data/* test4/tmp/*
cleanall: clean
	@echo "SET FOREIGN_KEY_CHECKS = 0; TRUNCATE domains; SET FOREIGN_KEY_CHECKS = 1;" | $(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)
	@echo "SET FOREIGN_KEY_CHECKS = 0; TRUNCATE servers; SET FOREIGN_KEY_CHECKS = 1;" | $(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)

.PHONY: db clean
