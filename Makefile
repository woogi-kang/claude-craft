# Claude Craft Makefile
# 간편한 설치 및 관리를 위한 Makefile
#
# 사용법:
#   make install      - 심볼릭 링크로 설치 (개발용, 기본값)
#   make install-copy - 파일 복사로 설치 (독립 설치)
#   make export       - 배포 패키지 생성
#   make uninstall    - 설치 제거
#   make status       - 설치 상태 확인
#   make help         - 도움말 표시

.PHONY: install install-copy export uninstall status help clean publish

# 기본 타겟
.DEFAULT_GOAL := help

# 변수
SCRIPT := ./scripts/install.sh
CLAUDE_HOME := $(HOME)/.claude

# 심볼릭 링크로 설치 (개발용 - 업데이트 자동 반영)
install:
	@echo "🔗 Installing claude-craft with symbolic links..."
	@$(SCRIPT) --link

# 파일 복사로 설치 (독립 설치)
install-copy:
	@echo "📋 Installing claude-craft by copying files..."
	@$(SCRIPT) --copy

# 배포 패키지 생성
export:
	@echo "📦 Creating distribution package..."
	@$(SCRIPT) --export

# 설치 제거
uninstall:
	@echo "🗑️  Uninstalling claude-craft..."
	@rm -f "$(CLAUDE_HOME)/statusline.py"
	@rm -rf "$(CLAUDE_HOME)/agents"
	@rm -rf "$(CLAUDE_HOME)/skills"
	@rm -rf "$(CLAUDE_HOME)/hooks"
	@echo "✅ Uninstalled. settings.json preserved."

# 설치 상태 확인
status:
	@echo "📊 Claude Craft Installation Status"
	@echo "===================================="
	@echo ""
	@echo "📁 ~/.claude/ contents:"
	@ls -la "$(CLAUDE_HOME)" 2>/dev/null || echo "   (not found)"
	@echo ""
	@echo "🔗 Symlink status:"
	@if [ -L "$(CLAUDE_HOME)/agents" ]; then \
		echo "   agents  → $$(readlink $(CLAUDE_HOME)/agents)"; \
	elif [ -d "$(CLAUDE_HOME)/agents" ]; then \
		echo "   agents  → (copied directory)"; \
	else \
		echo "   agents  → (not installed)"; \
	fi
	@if [ -L "$(CLAUDE_HOME)/skills" ]; then \
		echo "   skills  → $$(readlink $(CLAUDE_HOME)/skills)"; \
	elif [ -d "$(CLAUDE_HOME)/skills" ]; then \
		echo "   skills  → (copied directory)"; \
	else \
		echo "   skills  → (not installed)"; \
	fi
	@if [ -L "$(CLAUDE_HOME)/hooks" ]; then \
		echo "   hooks   → $$(readlink $(CLAUDE_HOME)/hooks)"; \
	elif [ -d "$(CLAUDE_HOME)/hooks" ]; then \
		echo "   hooks   → (copied directory)"; \
	else \
		echo "   hooks   → (not installed)"; \
	fi
	@echo ""
	@echo "📊 Component counts:"
	@if [ -d "$(CLAUDE_HOME)/agents" ]; then \
		agent_count=$$(find "$(CLAUDE_HOME)/agents" -name "*.md" 2>/dev/null | wc -l | tr -d ' '); \
		echo "   Agents: $$agent_count"; \
	fi
	@if [ -d "$(CLAUDE_HOME)/skills" ]; then \
		skill_count=$$(find "$(CLAUDE_HOME)/skills" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' '); \
		echo "   Skills: $$skill_count"; \
	fi

# 도움말
help:
	@echo "🎩 Claude Craft - Installation Commands"
	@echo "========================================"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install       심볼릭 링크로 설치 (개발용, 업데이트 자동 반영)"
	@echo "  install-copy  파일 복사로 설치 (독립 설치)"
	@echo "  export        배포 패키지(.zip) 생성"
	@echo "  uninstall     설치 제거 (settings.json 유지)"
	@echo "  status        현재 설치 상태 확인"
	@echo "  publish       GitHub Pages 배포 준비 (원라인 설치)"
	@echo "  clean         dist 폴더 정리"
	@echo "  help          이 도움말 표시"
	@echo ""
	@echo "Examples:"
	@echo "  make install  # 심볼릭 링크로 설치 (권장)"
	@echo "  make status   # 설치 상태 확인"

# dist 폴더 정리
clean:
	@echo "🧹 Cleaning dist folder..."
	@rm -rf ./dist
	@echo "✅ Cleaned."

# GitHub Pages 배포 준비 (원라인 설치 지원)
publish:
	@echo "🚀 Preparing for GitHub Pages deployment..."
	@chmod +x ./docs/install.sh
	@echo ""
	@echo "✅ Ready for GitHub Pages!"
	@echo ""
	@echo "📋 Setup Instructions:"
	@echo "   1. Push docs/install.sh to GitHub"
	@echo "   2. Go to Repository Settings → Pages"
	@echo "   3. Set Source: 'Deploy from a branch'"
	@echo "   4. Set Branch: 'main' (or master), folder: '/docs'"
	@echo "   5. Save and wait for deployment"
	@echo ""
	@echo "🔗 After setup, users can install with:"
	@echo "   curl -LsSf https://<username>.github.io/claude-craft/install.sh | sh"
	@echo ""
	@echo "📦 Alternative (raw GitHub):"
	@echo "   curl -LsSf https://raw.githubusercontent.com/<username>/claude-craft/main/docs/install.sh | sh"
