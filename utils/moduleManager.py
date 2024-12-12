from typing import Dict, Any, Callable, Optional
import asyncio
import importlib
import logging
from datetime import datetime

class AnalysisModule:
    def __init__(self, name: str, function: Callable, required_params: list):
        self.name = name
        self.function = function
        self.required_params = required_params

class AnalysisManager:
    def __init__(self):
        self.modules: Dict[str, AnalysisModule] = {}
        self.logger = logging.getLogger(__name__)
        self._register_modules()

    def _register_modules(self):
        """Register all available analysis modules"""
        module_configs = {
            "International Market Analysis": {
                "module": "internationalMarketAnalysis",
                "function": "analyze_market",
                "params": ["country", "industry", "company_name"]
            },
            "Advanced Competitor Analysis": {
                "module": "advancedCompetitorAnalysis",
                "function": "analyze_competitors",
                "params": ["country", "industry", "company_name", "competitor_count", "analysis_depth"]
            },
            "Advanced Market Analysis": {
                "module": "advancedMarketAnalysis",
                "function": "analyze_market_advanced",
                "params": ["country", "industry"]
            },
            "Competitive Product Analysis": {
                "module": "competitiveProductAnalysis",
                "function": "analyze_product",
                "params": ["product_name", "include_pricing", "include_features"]
            },
            "Competitor Finder & Crawl": {
                "module": "competitorFinder",
                "function": "find_competitors",
                "params": ["company_name", "industry"]
            },
            "Market Analysis": {
                "module": "marketAnalysis",
                "function": "analyze_market_basic",
                "params": ["country", "industry"]
            },
            "Technical Report Generator": {
                "module": "technicalReportGenerator",
                "function": "generate_technical_report",
                "params": ["report_type", "include_diagrams"]
            }
        }

        for name, config in module_configs.items():
            try:
                module = importlib.import_module(config["module"])
                function = getattr(module, config["function"])
                self.modules[name] = AnalysisModule(
                    name=name,
                    function=function,
                    required_params=config["params"]
                )
                self.logger.info(f"Successfully registered module: {name}")
            except (ImportError, AttributeError) as e:
                self.logger.warning(f"Failed to register module {name}: {str(e)}")

    def validate_params(self, analysis_type: str, params: Dict[str, Any]) -> bool:
        """Validate that all required parameters are present"""
        if analysis_type not in self.modules:
            raise ValueError(f"Unknown analysis type: {analysis_type}")
            
        module = self.modules[analysis_type]
        missing_params = [
            param for param in module.required_params 
            if param not in params or params[param] is None
        ]
        
        if missing_params:
            raise ValueError(f"Missing required parameters for {analysis_type}: {missing_params}")
        
        return True

    async def run_analysis(self, analysis_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run the specified analysis with given parameters"""
        try:
            self.validate_params(analysis_type, params)
            module = self.modules[analysis_type]
            
            # Add metadata to results
            result = await module.function(**params)
            
            return {
                "metadata": {
                    "analysis_type": analysis_type,
                    "timestamp": datetime.now().isoformat(),
                    "parameters": params
                },
                "results": result
            }
            
        except Exception as e:
            self.logger.error(f"Error running {analysis_type}: {str(e)}")
            raise

    def get_required_params(self, analysis_type: str) -> list:
        """Get list of required parameters for an analysis type"""
        if analysis_type not in self.modules:
            raise ValueError(f"Unknown analysis type: {analysis_type}")
        return self.modules[analysis_type].required_params

    def list_available_modules(self) -> list:
        """Get list of available analysis modules"""
        return list(self.modules.keys())

# Create singleton instance
analysis_manager = AnalysisManager()