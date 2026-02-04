setup:
	uv sync

run:
	docker compose up -d

stop:
	docker compose down

clean:
	docker compose down
	docker volume rm weaviate_data ollama_data

fetch_models:
	docker compose exec ollama ollama pull nomic-embed-text
	docker compose exec ollama ollama pull llama3.2

populate_db:
	uv run scripts/populate_db.py

run_langgraph:
	uv run langgraph dev

# UI setup and run targets
ui-setup:
	./scripts/deploy_ui.sh

ui-run:
	@if [ ! -d "chat-ui" ]; then \
		echo "chat-ui not found. Run 'make setup-ui' first."; \
		exit 1; \
	fi
	cd chat-ui && pnpm dev

ui-clean:
	rm -rf chat-ui