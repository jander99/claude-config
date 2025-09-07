# Simple Global Agent Delegation System

## ✅ **System Complete**

A simplified, universal global configuration system that enforces mandatory agent delegation across ALL Claude Code sessions.

## 🚀 **Usage**

```bash
# Build universal global configuration  
make build-global

# Install to ~/.claude/CLAUDE.md
make install-global

# Verify installation
make verify-global
```

## 🎯 **What It Does**

1. **Creates Universal `~/.claude/CLAUDE.md`**: Single configuration that applies to all Claude Code sessions
2. **Enforces Agent Delegation**: Mandatory use of specialized agents for all development work  
3. **Pattern-Based Detection**: Automatic agent selection based on file types and project patterns
4. **Safety Protocols**: Branch protection, context verification, quality assurance gates
5. **Cost Optimization**: Intelligent tier selection (Haiku → Sonnet → Opus)

## 📋 **Key Features**

### **Mandatory Agent Patterns**
- **Python**: `.py`, `requirements.txt` → `python-engineer`
- **JavaScript/TypeScript**: `.js`, `.jsx`, `.ts`, `.tsx` → `frontend-engineer` 
- **Java**: `.java`, `pom.xml` → `java-engineer`
- **Database**: `.sql`, migrations → `database-engineer`
- **Infrastructure**: `Dockerfile`, K8s → `devops-engineer`
- **ML/AI**: `.ipynb`, ML libraries → `ai-engineer`
- **Blockchain**: `.sol`, Web3 → `blockchain-engineer`
- **Security**: Auth, security configs → `security-engineer`
- **Git**: Git operations → `git-helper`
- **QA**: Testing, validation → `qa-engineer`

### **Universal Safety Rules**
- ✅ Branch protection before all development work
- ✅ Context verification required
- ✅ Quality assurance coordination mandatory
- ❌ Direct coding without agent coordination PROHIBITED

### **Cost Optimization**
- **Tier 1 (Haiku)**: Simple operations (`git-helper`, `technical-writer`)
- **Tier 2 (Sonnet)**: Standard development (most agents)
- **Tier 3 (Opus)**: Strategic decisions (`sr-*` agents)

## 🏗️ **Architecture**

```
src/build_simple_global.py  # Simple universal configuration generator
└── dist/global/CLAUDE.md   # Generated universal global config
    └── ~/.claude/CLAUDE.md  # Installed global enforcement
```

## 🎯 **Benefits**

1. **Universal Consistency**: Same agent delegation rules across all projects
2. **Zero Configuration**: No profiles or environments - just works
3. **Safety First**: Mandatory safety protocols prevent mistakes  
4. **Cost Efficient**: Automatic tier selection optimizes spending
5. **Quality Focused**: Built-in QA and documentation coordination

---

**Result**: Claude Code becomes a specialized agent orchestration platform with universal mandatory delegation, replacing direct coding with systematic agent coordination.