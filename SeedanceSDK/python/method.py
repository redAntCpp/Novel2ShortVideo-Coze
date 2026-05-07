import os
from volcenginesdkarkruntime import Ark

def build_full_multimodal_content(
    prompt: str, 
    images: list = None, 
    videos: list = None, 
    audios: list = None
):
    """
    全模态内容构造器。
    类比 C++: 构造一个包含多个 std::vector 的 Context 结构体。
    """
    # 初始化内容列表，放入第一个元素：文本指令
    content = [{"type": "text", "text": prompt}]

    # 1. 批量处理图片 (支持1-9张)[cite: 3, 4]
    if images:
        for url in images:
            content.append({
                "type": "image_url",
                "image_url": {"url": url},
                "role": "reference_image" # 角色定义为参考图
            })

    # 2. 批量处理视频 (支持最多3个)[cite: 3, 4]
    if videos:
        for url in videos:
            content.append({
                "type": "video_url",
                "video_url": {"url": url},
                "role": "reference_video" # 角色定义为参考视频
            })

    # 3. 批量处理音频 (支持最多3个)[cite: 3, 4]
    if audios:
        for url in audios:
            content.append({
                "type": "audio_url",
                "audio_url": {"url": url},
                "role": "reference_audio" # 角色定义为参考音频
            })

    return content

# 调用方式说明:输入提示词、图片列表、视频列表、音频列表。时长
def create_video_task(prompt: str,time: int, images: list = None, videos: list = None, audios: list = None,):
    client = Ark(
        api_key=os.environ.get("ARK_API_KEY"),
        base_url=os.environ.get("base_url"),
    )
    # 发起请求
    # generate_audio=True 表示输出带有音轨的视频[cite: 3, 4]
    resp = client.content_generation.tasks.create(
        model="doubao-seedance-2-0-260128",
        content=build_full_multimodal_content(prompt,images,videos,audios),
        generate_audio=True, 
        duration=time # 指定生成10秒视频[cite: 3, 4]
    )
    print(f"全模态任务已提交！Task ID: {resp.id}")
    return resp.id


if __name__ == "__main__":
    prompt = (
        "全程使用视频1的第一视角构图，参考图片1的人物外貌。"
        "背景音乐使用音频1，画面中的人在雪地里欢快奔跑。"
    )
    # 模拟从数据库或配置读取的 URL 列表
    my_images = ["https://example.com/face.jpg"]
    my_videos = ["https://example.com/fpv_vlog.mp4"]
    my_audios = ["https://example.com/bgm_jazz.mp3"]
    time = 2.4
    taskid = create_video_task (prompt,time,my_images,my_videos,my_audios)
    print(f"全模态任务已提交！Task ID: {taskid}")