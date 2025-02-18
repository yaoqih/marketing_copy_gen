from dataclasses import dataclass
from typing import List, Optional, Dict
from api import AIModelAPI
import asyncio
import yaml
import time
@dataclass
class MarketingTemplate:
    name: str

    structure: str
    example: str
    suitable_platforms: List[str]

class MarketingCopyGenerator:
    def __init__(self, api_key: str, config_path: str):
        self.config_path = config_path
        self.ai_api = AIModelAPI(api_key, config_path)
        self.config = self._load_config()
        self.templates = self._init_templates()
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _init_templates(self) -> Dict[str, MarketingTemplate]:
        """从配置文件初始化营销文案模板"""
        templates = {}
        for template_id, template_data in self.config['templates'].items():
            templates[template_id] = MarketingTemplate(
                name=template_data['name'],
                structure=template_data['structure'],
                example=template_data['example'],
                suitable_platforms=template_data['suitable_platforms']
            )
        return templates
    
    def get_available_platforms(self) -> List[str]:
        """获取所有支持的平台"""
        return list(self.config['platforms'].keys())

    def get_suitable_templates_for_platform(self, platform: str) -> List[str]:
        """获取适合特定平台的模板"""
        return [
            template_id 
            for template_id, template in self.templates.items() 
            if platform in template.suitable_platforms
        ]

    async def generate_copy(self,
                          image_path: str,
                          keywords: List[str],
                          template_name: str,
                          platform: str) -> str:
        """生成营销文案的主要函数"""
        # 验证平台
        if platform not in self.config['platforms']:
            raise ValueError(f"不支持的平台: {platform}")
            
        # 验证模板
        if template_name not in self.templates:
            raise ValueError(f"未知的模板类型: {template_name}")
            
        # 验证模板是否适用于该平台
        if platform not in self.templates[template_name].suitable_platforms:
            raise ValueError(f"模板 {template_name} 不适用于平台 {platform}")
        
        # 分析图片
        start_time = time.time()
        product_info = self.ai_api.analyze_image(image_path)
        end_time = time.time()
        print(f"分析图片时间: {end_time - start_time} 秒")
        
        # 生成文案
        start_time = time.time()
        marketing_copy = self.ai_api.generate_copy(
            product_info=product_info,
            keywords=keywords,
            template_type=self.templates[template_name].structure,
            platform=platform

        )
        end_time = time.time()
        print(f"生成文案时间: {end_time - start_time} 秒")
        return marketing_copy

    def get_available_templates(self) -> List[str]:
        """获取所有可用的模板名称"""
        return list(self.templates.keys()) 
    
async def main():
    generator = MarketingCopyGenerator(api_key="sk-", config_path="config/marketing_config.yaml")

    
    # 生成营销文案
    copy = await generator.generate_copy(
        image_path="https://cbu01.alicdn.com/img/ibank/2017/498/559/4285955894_944273139.jpg",
        keywords=["时尚", "秋季", "约会"],
        template_name="lifestyle",
        platform="xiaohongshu"
    )
    
    print(copy)
    
    # 获取可用模板
    templates = generator.get_available_templates()
    print("可用模板:", templates) 

if __name__ == "__main__":
    asyncio.run(main())