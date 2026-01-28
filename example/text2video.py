import time
import jwt
import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class KlingVideoClient:
    def __init__(self, access_key, secret_key, timeout=(5, 30), max_retries=5):
        self.ak = access_key
        self.sk = secret_key
        self.base_url = "https://api-beijing.klingai.com"
        self.timeout = timeout
        self.session = requests.Session()
        retry = Retry(
            total=max_retries,
            backoff_factor=0.6,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _get_token(self):
        """
        生成符合 JWT 标准的 API Token
        """
        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }
        payload = {
            "iss": self.ak,
            "exp": int(time.time()) + 1800,  # 30分钟有效期
            "nbf": int(time.time()) - 5      # 生效时间
        }
        token = jwt.encode(payload, self.sk, headers=headers)
        return token

    def _get_headers(self):
        """
        组装请求头
        """
        token = self._get_token()
        # 注意：PyJWT 2.x+ 返回的是 string，旧版本可能返回 bytes
        if isinstance(token, bytes):
            token = token.decode('utf-8')
            
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

    def create_text2video_task(self, 
                               prompt, 
                               model_name="kling-v1", 
                               negative_prompt="", 
                               aspect_ratio="16:9", 
                               duration="5", 
                               mode="std", 
                               cfg_scale=0.5,
                               camera_control=None):
        """
        创建文生视频任务
        :param model_name: 模型名称 (kling-v1, kling-v2-5-turbo 等)
        :param prompt: 正向提示词
        :param negative_prompt: 负向提示词
        :param aspect_ratio: 画幅 (16:9, 9:16, 1:1)
        :param duration: 时长 "5" 或 "10"
        :param mode: "std"(标准) 或 "pro"(专业)
        :param cfg_scale: 自由度 [0, 1] (仅部分模型支持)
        :param camera_control: 运镜控制字典 (可选)
        """
        url = f"{self.base_url}/v1/videos/text2video"
        
        payload = {
            "model_name": model_name,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "mode": mode
        }

        # 特定模型参数处理：kling-v2.x 不支持 cfg_scale
        if "kling-v2" not in model_name:
            payload["cfg_scale"] = cfg_scale

        # 如果有运镜控制，添加到请求体
        if camera_control:
            payload["camera_control"] = camera_control

        try:
            response = self.session.post(
                url,
                headers=self._get_headers(),
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                print(f"[Create] 任务提交成功，Task ID: {result['data']['task_id']}")
                return result['data']
            else:
                print(f"[Create] 提交失败: {result.get('message')}")
                return None
        except Exception as e:
            print(f"[Create] 请求异常: {e}")
            return None

    def get_task_details(self, task_id):
        """
        查询单个任务详情
        """
        # 根据文档，task_id 直接拼在 URL 路径中
        url = f"{self.base_url}/v1/videos/text2video/{task_id}"
        
        try:
            response = self.session.get(
                url,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                return result['data']
            else:
                print(f"[Query] 查询失败: {result.get('message')}")
                return None
        except Exception as e:
            print(f"[Query] 请求异常: {e}")
            return None

    def wait_for_completion(self, task_id, check_interval=5):
        """
        辅助函数：轮询直到任务完成或失败
        """
        print(f"正在等待任务 {task_id} 完成...", end="", flush=True)
        failure_count = 0
        while True:
            task_data = self.get_task_details(task_id)
            if not task_data:
                failure_count += 1
                if failure_count >= 5:
                    print("\n❌ 多次请求异常，已停止轮询")
                    break
                print(".", end="", flush=True)
                time.sleep(check_interval)
                continue
            
            status = task_data.get("task_status")
            
            if status == "succeed":
                print("\n✅ 视频生成成功！")
                video_url = task_data["task_result"]["videos"][0]["url"]
                print(f"视频下载地址: {video_url}")
                return task_data
            elif status == "failed":
                print(f"\n❌ 视频生成失败: {task_data.get('task_status_msg')}")
                return task_data
            else:
                # 状态为 submitted 或 processing
                print(".", end="", flush=True)
                time.sleep(check_interval)

# --- 使用示例 ---

if __name__ == "__main__":
    # 1. 配置您的鉴权信息
    AK = "Ab4RpChdhNpC8QnD4gYB9r8JMYHFR9ge"
    SK = "bN4y9DyETkTJQCPEmN3hHyR8MKe9FRKh"

    if AK == "YOUR_ACCESS_KEY":
        print("请先在代码中填入您的 AccessKey 和 SecretKey")
    else:
        client = KlingVideoClient(AK, SK)

        # 2. 定义任务参数
        # 示例：使用 kling-v1 模型生成一只在海滩上奔跑的狗
        prompt_text = "A cinematic shot of a golden retriever running on a sunny beach, slow motion, 4k, high detail."
        
        # 3. 提交任务
        # 你可以修改 model_name 为 "kling-v2-5-turbo" 或其他文档支持的模型
        task_info = client.create_text2video_task(
            prompt=prompt_text,
            model_name="kling-v1",
            aspect_ratio="16:9",
            mode="std"
        )

        # 4. 如果提交成功，自动等待结果
        if task_info:
            task_id = task_info["task_id"]
            client.wait_for_completion(task_id)
