from typing import Dict, List, Optional
import asyncio

# from together import Together
from groq import Groq  
import json
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from datetime import datetime
load_dotenv()

# Remove these hardcoded values
# user_startup = "100xEngineering"
# country = "India"
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
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                max_tokens=800,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Chat error: {e}")
            return ""

    def analyze(self, country: str, industry: str) -> Dict:
        research_query = self.get_research_query(country, industry)
        research_results = self.research(research_query)
        
        analyses = []
        for source in research_results:
            prompt = f"""Analyze this source for {industry} industry in {country}:
            Source: {source['url']}
            Content: {source['content']}
            
            {self.analysis_prompt}
            
            Format your response in markdown with:
            - Clear headers and sections
            - Bulleted lists for key points
            - Tables for numerical data
            - Bold/italic for emphasis
            - Blockquotes for important insights
            """
            analysis = self.chat(prompt)
            analyses.append(analysis)
        
        final_analysis = "\n\n".join(analyses)
        
        return {
            "analysis": final_analysis,
            "sources": research_results,
            "query": research_query,
            "timestamp": datetime.now().isoformat()
        }

    def get_research_query(self, country: str, industry: str) -> str:
        return f"{self.research_prompt} {industry} industry {country}"




class TechnologicalAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Technological Analysis
        1. Technology Adoption Rates
        2. Digital Infrastructure
        3. Innovation Landscape
        4. Tech Skills Availability
        5. R&D Investment Trends"""
    research_prompt = "technological environment digital infrastructure innovation research development"


class EconomicAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Economic Analysis
        1. GDP and GDP per capita
        2. Inflation and Interest Rates
        3. Disposable Income Levels
        4. Exchange Rates and Currency Volatility
        5. Investment Climate and FDI"""
    research_prompt = "economic indicators GDP inflation interest rates disposable income"

class PoliticalAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Political Analysis
        1. Political Stability
        2. Government Intervention
        3. Regulatory Framework
        4. Trade Agreements and Tariffs"""
    research_prompt = "political stability government intervention regulatory framework trade agreements"

class SociologicalAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Sociological Analysis
        1. Cultural Norms and Values
        2. Demographics and Population Trends
        3. Age Distribution and Generation Gaps
        4. Career Attitudes and Work Culture
        5. Education and Skill Levels
        6. Consumer Behavior Patterns"""
    research_prompt = "demographics cultural norms population trends career attitudes social factors"

class LegalAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Legal Analysis
        1. Industry Regulations and Compliance
        2. Licensing and Permit Requirements
        3. Intellectual Property Rights
        4. Tax Laws and Regulations"""
    research_prompt = "legal regulations compliance licenses permits employment law consumer protection IP rights taxation"

class EnvironmentalAnalyst(BaseAnalyst):
    analysis_prompt = """Provide a markdown-formatted analysis focusing on:
        ## Environmental Analysis
        1. Environmental Regulations
        2. Carbon Footprint Requirements
        3. Climate Change Impacts and Risks
        4. Sustainability Standards"""
    research_prompt = "environmental regulations climate change sustainability carbon footprint green initiatives"

def save_raw_analysis(output_dir: str, country: str, industry: str, analysis_data: Dict) -> str:
    filename = os.path.join(output_dir, f"{country}_{industry}_raw_analysis.json")
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
    return filename

async def pestel_market(country: str, industry: str, company_name: Optional[str] = None) -> str:
    try:
        # Create data folder dynamically
        data_folder = f'data_{company_name}' if company_name else 'data_analysis'
        os.makedirs(data_folder, exist_ok=True)
        
        analysts = {

            "Political": PoliticalAnalyst(),
            "Economic": EconomicAnalyst(),
            "Sociological": SociologicalAnalyst(),
            "Technology": TechnologicalAnalyst(),
            "Legal": LegalAnalyst(),
            "Environmental": EnvironmentalAnalyst()

        }

        results = await asyncio.gather(*[
            asyncio.to_thread(analyst.analyze, country, industry)
            for analyst in analysts.values()
        ])
        
        # Use the centralized data folder
        output_dir = data_folder
        
        report_content = [
            f"# {industry.title()} Industry Analysis: {country}",
            f"\n## Analysis Date: {datetime.now().strftime('%Y-%m-%d')}",
            "\n## Table of Contents\n"
        ]
        
        for (section_name, _), result in zip(analysts.items(), results):
            report_content.append(f"\n## {section_name} Analysis\n")
            report_content.append(result['analysis'])
            report_content.append("\n### Sources")
            for source in result['sources']:
                report_content.append(f"- [{source['url']}]({source['url']})")

        # Save markdown report
        report_path = os.path.join(output_dir,"PESTEL_report.md")
        with open(report_path, "w", encoding='utf-8') as f:
            f.write("\n".join(report_content))
        
        return report_path
    except Exception as e:
        print(f"Analysis error: {e}")
        return ""

if __name__ == "__main__":
    # Remove test code or modify for testing
    pass