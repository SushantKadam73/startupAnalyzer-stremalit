from typing import Dict, Optional
import asyncio
from PESTEL_Analysis import BaseAnalyst
import json
import os
from datetime import datetime

user_startup = "100xEngineering"
data_folder = f'data_{user_startup}'

class CompetitiveProductAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Product Analysis
        1. Core Product Features
           - Key functionalities
           - Technical capabilities
           - Platform/Technology stack
        2. Product Market Fit
           - Target audience
           - Use cases
           - Customer segments
        3. Product Development
           - Release cycles
           - Innovation roadmap
           - Recent updates
        4. User Experience
           - Interface design
           - Ease of use
           - Customer feedback"""
    research_prompt = f'Competitive Produt analysis of {user_startup} and its competitors'

class PricingStrategyAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Pricing Strategy
        1. Pricing Models
           - Subscription tiers
           - One-time purchases
           - Enterprise pricing
        2. Price Comparison
           - Market positioning
           - Value proposition
        3. Revenue Model
           - Monetization strategy
           - Payment structures
        4. Promotional Strategy
           - Discounts
           - Trials
           - Special offers"""
    research_prompt = f'Pricing analysis of {user_startup} and its competitors'

class CompetitiveAdvantageAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Competitive Advantages
        1. Unique Selling Points
           - Key differentiators
           - Proprietary technology
        2. Market Position
           - Industry ranking
           - Market share
        3. Brand Strength
           - Brand recognition
           - Customer loyalty
        4. Innovation Focus
           - R&D investments
           - Patents and IP"""
    research_prompt = f' competitive analysis of {user_startup} and its competitors'

async def analyze_competitor(country: str, industry: str, company_name: Optional[str] = None) -> str:
    """Competitive product analysis function"""
    try:
        # Create data folder dynamically
        data_folder = f'data_{company_name}' if company_name else 'data_analysis'
        os.makedirs(data_folder, exist_ok=True)
        
        analysts = {
            "Product Analysis": CompetitiveProductAnalyst(),
            "Pricing Strategy": PricingStrategyAnalyst(),
            "Competitive Advantages": CompetitiveAdvantageAnalyst()
        }

        results = await asyncio.gather(*[
            asyncio.to_thread(analyst.analyze, company_name, industry)
            for analyst in analysts.values()
        ])

        # Format report content
        report_content = [
            f"# Competitor Product Analysis: {company_name}",
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
        report_path = os.path.join(data_folder, "competitor_product_report.md")
        with open(report_path, "w", encoding='utf-8') as f:
            f.write("\n".join(report_content))

        # Save raw data for technical report
        raw_data = {
            "metadata": {
                "analysis_type": "Competitor Product Analysis",
                "country": country,
                "industry": industry,
                "company_name": company_name,
                "timestamp": datetime.now().isoformat()
            },
            "sections": analysis_data
        }
        
        json_path = os.path.join(data_folder, "competitor_product_raw.json")
        with open(json_path, "w", encoding='utf-8') as f:
            json.dump(raw_data, f, indent=2, ensure_ascii=False)

        return report_path

    except Exception as e:
        print(f"Analysis error: {e}")
        return ""

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python competitive_product_analysis.py <country> <industry> <company_name>")
        sys.exit(1)
        
    result = asyncio.run(analyze_competitor(sys.argv[1], sys.argv[2], sys.argv[3]))
    if result:
        print(f"Analysis saved to: {result}")
    else:
        print("Analysis failed")