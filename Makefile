.PHONY: fmt run clean

fmt:
	npx prettier --write .

run: fmt
	npm run dev

clean:
	find . -type d -name "node_modules" | xargs rm -rf