import dashscope
from dashscope import MultiModalConversation
from typing import List, Dict
import yaml

class AIModelAPI:
    def __init__(self, api_key: str, config_path: str):
        self.api_key = api_key
        dashscope.api_key = api_key
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def analyze_image(self, image_path: str) -> Dict:
        """使用QwenVL分析商品图片"""
        messages = [{
            'role': 'user',
            'content': [
                {
                    'text': '请详细分析这张商品图片，包括以下方面：\n1. 服装类型\n2. 颜色和图案\n3. 材质\n4. 风格特点\n5. 细节设计\n6. 适合场合'
                },
                {
                    'image': image_path
                }
            ]
        }]

        response = MultiModalConversation.call(
            model='qwen-vl-plus',
            messages=messages
        )
        
        return response.output.choices[0].message.content

    def generate_copy(self, 
                     product_info: Dict,
                     keywords: List[str],
                     template_type: str,
                     platform: str) -> str:
        """使用Qwen-turbo生成营销文案"""
        prompt = self._create_prompt(product_info, keywords, template_type, platform)
        
        response = dashscope.Generation.call(
            model='qwen-turbo',
            prompt=prompt
        )
        
        return response.output.text

    def _create_prompt(self,
                      product_info: Dict,
                      keywords: List[str],
                      template_type: str,
                      platform: str) -> str:
        """创建文案生成提示词"""
        platform_config = self.config['platforms'][platform]
        
        prompt = f"""
        基于以下信息生成{platform_config['name']}平台的营销文案:
        
        商品信息:
        {product_info}
        
        关键词:
        {', '.join(keywords)}
        
        文案风格: {platform_config['style']}
        模板类型: {template_type}
        字数限制: {platform_config['max_length']}字以内
        
        平台特性:
        {', '.join(platform_config['features'])}
        
        请生成一篇吸引人的营销文案,请只返回文案,不要返回其他内容。
        """
        return prompt

