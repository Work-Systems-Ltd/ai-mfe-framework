.PHONY: up down build logs ps clean lint test smoke

# Start all services
up:
	docker compose up -d

# Start with build
up-build:
	docker compose up -d --build

# Stop all services
down:
	docker compose down

# Stop and remove volumes
clean:
	docker compose down -v

# Build all images
build:
	docker compose build

# View logs (follow)
logs:
	docker compose logs -f

# View specific service logs
logs-%:
	docker compose logs -f $*

# Show running services
ps:
	docker compose ps

# Restart a specific service
restart-%:
	docker compose restart $*

# Run linting across all backend apps
lint-backend:
	cd common/templates/backend && poetry run ruff check src/ tests/ && poetry run mypy src/
	cd apps/shell/backend && poetry run ruff check src/ tests/ && poetry run mypy src/
	cd apps/permissions/backend && poetry run ruff check src/ tests/ && poetry run mypy src/
	cd apps/mfe-example-app-1/backend && poetry run ruff check src/ tests/ && poetry run mypy src/

# Run tests across all backend apps
test-backend:
	cd common/templates/backend && poetry run pytest
	cd apps/shell/backend && poetry run pytest
	cd apps/permissions/backend && poetry run pytest
	cd apps/mfe-example-app-1/backend && poetry run pytest

# Smoke test - verify all services are healthy
smoke:
	@echo "Waiting for services to be ready..."
	@sleep 10
	@echo "Checking Keycloak..."
	@curl -sf http://localhost:8080/realms/mfe > /dev/null && echo "  Keycloak: OK" || echo "  Keycloak: FAIL"
	@echo "Checking Shell Backend..."
	@curl -sf http://localhost:8000/internal/health > /dev/null && echo "  Shell Backend: OK" || echo "  Shell Backend: FAIL"
	@echo "Checking OpenFGA..."
	@curl -sf http://localhost:8081/healthz > /dev/null && echo "  OpenFGA: OK" || echo "  OpenFGA: FAIL"
	@echo "Checking registered apps..."
	@curl -sf http://localhost:8000/api/apps && echo "" || echo "  App listing: FAIL"
	@echo "Smoke test complete."
