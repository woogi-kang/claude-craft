# Research: Mac GitHub SSH Setup

**Date:** 2026-01-06
**Author:** woogi
**Status:** Ready for Draft

## SEO Keywords

```yaml
seo_keywords:
  primary: "Mac GitHub SSH setup"
  secondary:
    - "SSH key Mac tutorial"
    - "GitHub SSH key macOS"
    - "ssh-keygen ed25519 Mac"
    - "GitHub authentication SSH"
  long_tail:
    - "how to setup SSH key for GitHub on Mac"
    - "Mac SSH key GitHub step by step"
    - "ed25519 SSH key Mac GitHub"
  search_intent: "tutorial"
  competition: "medium"
  suggested_title_keywords: ["Mac", "GitHub", "SSH", "Setup", "Guide", "2025"]
```

## Topic Analysis

```yaml
topic_analysis:
  main_topic: "Setting up SSH keys on Mac for GitHub"
  sub_topics:
    - "What is SSH authentication"
    - "Why use SSH over HTTPS"
    - "Ed25519 vs RSA algorithm"
    - "SSH agent and keychain integration"
    - "Testing SSH connection"
  target_audience: "beginner to intermediate"
  key_questions:
    - "How do I generate an SSH key on Mac?"
    - "What algorithm should I use for SSH keys?"
    - "How do I add SSH key to GitHub?"
    - "How to avoid entering passphrase every time?"
```

## Web Research

### W001: GitHub Official Docs - Generating SSH Key
- **URL:** https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
- **Type:** Official documentation
- **Credibility:** High
- **Key Points:**
  - Ed25519 is recommended algorithm
  - Use `--apple-use-keychain` flag on macOS
  - Configure `~/.ssh/config` for automatic key loading
  - macOS Monterey changed flag from `-K` to `--apple-use-keychain`

### W002: GitHub Official Docs - Adding SSH Key
- **URL:** https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
- **Type:** Official documentation
- **Credibility:** High
- **Key Points:**
  - Settings > SSH and GPG keys
  - Can add authentication or signing keys
  - Title should be descriptive (e.g., "MacBook Pro 2024")

### W003: SSH Key Best Practices 2025
- **URL:** https://www.brandonchecketts.com/archives/ssh-ed25519-key-best-practices-for-2025
- **Type:** Expert blog
- **Credibility:** High
- **Key Points:**
  - Ed25519 is current standard for professional users
  - 10+ years of wide use
  - Never share private key
  - Consider hardware-backed keys (ed25519-sk) for high security

### W004: Ed25519 vs RSA Comparison
- **URL:** https://goteleport.com/blog/comparing-ssh-keys/
- **Type:** Technical analysis
- **Credibility:** High
- **Key Points:**
  - Ed25519: 68 char public key vs RSA: 3072 chars
  - Faster performance, better security
  - More resistant to PRNG failures
  - OpenSSH 6.5+ supports Ed25519

### W005: DEV Community Tutorial
- **URL:** https://dev.to/pthapa1/setting-up-ssh-keys-on-mac-for-github-3b2m
- **Type:** Community tutorial
- **Credibility:** Medium
- **Key Points:**
  - Step-by-step Mac-specific instructions
  - Passphrase is optional but recommended
  - pbcopy for clipboard integration

## Key Insights

### Pain Points
- HTTPS requires entering credentials repeatedly
- Password authentication deprecated by GitHub
- Managing multiple SSH keys can be confusing
- Passphrase entry on every use is annoying

### How It Works
- SSH uses public-key cryptography (asymmetric encryption)
- Private key stays on local machine
- Public key registered with GitHub
- SSH agent manages keys and passphrases

### Best Practices
1. **Use Ed25519** - Modern, secure, small key size
2. **Set passphrase** - Extra security layer
3. **Use keychain** - `--apple-use-keychain` for macOS
4. **Configure ssh config** - Auto-load keys on startup
5. **Descriptive titles** - Easy key management

### Common Pitfalls
- Using deprecated RSA algorithm with small key size
- Not configuring ssh-agent properly
- Forgetting to add key after reboot
- Sharing private key accidentally
- Using same key across multiple machines (not recommended)

## Suggested Outline

```markdown
# Suggested Outline

## Hook
"Tired of entering your GitHub password every time you push? SSH keys are the answer - and they're more secure too."

## Sections
1. Introduction - Why SSH over HTTPS
2. What You'll Need - Prerequisites
3. Step-by-Step Setup
   - Generate SSH key (ed25519)
   - Start SSH agent
   - Add key to agent with keychain
   - Copy public key
   - Add to GitHub
   - Test connection
4. Bonus: SSH Config for Auto-loading
5. Troubleshooting Common Issues
6. Conclusion - Next steps

## Estimated Length
~1200-1500 words

## Code Examples Needed
- [x] ssh-keygen command
- [x] ssh-agent commands
- [x] ssh-add with keychain
- [x] pbcopy command
- [x] ssh -T test
- [x] SSH config file content
```

## Sources

- [GitHub Docs - Generating SSH Key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [GitHub Docs - Adding SSH Key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
- [SSH Key Best Practices 2025](https://www.brandonchecketts.com/archives/ssh-ed25519-key-best-practices-for-2025)
- [Comparing SSH Keys](https://goteleport.com/blog/comparing-ssh-keys/)
- [DEV Community - SSH Keys on Mac](https://dev.to/pthapa1/setting-up-ssh-keys-on-mac-for-github-3b2m)
