.PHONY: test validate vault-check clean

test:
	cd apps/pre-calling-system && python3 -m pytest -q

vault-check:
	python3 /home/ubuntu/skills/ai-receptionist-production-vault/scripts/validate_vault.py brain/obsidian-vault

validate: test vault-check
	git diff --check
	! find . -type f \( -name '*.db' -o -name '*.sqlite' -o -name '.env' \) -not -path './.git/*' | grep -q .
	@echo 'Unified repository validation passed.'

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf apps/pre-calling-system/.pytest_cache apps/pre-calling-system/run
