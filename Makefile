build:
	cd yatta/client && npm run build
	rm -f yatta/config/__internal.py
	poetry build

clean-repo:
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "Uncommitted changes found. Please commit or stash your changes."; \
		exit 1; \
	fi

testpublish: build clean-repo
	poetry publish -r testpypi


test:
	poetry run pytest


@PHONY: build testpublish clean-repo