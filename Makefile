GREEN   = \033[1;32m
CYAN    = \033[1;36m
YELLOW  = \033[1;33m
RESET   = \033[0m

FRAMES = 40

install:
	uv sync

run:
	@clear
	@lines=$$(wc -l < banner.txt); \
	printf '\033[?25l'; \
	for f in $$(seq 1 $(FRAMES)); do \
		awk -v off=$$f 'BEGIN{n=split("196 202 226 46 51 21 201",c," ")} \
		{s=""; for(i=1;i<=length($$0);i++){ch=substr($$0,i,1); \
		if(ch==" ") s=s ch; \
		else s=s sprintf("\033[1;38;5;%sm%s",c[(i+NR+off)%n+1],ch)} \
		print s "\033[0m"}' banner.txt; \
		sleep 0.05; \
		if [ $$f -lt $(FRAMES) ]; then printf "\033[$${lines}A"; fi; \
	done; \
	printf '\033[?25h'
	@uv run python -m src

debug:
	uv run python -m pdb -m src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

lint:
	-uv run flake8 . --exclude=.venv
	uv run mypy . --exclude "(.venv)" --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

.PHONY: install run debug clean lint
