from log_helper import logger
import time
import random
import json

def simulate_seekey_api_workflow():
    print("--- 开始模拟 Seekey 数字化工作室 API 流 ---")

    # 1. 模拟一个 AI 图像生成接口的返回数据
    mock_api_response = {
        "status": "success",
        "data": {
            "image_url": "https://cdn.seekey.ai/v1/gen/abc12345.png",
            "seed": 987654321,
            "engine": "StableDiffusion-XL"
        },
        "meta": {
            "request_id": "req_009876",
            "compute_node": "gpu-cluster-05"
        }
    }

    # 使用计时器包裹 API 调用过程
    with logger.timer("AI_Image_Generation"):
        print(f"正在调用 AI 接口生成图像，RequestID: {mock_api_response['meta']['request_id']}...")
        
        # 模拟网络 IO 延迟
        time.sleep(random.uniform(1.0, 2.5)) 
        
        # 模拟 API 返回后，记录日志并直接传入整个 JSON 对象作为字段
        # 这正是你需要的 JSON 支持：对象会自动展开到日志的一行中
        logger.add_info(
            "图像生成任务结束", 
            api_name="Text2Image",
            response_payload=mock_api_response  # 这里直接传字典
        )

    # 2. 模拟一个带错误的 API 调用（例如：视频合成超时）
    mock_error_data = {
        "error_code": "RENDER_TIMEOUT",
        "retry_count": 3,
        "last_frame": 124
    }

    with logger.timer("Video_Rendering"):
        print("\n正在模拟视频渲染任务...")
        time.sleep(0.8)
        
        # 记录错误信息，同时附带详细的 JSON 错误上下文
        logger.add_error(
            "视频渲染失败", 
            context=mock_error_data,
            node="RenderNode-01"
        )

if __name__ == "__main__":
    simulate_seekey_api_workflow()
    print(f"\n[测试成功] 日志已按 JSON 格式写入，请检查 Logs 文件夹。")