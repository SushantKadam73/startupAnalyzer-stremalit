from typing import Dict, List, Optional
import asyncio
from groq import Groq
import json
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from datetime import datetime
from PESTEL_Analysis import BaseAnalyst

user_startup = "100xEngineering"
data_folder = f'data_{user_startup}'

class MarketingStrategyAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Marketing Strategy
        1. Marketing Channels
        2. Partnership Analysis
        3. Content Strategy
           - Social Media, Webinars, Podcasts, Blog content...
        4. Brand Positioning"""
    research_prompt = f'Competitive analysis of {user_startup} and its competitors'

class KeywordSEOAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## SEO and Digital Presence
        1. Keyword Analysis
           - Top ranking keywords
           - Search volume
        2. SEO Strategy
           - Content optimization
           - Technical SEO
        3. Social Media Presence
           - Platform analysis
           - Engagement metrics"""
    research_prompt = f'Competitive analysis of {user_startup} and its competitors'

class ValuationAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Company Valuations
        1. Funding History
        2. Investment Rounds
        3. Key Investors
        4. Cap Table Analysis
        5. Current Valuation"""
    research_prompt = f'Competitive analysis of {user_startup} and its competitors'



class RecentUpdatesAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Recent Company Updates
        1. Latest News
        2. Product Releases
        3. Major Milestones
        4. Company Achievements
        5. Market Impact"""
    research_prompt = f'Competitive analysis of {user_startup} and its competitors'

class FinancialAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Financial Analysis
        1. Revenue Metrics
           - Revenue growth
           - Revenue streams
           - Key financial indicators
        2. Profitability Analysis
           - Margins, Operating costs, Profitability trends
        3. Financial Health
           - Burn rate, Cash reserves, debt structure
        4. Unit Economics
           - Customer acquisition cost, Lifetime value, 
           - Other key metrics"""
    research_prompt = f'Competitive analysis of {user_startup} and its competitors'

async def analyze_competitor(company_name: str, industry: str) -> str:
    try:
        analysts = {

            "Marketing Strategy": MarketingStrategyAnalyst(),
            "Keyword/SEO": KeywordSEOAnalyst(),
            "Valuations": ValuationAnalyst(),
            "Recent Updates": RecentUpdatesAnalyst(),
            "Financial Analysis": FinancialAnalyst()
        }

        results = await asyncio.gather(*[
            asyncio.to_thread(analyst.analyze, company_name, industry)
            for analyst in analysts.values()
        ])

        output_dir = data_folder
        os.makedirs(output_dir, exist_ok=True)

        report_content = [
            f"# Competitor Analysis: {company_name}",
            f"\n## Industry: {industry}",
            f"\n## Analysis Date: {datetime.now().strftime('%Y-%m-%d')}",
            "\n## Table of Contents\n"
        ]

        for (section_name, _), result in zip(analysts.items(), results):
            report_content.append(f"\n## {section_name}\n")
            report_content.append(result['analysis'])
            report_content.append("\n### Sources")
            for source in result['sources']:
                report_content.append(f"- [{source['url']}]({source['url']})")

        report_path = os.path.join(output_dir, "adv_competitor.md")
        with open(report_path, "w", encoding='utf-8') as f:
            f.write("\n".join(report_content))

        return report_path

    except Exception as e:
        print(f"Analysis error: {e}")
        return ""

async def analyze_competitor_advanced(country: str, industry: str, company_name: Optional[str] = None) -> str:
    """Advanced competitor analysis function"""
    try:
        # Create data folder dynamically
        data_folder = f'data_{company_name}' if company_name else 'data_analysis'
        os.makedirs(data_folder, exist_ok=True)
        
        analysts = {
            "Marketing Strategy": MarketingStrategyAnalyst(),
            "Keyword/SEO": KeywordSEOAnalyst(),
            "Valuations": ValuationAnalyst(),
            "Recent Updates": RecentUpdatesAnalyst(),
            "Financial Analysis": FinancialAnalyst()
        }

        results = await asyncio.gather(*[
            asyncio.to_thread(analyst.analyze, company_name, industry)
            for analyst in analysts.values()
        ])

        # Format report content
        report_content = [
            f"# Advanced Competitor Analysis: {company_name}",
            f"\n## Industry: {industry}",
            f"\n## Analysis Date: {datetime.now().strftime('%Y-%m-%d')}",
            "\n## Table of Contents\n"
        ]

        analysis_data = {}
        for (section_name, _), result in zip(analysts.items(), results):
            report_content.append(f"\n## {section_name}\n")
            report_content.append(result['analysis'])
            report_content.append("\n### Sources")
            for source in result['sources']:
                report_content.append(f"- [{source['url']}]({source['url']})")
            analysis_data[section_name] = result

        # Save both markdown and raw data
        report_path = os.path.join(data_folder, "advanced_competitor_report.md")
        with open(report_path, "w", encoding='utf-8') as f:
            f.write("\n".join(report_content))

        # Save raw data for technical report
        raw_data = {
            "metadata": {
                "analysis_type": "Advanced Competitor Analysis",
                "country": country,
                "industry": industry,
                "company_name": company_name,
                "timestamp": datetime.now().isoformat()
            },
            "sections": analysis_data
        }
        
        json_path = os.path.join(data_folder, "advanced_competitor_raw.json")
        with open(json_path, "w", encoding='utf-8') as f:
            json.dump(raw_data, f, indent=2, ensure_ascii=False)

        return report_path

    except Exception as e:
        print(f"Analysis error: {e}")
        return ""

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python advance_competitor_analysis.py <country> <industry> <company_name>")
        sys.exit(1)
        
    result = asyncio.run(analyze_competitor_advanced(sys.argv[1], sys.argv[2], sys.argv[3]))
    if result:
        print(f"Analysis saved to: {result}")
    else:
        print("Analysis failed")