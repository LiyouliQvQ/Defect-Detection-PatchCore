import os
from anomalib.data import Folder
from anomalib.models import Patchcore
from anomalib.engine import Engine

def main():
    print("🚀 正在初始化差速器壳体视觉检测系统 (PatchCore 分割模式)...")

    # ---------------------------------------------------------
    # 1. 配置数据集 (精准匹配你左侧的文件夹结构)
    # ---------------------------------------------------------
    datamodule = Folder(
        name="differential_housing",
        root="./datasets/differential_housing", # 指向你刚刚建好的 datasets 文件夹
        normal_dir="train/good",                # 良品训练集 (建库用)
        abnormal_dir="test/bad",                # 次品测试集 (带缺陷的照片)
        normal_test_dir="test/good",            # 良品测试集 (防误报测试)
    )
    datamodule.setup()
    print("✅ 数据集挂载成功！")

    # ---------------------------------------------------------
    # 2. 初始化 PatchCore 模型
    # ---------------------------------------------------------
    model = Patchcore(
        backbone="wide_resnet50_2", 
        layers=["layer2", "layer3"],            # 提取中层和深层特征
        coreset_sampling_ratio=0.1              # 核心集采样，丢弃冗余背景特征
    )
    print("✅ 算法模型初始化完成！")

    # ---------------------------------------------------------
    # 3. 初始化引擎 (Engine)
    # ---------------------------------------------------------
    engine = Engine(
        #task="segmentation",                    # 🌟 再次确认任务类型为分割
        default_root_dir="./results"            # 跑完的结果（热力图）会自动存在这个文件夹
    )

    # ---------------------------------------------------------
    # 4. 开始建立特征库 (Training)
    # ---------------------------------------------------------
    print("\n🧠 正在提取正常壳体特征，建立记忆库... (首次运行可能需要下载预训练权重，请耐心等待)")
    engine.fit(datamodule=datamodule, model=model)
    print("✅ 记忆库构建完毕！")

    # ---------------------------------------------------------
    # 5. 测试并生成热力图 (Testing)
    # ---------------------------------------------------------
    print("\n🔍 正在测试缺陷样本，生成热力图...")
    engine.test(datamodule=datamodule, model=model)
    
    print("\n🎉 全部完成！")
    print("📂 请去 VS Code 左侧查看新生成的 results 文件夹，欣赏你的热力图吧！")

if __name__ == "__main__":
    main()