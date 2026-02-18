---
name: google-dorking
description: Advanced search engine dorking for asset discovery
---

# Google Dorking Skill

## When to Use

When searching for exposed assets, files, or information indexed by search engines.

## Dork Categories

### Admin Panels

```
site:<target> inurl:admin
site:<target> intitle:"login" OR intitle:"sign in"
site:<target> inurl:dashboard
site:<target> inurl:portal
site:<target> inurl:cpanel OR inurl:webmail
```

### Configuration Files

```
site:<target> filetype:env
site:<target> filetype:yml OR filetype:yaml
site:<target> filetype:conf OR filetype:cfg
site:<target> filetype:ini
site:<target> filetype:xml "password"
```

### Database Exposure

```
site:<target> inurl:phpmyadmin
site:<target> inurl:adminer
site:<target> filetype:sql
site:<target> "index of" "database"
site:<target> inurl:_config OR inurl:db_config
```

### Sensitive Documents

```
site:<target> filetype:pdf "confidential" OR "internal"
site:<target> filetype:xlsx OR filetype:csv "password"
site:<target> filetype:doc "restricted"
site:<target> "index of" filetype:pem OR filetype:key
```

### API Discovery

```
site:<target> inurl:api inurl:v1 OR inurl:v2
site:<target> inurl:swagger OR inurl:api-docs
site:<target> inurl:graphql OR inurl:graphiql
site:<target> filetype:json "api_key" OR "apiKey"
site:<target> inurl:rest OR inurl:endpoint
```

### Error Messages / Debug

```
site:<target> "stack trace" OR "traceback"
site:<target> "SQL syntax" OR "mysql_fetch"
site:<target> "Warning:" filetype:php
site:<target> inurl:debug OR inurl:test
site:<target> "index of /" +.git
```

### Backup Files

```
site:<target> filetype:bak OR filetype:old
site:<target> filetype:tar.gz OR filetype:zip
site:<target> "index of" "backup"
site:<target> inurl:backup OR inurl:bkp
```

### Credentials

```
site:<target> filetype:log "password"
site:<target> "BEGIN RSA PRIVATE KEY"
site:<target> filetype:env "DB_PASSWORD" OR "SECRET_KEY"
"<target>" site:pastebin.com OR site:paste.ee
"<target>" site:trello.com "password" OR "key"
```

## Engines

1. **Google**: Most comprehensive index
2. **DuckDuckGo HTML**: No CAPTCHA, good for automation
3. **Bing**: Sometimes indexes pages Google misses
4. **Yandex**: Good for Eastern European targets

## Automation

```bash
python3 scripts/osint/market_watch.py "<target>"
```

## Rules

- [CRITICAL] Passive only - never access found URLs
- Rate limit queries (2-5 seconds between requests)
- Rotate User-Agents
- Document every dork used and results found
- Pass actionable URLs to Pentester for verification
