.PHONY: fmt run clean

fmt:
	ruff format

run: fmt
	python3 -m streamlit run src/Main.py

clean:
	find . -type d -name ".ruff_cache" | xargs rm -rf