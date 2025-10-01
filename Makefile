.PHONY: fmt run clean

fmt:
	cd edatool && npx prettier --write .

run: fmt
	cd edatool && npm run dev

clean:
	find . -type d -name "node_modules" | xargs rm -rf