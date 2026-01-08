---
title: "How to Set Up SSH Keys for GitHub on Mac: The Complete Guide"
subtitle: "Stop typing passwords forever with this 5-minute setup"
tags: ["github", "ssh", "macos", "git", "tutorial"]
cover_image: ""
canonical_url: ""
draft: true
tone: "mixed"
word_count: 1450
seo:
  primary_keyword: "Mac GitHub SSH setup"
  secondary_keywords: ["SSH key macOS", "GitHub authentication SSH", "ssh-keygen ed25519"]
  meta_description: "Learn how to set up SSH keys for GitHub on Mac in 5 minutes. Use Ed25519 for better security, integrate with macOS Keychain, and never type passwords again."
  slug: "mac-github-ssh-setup-guide"
---

# How to Set Up SSH Keys for GitHub on Mac: The Complete Guide

Tired of typing your GitHub password every time you push code? I was too. After setting up a new Mac last week, I realized I'd been doing this wrong for years. SSH keys are not just more convenient — they're also more secure.

In this guide, I'll walk you through setting up SSH keys for GitHub on Mac, the right way. We'll use Ed25519 (the modern standard) and integrate with macOS Keychain so you never have to type your passphrase again.

## Table of Contents
- [Why SSH Over HTTPS?](#why-ssh-over-https)
- [What You'll Need](#what-youll-need)
- [Step 1: Generate Your SSH Key](#step-1-generate-your-ssh-key)
- [Step 2: Start the SSH Agent](#step-2-start-the-ssh-agent)
- [Step 3: Add Key to Agent with Keychain](#step-3-add-key-to-agent-with-keychain)
- [Step 4: Copy Your Public Key](#step-4-copy-your-public-key)
- [Step 5: Add the Key to GitHub](#step-5-add-the-key-to-github)
- [Step 6: Test Your Connection](#step-6-test-your-connection)
- [Bonus: Auto-load Keys on Startup](#bonus-auto-load-keys-on-startup)
- [Troubleshooting](#troubleshooting)
- [Wrapping Up](#wrapping-up)

## Why SSH Over HTTPS?

Before we dive in, let's talk about why you should bother with SSH:

1. **No more passwords** — Once set up, authentication happens automatically
2. **Better security** — SSH keys use public-key cryptography, which is harder to compromise than passwords
3. **GitHub recommends it** — Password authentication for Git operations was [deprecated by GitHub](https://github.blog/changelog/2021-08-12-git-password-authentication-is-shutting-down/)

## What You'll Need

- A Mac running macOS (Sierra 10.12.2 or later for best results)
- A GitHub account
- Terminal access (built-in on all Macs)

That's it. Let's get started.

## Step 1: Generate Your SSH Key

Open Terminal and run this command:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Replace `your_email@example.com` with your actual GitHub email.

### What's happening here?

- `-t ed25519` — Uses the Ed25519 algorithm (more on this below)
- `-C "email"` — Adds a comment to identify the key

### Why Ed25519?

You might see older tutorials using RSA. Ed25519 is the better choice in 2025:

| Feature | Ed25519 | RSA |
|---------|---------|-----|
| Key size | 68 characters | 3000+ characters |
| Security | More resistant to attacks | Still secure at 4096-bit |
| Speed | Faster | Slower |
| Support | OpenSSH 6.5+ (2014) | Universal |

Ed25519 has been the recommended standard for about 10 years now. Unless you're working with ancient systems, use it.

### During generation

You'll see prompts:

```
Enter file in which to save the key (/Users/you/.ssh/id_ed25519):
```

Press **Enter** to accept the default location.

```
Enter passphrase (empty for no passphrase):
```

**I recommend setting a passphrase**. Yes, it's one more thing to remember, but it adds a crucial layer of security. If someone gets access to your machine, they still can't use your key without the passphrase.

Don't worry — we'll set up Keychain integration so you won't have to type it every time.

## Step 2: Start the SSH Agent

The SSH agent manages your keys in memory. Start it with:

```bash
eval "$(ssh-agent -s)"
```

You should see something like:

```
Agent pid 12345
```

## Step 3: Add Key to Agent with Keychain

This is where macOS magic happens. Run:

```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

The `--apple-use-keychain` flag stores your passphrase in macOS Keychain. This means:
- Your passphrase is securely stored
- It persists across reboots
- You only type it once (or never, if you use Touch ID)

> **Note for older macOS versions**: If you're on macOS before Monterey (12.0), use `-K` instead of `--apple-use-keychain`.

## Step 4: Copy Your Public Key

Now we need to copy the public key (the `.pub` file) to add it to GitHub:

```bash
pbcopy < ~/.ssh/id_ed25519.pub
```

This copies the key directly to your clipboard. `pbcopy` is a handy Mac-specific command.

**Important**: Never share your private key (`id_ed25519` without `.pub`). The public key is meant to be shared; the private key is not.

## Step 5: Add the Key to GitHub

1. Go to [GitHub.com](https://github.com) and log in
2. Click your profile picture → **Settings**
3. In the sidebar, click **SSH and GPG keys**
4. Click **New SSH key**
5. Fill in the form:
   - **Title**: Something descriptive like "MacBook Pro 2024" or "Work Laptop"
   - **Key type**: Authentication Key
   - **Key**: Paste with `Cmd + V`
6. Click **Add SSH key**

GitHub might ask for your password to confirm. That's normal.

## Step 6: Test Your Connection

Let's make sure everything works:

```bash
ssh -T git@github.com
```

First time connecting? You'll see:

```
The authenticity of host 'github.com (...)' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
Are you sure you want to continue connecting (yes/no)?
```

Type `yes` and press Enter.

If successful, you'll see:

```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

That "does not provide shell access" message is expected — GitHub doesn't offer shell access, only Git operations.

## Bonus: Auto-load Keys on Startup

To make your SSH key automatically load every time you open Terminal, create (or edit) `~/.ssh/config`:

```bash
nano ~/.ssh/config
```

Add these lines:

```
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
```

Save with `Ctrl + O`, then exit with `Ctrl + X`.

This configuration tells macOS to:
- Automatically add keys to the SSH agent
- Use Keychain for passphrases
- Use your Ed25519 key for GitHub connections

## Troubleshooting

### "Permission denied (publickey)"

This usually means the key isn't loaded. Try:

```bash
# Check if key is in agent
ssh-add -l

# If empty, add it again
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

### "Could not open a connection to your authentication agent"

The SSH agent isn't running. Start it:

```bash
eval "$(ssh-agent -s)"
```

### Using Multiple GitHub Accounts

If you have work and personal GitHub accounts, you can use different keys:

```
# Personal GitHub
Host github.com
  IdentityFile ~/.ssh/id_ed25519_personal

# Work GitHub
Host github-work
  HostName github.com
  IdentityFile ~/.ssh/id_ed25519_work
```

Then clone work repos using: `git clone git@github-work:company/repo.git`

### Converting Existing HTTPS Repos to SSH

Already have repos cloned with HTTPS? Switch them:

```bash
# Check current remote
git remote -v

# Change to SSH
git remote set-url origin git@github.com:username/repo.git
```

## Wrapping Up

That's it! You've set up SSH keys on your Mac for GitHub. Here's what we covered:

1. Generated an Ed25519 key (modern and secure)
2. Added it to the SSH agent with Keychain integration
3. Registered it with GitHub
4. Configured auto-loading for convenience

Now you can push and pull without ever typing a password again. Your future self will thank you.

---

Got questions or ran into issues? Drop a comment below — I'm happy to help.

— woogi

---

**Sources:**
- [GitHub Docs - Generating SSH Keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [GitHub Docs - Adding SSH Keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
- [SSH Key Best Practices 2025](https://www.brandonchecketts.com/archives/ssh-ed25519-key-best-practices-for-2025)
- [Comparing SSH Key Algorithms](https://goteleport.com/blog/comparing-ssh-keys/)

---
*Draft generated: 2026-01-06*
*Ready for review: /blog-review*
