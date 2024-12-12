from together import Together 
from groq import Groq  
from typing import Dict, Optional
import asyncio
import json
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from datetime import datetime


load_dotenv()
# # international market analysis
# user_startup = "100xEngineering"
# country = "Europe"
# industry = "AI-accelerated Full-Stack engineering courses" 
# data_folder = f'data_{user_startup}'

class BaseAnalyst:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.tavily = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
    
    def research(self, query: str) -> dict:
        try:
            search_result = self.tavily.search(query=query, search_depth="basic", max_results=3)
            print(f"\nTavily Search Results for: {query}")
            print("=" * 50)
            
            formatted_results = []
            for idx, item in enumerate(search_result.get('results', []), 1):
                print(f"\nSource {idx}: {item.get('url')}")
                print(f"Content: {item.get('content')[:200]}...")  # Print first 200 chars
                formatted_results.append({
                    'url': item.get('url'),
                    'content': item.get('content'),
                    'score': item.get('score')
                })
            return formatted_results
        except Exception as e:
            print(f"Research error: {e}")
            return []

    def chat(self, prompt: str) -> str:
        # Shortened prompt handling
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0.7,
        )
        return response.choices[0].message.content

    def analyze(self, country: str, industry: str) -> Dict:
        research_query = self.get_research_query(country, industry)
        research_results = self.research(research_query)
        
        # Analyze each source separately to manage context length
        analyses = []
        for source in research_results:
            prompt = f"""Analyze this source for {industry} industry in {country}:
            Source: {source['url']}
            Content: {source['content']}
            
            Focus on: {self.analysis_prompt}
            """
            analysis = self.chat(prompt)
            analyses.append(analysis)
        
        # Combine analyses
        final_analysis = "\n\n".join(analyses)
        
        return {
            "analysis": final_analysis,
            "sources": research_results,
            "query": research_query,
            "timestamp": datetime.now().isoformat()
        }

    def get_research_query(self, country: str, industry: str) -> str:
        return f"{self.research_prompt} {industry} industry {country}"

class MarketSizeAnalyst(BaseAnalyst):
    analysis_prompt = """Focus on:
        1. TAM, SAM, SOM specific to the industry
        2. Industry Growth Potential and Trends
        3. Target Market Population"""
    research_prompt = "market size statistics TAM SAM market growth trends"

class CompetitiveLandscapeAnalyst(BaseAnalyst):
    analysis_prompt = """Focus on:
        1. Domestic Competition
        2. Market Entry Barriers
        3. Brand Loyalty Patterns"""
        # 4. Supply Chain Considerations"""
    research_prompt = "competitive landscape market analysis companies supply chain barriers entry"

class EconomicAnalyst(BaseAnalyst):
    analysis_prompt = """Focus on:
        1. GDP and GDP per capita
        2. Inflation and Interest Rates
        3. Disposable Income Levels
        # 4. Investment Climate and FDI"""
        # 5. Exchange Rates and Currency Volatility
    research_prompt = "economic indicators GDP inflation interest rates disposable income"

class PoliticalAnalyst(BaseAnalyst):
    analysis_prompt = """Focus on:
        1. Political Stability
        2. Government Intervention
        3. Regulatory Framework
        4. Trade Agreements and Tariffs"""
    research_prompt = "political stability government intervention regulatory framework trade agreements"

class CulturalAnalyst(BaseAnalyst):
    analysis_prompt = """Focus on:
        1. Cultural Norms and Values
        2. Consumer Behavior
        3. Language Barriers
        4. Localization Requirements"""
    research_prompt = "cultural norms consumer behavior language barriers localization"

class RiskAnalyst(BaseAnalyst):
    analysis_prompt = """Focus on:
        1. Cybersecurity and other Threats
        2. Natural Disaster Risks"""
        # 3. Infrastructure Risks
        # 4. Political Risks"""
    research_prompt = "cybersecurity threats natural disaster risks infrastructure political risks"

class CompanyDataAnalyst(BaseAnalyst):
    analysis_prompt = """Focus on:
        1. Company Overview
        2. Financial Performance
        3. Market Position
        4. Key Products/Services"""
        # 5. International Presence"""
    research_prompt = "company profile financial performance market position"

class ReportEditor(BaseAnalyst):
    def compile_report(self, raw_analysis: Dict) -> str:
        report_prompt = f"""As a Chief Market Research Editor, create a professional markdown-formatted market research report from this data:

{json.dumps(raw_analysis, indent=2)}

Use this strict markdown structure:
# {raw_analysis['metadata']['industry'].title()} Industry Analysis: {raw_analysis['metadata']['country']}

## Executive Summary

## Research Methodology
### Data Sources
### Analysis Framework

## Market Overview

## Detailed Analysis
### Market Size Analysis
### Competitive Landscape
### Economic Environment
### Political Factors
### Cultural Considerations
### Risk Assessment

## Key Findings and Insights

## Market Opportunities and Recommendations

## Risk Factors and Mitigation Strategies

## References and Sources

Format using proper markdown with:
- Headers (# ## ###)
- Lists (- * 1.)
- Tables where appropriate
- Bold and italic for emphasis
- Block quotes for important insights
- Code blocks for data/statistics

If possible make tables for data and statistics, graphs, and charts to visualize the data.

Maintain professional language and analytical objectivity."""

        return self.chat(report_prompt)

def save_raw_analysis(output_dir: str, country: str, industry: str, analysis_data: Dict) -> str:
    """Save analysis data in plain text format"""
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    raw_filename = os.path.join(output_dir, "international_market.md")
    
    with open(raw_filename, "w", encoding='utf-8') as f:
        # Write metadata section
        f.write(f"# Raw Market Analysis: {industry} in {country}\n\n")
        f.write("## Metadata\n")
        f.write(f"- Analysis Date: {timestamp}\n")
        f.write(f"- Country: {country}\n")
        f.write(f"- Industry: {industry}\n")
        if analysis_data['metadata'].get('company_name'):
            f.write(f"- Company: {analysis_data['metadata']['company_name']}\n")
        f.write("\n---\n\n")
        
        # Write each analysis section with better formatting
        for section, data in analysis_data['analyses'].items():
            f.write(f"## {section}\n")
            if isinstance(data, dict) and 'analysis' in data:
                f.write(f"{data['analysis']}\n\n")
            else:
                f.write(f"{data}\n\n")
    
    return raw_filename

async def analyze_market(country: str, industry: str, company_name: Optional[str] = None) -> str:
    """International market analysis function"""
    try:
        # Create data folder dynamically
        data_folder = f'data_{company_name}' if company_name else 'data_analysis'
        os.makedirs(data_folder, exist_ok=True)
        
        analysts = [
            MarketSizeAnalyst(),
            CompetitiveLandscapeAnalyst(),
            EconomicAnalyst(),
            PoliticalAnalyst(),
            CulturalAnalyst(),
            RiskAnalyst()
        ]
        
        # Add company analysis if company name provided
        if company_name:
            company_analyst = CompanyDataAnalyst()
            company_result = await asyncio.to_thread(
                lambda: company_analyst.analyze(country, f"{industry} {company_name}")
            )
            analysts.append(company_analyst)
        
        tasks = [asyncio.create_task(
            asyncio.to_thread(lambda a: a.analyze(country, industry), analyst)
        ) for analyst in analysts]
        
        results = await asyncio.gather(*tasks)
        
        raw_analysis = {
            "metadata": {
                "country": country,
                "industry": industry,
                "company_name": company_name,
                "analysis_date": datetime.now().isoformat(),
                "version": "1.0"
            },
            "analyses": {
                "Market Size": results[0],
                "Competitive Landscape": results[1],
                "Economic Analysis": results[2],
                "Political Analysis": results[3],
                "Cultural Analysis": results[4],
                "Risk Analysis": results[5],
                **({"Company Analysis": company_result} if company_name else {})
            }
        }
        
        # Use the centralized data folder
        output_dir = data_folder
        
        # Save analysis in markdown format
        raw_filename = save_raw_analysis(output_dir, country, industry, raw_analysis)
        raw_filename = "international_analysis"
        print(f"\nRaw analysis saved to: {raw_filename}")
        
        # Generate report content
        report_editor = ReportEditor()
        report_content = report_editor.compile_report(raw_analysis)
        
        # Save both markdown and raw data
        report_path = os.path.join(data_folder, "international_market_report.md")
        with open(report_path, "w", encoding='utf-8') as f:
            f.write(report_content)
            
        # Save raw data for technical report
        raw_data = {
            "metadata": {
                "analysis_type": "International Market",
                "country": country,
                "industry": industry,
                "company_name": company_name,
                "timestamp": datetime.now().isoformat()
            },
            "analyses": raw_analysis
        }
        
        json_path = os.path.join(data_folder, "international_market_raw.json")
        with open(json_path, "w", encoding='utf-8') as f:
            json.dump(raw_data, f, indent=2, ensure_ascii=False)
        
        return report_path
    except Exception as e:
        print(f"Analysis error: {e}")
        return ""

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python internationalMarketAnalysis.py <country> <industry> <company_name>")
        sys.exit(1)
        
    result = asyncio.run(analyze_market(sys.argv[1], sys.argv[2], sys.argv[3]))
    if result:
        print(f"Analysis saved to: {result}")
    else:
        print("Analysis failed")


