# Security Guidelines for AI Agent App

## 🔒 Critical Security Information

This document outlines the security measures and sensitive files that must NEVER be committed to version control.

## ❌ NEVER COMMIT THESE FILES

### Environment Files

- `.env` (any environment file)
- `.env.local`
- `.env.development`
- `.env.production`
- `.env.staging`
- `env_example` should only contain example values, never real secrets

### API Keys and Secrets

- OpenAI API keys
- Any `*.key` files
- `*.pem` certificate files
- Files in `secrets/` directory
- Any file containing `secret` in the name
- Configuration files with real API credentials

### Sensitive Directories

- `venv/` (Python virtual environment)
- `node_modules/` (Node.js dependencies)
- `.next/` (Next.js build cache)
- `__pycache__/` (Python cache)

## ✅ Security Checklist

### Before Committing Code

- [ ] Check that `.env` files are in `.gitignore`
- [ ] Verify no API keys are hardcoded in source files
- [ ] Ensure `env_example` contains only placeholder values
- [ ] Run `git status` to check for untracked sensitive files
- [ ] Review diff for any accidentally added secrets

### Environment Setup

- [ ] Copy `env_example` to `.env` (not tracked by git)
- [ ] Add real API keys only to `.env` file
- [ ] Never share `.env` files via email, chat, or other channels
- [ ] Use environment variables in production, never hardcode secrets

### OpenAI API Security

- [ ] Store OpenAI API key in `.env` file only
- [ ] Use environment variable `OPENAI_API_KEY` in code
- [ ] Monitor OpenAI usage in their dashboard
- [ ] Set up usage limits and alerts
- [ ] Rotate API keys regularly in production

## 🛡️ Best Practices

### Development

1. **Always use environment variables** for sensitive configuration
2. **Never hardcode API keys** in source code
3. **Use placeholder values** in example files
4. **Keep dependencies updated** to avoid security vulnerabilities

### Production

1. **Use secure environment variable management** (e.g., AWS Secrets Manager, HashiCorp Vault)
2. **Implement proper access controls** for API endpoints
3. **Monitor API usage and costs** regularly
4. **Use HTTPS only** for all communications
5. **Implement rate limiting** to prevent abuse

## 🚨 What to Do If Secrets Are Accidentally Committed

If you accidentally commit sensitive information:

1. **Immediately rotate/revoke** the exposed credentials
2. **Remove the sensitive data** from git history:

   ```bash
   git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch path/to/sensitive/file' --prune-empty --tag-name-filter cat -- --all
   ```

3. **Force push** to remove from remote repository
4. **Notify team members** to pull the cleaned history
5. **Update security practices** to prevent recurrence

## 📋 File Extensions to Watch

Always be cautious with these file types:

- `.env*` - Environment files
- `.key` - Key files
- `.pem` - Certificate files
- `.p12`, `.p8` - Certificate files
- `.config` - Configuration files
- `.json` with secrets
- `.yaml`/`.yml` with secrets

## 🔍 Tools for Security Scanning

Consider using these tools to detect secrets:

- **git-secrets** - Prevents committing secrets
- **GitGuardian** - Scans for exposed secrets
- **TruffleHog** - Searches git repos for secrets
- **detect-secrets** - Baseline scanning tool

## 📞 Security Incident Response

If you discover a security vulnerability:

1. **Do not discuss publicly** (GitHub issues, public channels)
2. **Document the issue** privately
3. **Assess the impact** and affected systems
4. **Implement fixes** promptly
5. **Update documentation** and practices

## ✅ Verification Commands

Use these commands to verify your security setup:

```bash
# Check git status for untracked files
git status

# Search for potential secrets (be careful with output)
grep -r "api.key\|password\|secret" . --exclude-dir=node_modules --exclude-dir=.git

# Verify .gitignore is working
git check-ignore .env
git check-ignore backend/.env
git check-ignore frontend/.env.local
```

## 📚 Additional Resources

- [GitHub's guide to removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [OpenAI API Security Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [OWASP Security Guidelines](https://owasp.org/www-project-top-ten/)

---

**Remember: Security is everyone's responsibility. When in doubt, ask for review before committing!**
