# Skill Registry — hamster-foods-backend

**Generated**: 2026-03-29
**Project**: hamster-foods-backend
**Source**: ~/.config/opencode/skills/

## Available Skills

### Development Skills
| Skill | Trigger | Description |
|-------|---------|-------------|
| `branch-pr` | When creating a pull request, opening a PR, or preparing changes for review. | PR creation workflow for Agent Teams Lite following the issue-first enforcement system. |
| `go-testing` | When writing Go tests, using teatest, or adding test coverage. | Go testing patterns for Gentleman.Dots, including Bubbletea TUI testing. |
| `issue-creation` | When creating a GitHub issue, reporting a bug, or requesting a feature. | Issue creation workflow for Agent Teams Lite following the issue-first enforcement system. |
| `judgment-day` | When user says "judgment day", "judgment-day", "review adversarial", "dual review", "doble review", "juzgar", "que lo juzguen". | Parallel adversarial review protocol that launches two independent blind judge sub-agents simultaneously. |
| `skill-creator` | When user asks to create a new skill, add agent instructions, or document patterns for AI. | Creates new AI agent skills following the Agent Skills spec. |

### SDD Skills (Spec-Driven Development)
| Skill | Trigger | Description |
|-------|---------|-------------|
| `sdd-init` | When user wants to initialize SDD in a project, or says "sdd init", "iniciar sdd", "openspec init". | Initialize Spec-Driven Development context in any project. |
| `sdd-explore` | When the orchestrator launches you to think through a feature, investigate the codebase, or clarify requirements. | Explore and investigate ideas before committing to a change. |
| `sdd-propose` | When the orchestrator launches you to create or update a proposal for a change. | Create a change proposal with intent, scope, and approach. |
| `sdd-spec` | When the orchestrator launches you to write or update specs for a change. | Write specifications with requirements and scenarios (delta specs for changes). |
| `sdd-design` | When the orchestrator launches you to write or update the technical design for a change. | Create technical design document with architecture decisions and approach. |
| `sdd-tasks` | When the orchestrator launches you to create or update the task breakdown for a change. | Break down a change into an implementation task checklist. |
| `sdd-apply` | When the orchestrator launches you to implement one or more tasks from a change. | Implement tasks from the change, writing actual code following the specs and design. |
| `sdd-verify` | When the orchestrator launches you to verify a completed (or partially completed) change. | Validate that implementation matches specs, design, and tasks. |
| `sdd-archive` | When the orchestrator launches you to archive a change after implementation and verification. | Sync delta specs to main specs and archive a completed change. |

## Project Conventions

No project-level agent instructions found (AGENTS.md, CLAUDE.md, .cursorrules, etc.).

## Usage Notes

- **SDD Skills**: Orchestrate the full development lifecycle (explore → propose → spec → design → tasks → apply → verify → archive)
- **Development Skills**: Handle specific development tasks (PRs, issues, reviews)
- **Skill Creator**: Create new skills for project-specific patterns

## Quick Reference

```bash
# Initialize SDD in a project
/sdd-init

# Start a new change
/sdd-explore <topic>

# Create a PR
/branch-pr

# Adversarial code review
/judgment-day
```