from typing import Dict, List, Optional
import asyncio
from PESTEL_Analysis import BaseAnalyst
import json
import os
from datetime import datetime

class MarketSizeAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Market Size Analysis
        1. Total Addressable Market (TAM)
        2. Serviceable Available Market (SAM)
        3. Serviceable Obtainable Market (SOM)
        4. Market Growth Rate
        5. Market Segments and Demographics"""
    research_prompt = "market size statistics revenue growth segments demographics"

class CompetitiveLandscapeAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Competitive Analysis
        1. Major Players and Market Share
        2. Competitive Advantages
        3. Entry Barriers
        4. Substitutes and Alternatives
        5. Porter's Five Forces Analysis"""
    research_prompt = "market competitors analysis market share competitive landscape"

class KeywordResearchAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Keyword Analysis
        1. Search Volume Trends
        2. Popular Search Terms
        3. Consumer Intent Analysis
        4. Content Gap Analysis
        5. Keyword Difficulty Assessment"""
    research_prompt = "keyword research search trends consumer intent digital marketing"

class SentimentAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Sentiment Analysis
        1. Brand Perception
        2. Consumer Feedback Analysis
        3. Social Media Sentiment
        4. Review Analysis
        5. Market Reception Trends"""
    research_prompt = "consumer sentiment brand perception social media feedback reviews"

class RiskAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Risk Analysis
        1. Market Risks
        2. Financial Risks
        3. Operational Risks
        4. Strategic Risks
        5. Mitigation Strategies"""
    research_prompt = "market risks financial risks operational risks strategic analysis"

async def analyze_market_advanced(country: str, industry: str, company_name: Optional[str] = None) -> str:
    """Advanced market analysis function"""
    try:
        # Create data folder dynamically
        data_folder = f'data_{company_name}' if company_name else 'data_analysis'
        os.makedirs(data_folder, exist_ok=True)
        
        analysts = {
            "Market Size": MarketSizeAnalyst(),
            "Competitive Landscape": CompetitiveLandscapeAnalyst(),
            "Keyword Research": KeywordResearchAnalyst(),
            "Sentiment": SentimentAnalyst(),
            "Risk": RiskAnalyst()
        }

        results = await asyncio.gather(*[
            asyncio.to_thread(analyst.analyze, country, industry)
            for analyst in analysts.values()
        ])
        
        # Format report content
        report_content = [
            f"# Advanced Market Analysis: {industry} in {country}",
            f"\n## Analysis Date: {datetime.now().strftime('%Y-%m-%d')}",
            "\n## Table of Contents\n"
        ]
        
        analysis_data = {}
        for (section_name, _), result in zip(analysts.items(), results):
            report_content.append(f"\n## {section_name} Analysis\n")
            report_content.append(result['analysis'])
            report_content.append("\n### Sources")
            for source in result['sources']:
                report_content.append(f"- [{source['url']}]({source['url']})")
            analysis_data[section_name] = result
        
        # Save both markdown and raw data
        report_path = os.path.join(data_folder, "advanced_market_report.md")
        with open(report_path, "w", encoding='utf-8') as f:
            f.write("\n".join(report_content))
            
        # Save raw data for technical report
        raw_data = {
            "metadata": {
                "analysis_type": "Advanced Market",
                "country": country,
                "industry": industry,
                "company_name": company_name,
                "timestamp": datetime.now().isoformat()
            },
            "sections": analysis_data
        }
        
        json_path = os.path.join(data_folder, "advanced_market_raw.json")
        with open(json_path, "w", encoding='utf-8') as f:
            json.dump(raw_data, f, indent=2, ensure_ascii=False)
        
        return report_path
    except Exception as e:
        print(f"Analysis error: {e}")
        return ""

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python advance_market_analysis.py <country> <industry> <company_name>")
        sys.exit(1)
        
    result = asyncio.run(analyze_market_advanced(sys.argv[1], sys.argv[2], sys.argv[3]))
    if result:
        print(f"Analysis saved to: {result}")
    else:
        print("Analysis failed")