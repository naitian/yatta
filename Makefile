build:
	cd yatta/client && npm run build
	rm -f yatta/config/__internal.py
	poetry build


testpublish: build
	poetry publish -r testpypi


@PHONY: build testpublish