# Global CLAUDE.md Build System

## 🎯 **System Overview**

The global build system generates personalized `~/.claude/CLAUDE.md` configurations that enforce mandatory agent delegation across ALL Claude Code sessions on your machine. This creates consistent, role-based agent usage patterns while maintaining flexibility for different work contexts.

## 🚀 **Quick Start**

```bash
# Build with default settings (developer profile, development environment)
make build-global

# Build for different profile/environment combinations
make build-global PROFILE=researcher ENV=production

# Build and install to ~/.claude/ in one step
make install-global PROFILE=developer ENV=development

# See available options
make show-global-profiles
make show-global-environments
```

## 📁 **Architecture**

```
data/global/
├── base/                    # NON-NEGOTIABLE enforcement rules
│   └── core-enforcement.md  # Universal agent delegation protocols
├── profiles/                # User role-based configurations
│   ├── developer.yaml       # Full-stack web development focus
│   └── researcher.yaml      # AI/ML research and analysis focus
├── environments/            # Environment-specific overrides
│   ├── development.yaml     # Relaxed rules for experimentation
│   └── production.yaml      # Strict safety and compliance
└── customizations/          # (Future: personal preferences)
```

## 🎭 **Available Profiles**

### **Developer Profile** (`developer.yaml`)
- **Focus**: Full-stack web development
- **Priority Agents**: python-engineer, frontend-engineer, database-engineer
- **Cost Budget**: $75/day, $25/session
- **Workflow**: Feature branches, comprehensive testing, API-focused docs

### **Researcher Profile** (`researcher.yaml`)
- **Focus**: AI/ML research and experimental work
- **Priority Agents**: ai-researcher, sr-ai-researcher, ai-engineer, data-engineer
- **Cost Budget**: $100/day, $40/session (higher for research iterations)
- **Workflow**: Research branches, experimental testing, comprehensive documentation

## 🌐 **Available Environments**

### **Development Environment** (`development.yaml`)
- **Safety**: Advisory warnings (non-blocking)
- **Cost**: 1.5x daily budget, 2x session budget
- **Workflow**: Relaxed testing requirements, minimal documentation
- **Experimental**: Allows prompt-engineer and flexible agent combinations

### **Production Environment** (`production.yaml`)
- **Safety**: Strict enforcement (blocking)
- **Cost**: 0.8x daily budget (conservative spending)
- **Workflow**: Comprehensive testing, full documentation, mandatory security review
- **Compliance**: Audit logging, regulatory compliance, rollback plans

## 🛠️ **Build Process**

1. **Base Layer**: Universal agent delegation rules (cannot be overridden)
2. **Profile Layer**: Role-specific agent priorities and workflow preferences
3. **Environment Layer**: Context-specific safety and cost adjustments
4. **Generation**: Composed into complete `~/.claude/CLAUDE.md`

## 📊 **Configuration Examples**

### Developer + Development (Default)
- **Agent Priority**: Web development agents (python, frontend, database)
- **Safety Level**: Advisory (warnings only)
- **Cost**: Moderate budget with experimentation room
- **Perfect for**: Daily development work, prototyping, learning

### Researcher + Development
- **Agent Priority**: Research agents (ai-researcher, sr-ai-researcher)
- **Safety Level**: Advisory (experimental work)
- **Cost**: Higher budget for research iterations
- **Perfect for**: Experimental ML work, research prototyping

### Developer + Production
- **Agent Priority**: Web development agents with security focus
- **Safety Level**: Strict (blocking unsafe operations)
- **Cost**: Conservative spending, careful tier selection
- **Perfect for**: Production deployments, hotfixes, maintenance

### Researcher + Production
- **Agent Priority**: Research agents with rigorous validation
- **Safety Level**: Strict with comprehensive documentation
- **Cost**: Conservative but sufficient for production research
- **Perfect for**: Production ML models, research deployments

## 🎯 **Key Benefits**

1. **Consistency**: Same agent delegation rules across all projects
2. **Role-Based**: Optimized for your specific work type
3. **Environment-Aware**: Different safety/cost rules for dev vs prod
4. **Team Synchronization**: Share profiles across team members
5. **Cost Optimization**: Intelligent budget management per role/environment
6. **Safety First**: Universal branch protection and quality gates

## 🔧 **Customization**

### Adding New Profiles
```yaml
# data/global/profiles/devops.yaml
profile: devops
display_name: "DevOps Engineer"
agent_priorities:
  critical: ["devops-engineer", "security-engineer", "database-engineer"]
  # ... rest of configuration
```

### Adding New Environments
```yaml
# data/global/environments/staging.yaml
environment: staging
display_name: "Staging Environment"
enforcement_overrides:
  branch_protection: "standard"
  # ... rest of configuration
```

## 📦 **Installation Workflow**

```bash
# 1. Build for your role and environment
make build-global PROFILE=developer ENV=development

# 2. Review generated configuration
cat dist/global/CLAUDE.md

# 3. Install to global location
make install-global

# 4. Verify installation
ls -la ~/.claude/CLAUDE.md

# 5. Restart Claude Code to apply global settings
```

## 🔄 **Team Usage**

### Individual Developer Setup
```bash
# Each developer chooses their profile
make install-global PROFILE=developer ENV=development
```

### Research Team Setup
```bash
# Research team uses research profile
make install-global PROFILE=researcher ENV=development
```

### Production Deployment
```bash
# Everyone uses strict production settings
make install-global PROFILE=developer ENV=production
```

## 🚀 **Future Enhancements**

1. **Team Synchronization**: Pull configurations from shared repositories
2. **Custom Profiles**: User-specific profile generation
3. **Analytics Integration**: Track effectiveness of different configurations
4. **Auto-Updates**: Automatically update when agent ecosystem changes
5. **A/B Testing**: Compare different global configuration approaches

---

## 📚 **Next Steps**

1. **Try Different Combinations**: Experiment with profile/environment pairs
2. **Create Custom Profiles**: Add your own role-specific configurations  
3. **Team Rollout**: Deploy consistent configurations across your team
4. **Monitor Effectiveness**: Track cost and quality improvements
5. **Iterate and Improve**: Refine configurations based on usage patterns

The global build system transforms Claude Code from a per-project tool into a comprehensive, role-aware development platform with consistent agent delegation across your entire development workflow.