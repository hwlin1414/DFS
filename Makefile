MYSQL=mysql
MYSQL_USER=dfs
MYSQL_PASS=dfspass
MYSQL_DB=dfs
DOMAIN=demo

all: dbdomain

db:
	@$(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)

dbdomain:
	@echo "adding domain $(DOMAIN)"
	#@echo "INSERT INTO domains(name, folder, url) VALUE('$(DOMAIN)', '$(DOMAIN)', '')" | $(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)
	@echo "INSERT INTO servers_domains(server_id, domain_id) SELECT servers.id, domains.id from servers, domains WHERE domains.name = '$(DOMAIN)'" | $(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)

clean:
	@echo "cleaning database"
	@echo "SET FOREIGN_KEY_CHECKS = 0; TRUNCATE servers_domains; SET FOREIGN_KEY_CHECKS = 1;" | $(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)
	@echo "SET FOREIGN_KEY_CHECKS = 0; TRUNCATE replicas; SET FOREIGN_KEY_CHECKS = 1;" | $(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)
	@echo "SET FOREIGN_KEY_CHECKS = 0; TRUNCATE files; SET FOREIGN_KEY_CHECKS = 1;" | $(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)
	#@echo "SET FOREIGN_KEY_CHECKS = 0; TRUNCATE domains; SET FOREIGN_KEY_CHECKS = 1;" | $(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)
	#@echo "TRUNCATE servers" | $(MYSQL) -u $(MYSQL_USER) -p$(MYSQL_PASS) $(MYSQL_DB)

.PHONY: db clean
