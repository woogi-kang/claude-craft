# Clinic Crawl Project Notes

## Project Structure
- Location: `clinic-crawl/` (project root) with `clinic_crawl/` (Python package)
- CSV: `samples/skin_clinics.csv` - 4,255 Korean skin clinics
- Agent: `.claude/agents/clinic-crawler-agent.md`
- 5 Skills: moai-clinic-{triage,social,doctors,popup,chain}

## Data Distribution (Triage Results)
- 2,900 custom domains, 427 naver blogs, 115 kakao, 80 instagram, 76 youtube, 15 imweb, 637 no URL
- 89 chain domains (velyb: 57, vandsclinic: 52, maypure: 41, cnpskin: 28)

## Key Technical Notes
- Config paths use `Path(__file__).resolve()` for CWD-independent execution
- Python package with hyphenated project name needs underscore package dir
- Security hook blocks writes outside project dir (including ~/.claude/plans/)
- Chain detection picks up platform domains (naver.com, kakao.com) as chains - filter needed
