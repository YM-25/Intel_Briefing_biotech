
import sys
import os
import datetime
from typing import List
import argparse

# Add sensors path
sys.path.append(os.path.join(os.path.dirname(__file__), "src", "sensors"))

try:
    from v2ex_radar import V2EXRadar, Lead
    from chrome_radar import ChromeRadar, ChromeAssetOpportunity
except ImportError as e:
    print(f"❌ Error importing sensors: {e}")
    sys.exit(1)

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def generate_report(leads: List[Lead], opportunities: List[ChromeAssetOpportunity], filename: str = "Daily_Hit_List.md"):
    print(f"📝 Generating Hit List Report: {filename}...")
    
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# 💰 Tactical Revenue Dept. Hit List ({date_str})\n\n")
        f.write("> **Mission**: Identify Cash Flow & Asset Building Opportunities.\n\n")
        
        # Section 1: Soft-Target Radar (V2EX)
        f.write("## 🎯 Soft-Target Radar: V2EX (ServiceLeads)\n")
        f.write("*Focus: High Desperation, Urgent Needs, Paid Gigs.*\n\n")
        
        if not leads:
            f.write("*(No high-signal leads found via RSS. Check manually.)*\n\n")
        else:
            for i, lead in enumerate(leads, 1):
                urgency_icon = "🔥" if lead.desperation_score >= 100 else "⚠️" if lead.desperation_score >= 50 else "💼"
                f.write(f"### {i}. {urgency_icon} {lead.title}\n")
                f.write(f"- **Score**: `{lead.desperation_score}` | **Tags**: `{', '.join(lead.tags)}`\n")
                f.write(f"- **Summary**: {lead.summary}\n")
                f.write(f"- **Action**: [View Source]({lead.url})\n\n")
        
        f.write("---\n\n")
        
        # Section 2: Chrome Landlord (SaaS Assets)
        f.write("## 💎 Chrome Landlord (SaaS Opportunities)\n")
        f.write("*Focus: High Traffic (>5k Users) + Low Rating (<3.8).*\n\n")
        
        if not opportunities:
            f.write("*(No 'Ugly Cash Cows' found in this scan. Try expanding categories.)*\n\n")
        else:
            for i, opp in enumerate(opportunities, 1):
                f.write(f"### {i}. 🐮 {opp.name}\n")
                f.write(f"- **Stats**: {opp.rating}⭐ | **{opp.user_count_str}** Users\n")
                f.write(f"- **Kill Shot**: {opp.kill_shot}\n")
                f.write(f"- **Opportunity**: Rewrite this with modern UI and fix the complaints.\n")
                f.write(f"- **Link**: [Chrome Store]({opp.url})\n\n")

    print(f"✅ Report saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Antigravity Bounty Hunter")
    parser.add_argument("--days", type=int, default=2, help="Days to look back for leads")
    parser.add_argument("--limit", type=int, default=3, help="Max items per section")
    args = parser.parse_args()

    print("🚀 Starting Tactical Revenue Mission...")
    
    # 1. Run V2EX Radar
    v2ex = V2EXRadar()
    leads = v2ex.fetch_leads(days=args.days)
    
    # Filter & Sort
    high_value_leads = [l for l in leads if l.desperation_score > 0]
    high_value_leads.sort(key=lambda x: x.desperation_score, reverse=True)
    high_value_leads = high_value_leads[:args.limit]
    
    # 2. Run Chrome Radar
    chrome = ChromeRadar()
    opportunities = chrome.scan_opportunities(limit=args.limit)
    
    # 3. Generate Report
    report_file = os.path.join(os.path.dirname(__file__), "reports", "tactical", f"Hit_List_{datetime.datetime.now().strftime('%Y-%m-%d')}.md")
    generate_report(high_value_leads, opportunities, report_file)
    
    print("🏁 Mission Complete.")

if __name__ == "__main__":
    main()
