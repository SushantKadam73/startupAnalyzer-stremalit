import os
from google.generativeai import GenerativeModel, configure
from typing import List, Optional
from datetime import datetime
import markdown
import pdfkit

class TechnicalReportGenerator:
    def __init__(self, company_name: Optional[str] = None):
        configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = GenerativeModel('gemini-1.5-flash')
        self.data_folder = f'data_{company_name}' if company_name else 'data_analysis'
        self.output_folder = os.path.join(self.data_folder, 'Reports')
        os.makedirs(self.output_folder, exist_ok=True)
        
        self.report_types = {
            "PESTEL Analysis": ["PESTEL_report.md"],
            "Advanced Market": ["advanced_market_report.md"],
            "International Market": "international_market_report.md" ,
            "Competitor Analysis": "competitor_product_report.md",
            "Advanced Competitor": "advanced_competitor_report.md"
        }

    def read_source_files(self, analysis_type: str) -> str:
        """Read content from source files"""
        combined_content = []
        filenames = self.report_types.get(analysis_type, [])
        
        for filename in filenames:
            filepath = os.path.join(self.data_folder, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    combined_content.append(f"### Content from {filename}\n{content}\n")
            except FileNotFoundError:
                print(f"File not found: {filepath}")
                
        return "\n".join(combined_content)

    async def generate_technical_report(self, company_name: str, analysis_type: str) -> str:
        """Generate technical report"""
        try:
            content = self.read_source_files(analysis_type)
            if not content:
                return ""

            prompt = f"""Generate a comprehensive technical report for {company_name} based on the following analysis.
            Focus on technical aspects, implementation details, and actionable recommendations.
            
            Source Content:
            {content}

            Format the report in markdown with:
            - Technical specifications
            - Implementation roadmap
            - Risk assessment
            - Resource requirements
            - Timeline estimates
            - Cost projections
            
            Use tables, lists, and code blocks where appropriate."""

            response = self.model.generate_content(prompt)
            report_content = response.text

            # Save report
            report_path = os.path.join(self.output_folder, f"technical_report_{analysis_type.lower().replace(' ', '_')}.md")
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)

            return report_path

        except Exception as e:
            print(f"Error generating technical report: {e}")
            return ""

async def generate_report(company_name: str, analysis_type: str) -> str:
    """Wrapper function for technical report generation"""
    generator = TechnicalReportGenerator(company_name)
    return await generator.generate_technical_report(company_name, analysis_type)