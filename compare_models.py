from anomalib.data import MVTecAD
from anomalib.models import Patchcore, EfficientAd
from anomalib.engine import Engine

def train_and_test(model_name, model):
    print(f"\n🚀 正在测试模型: {model_name} ...")
    datamodule = MVTecAD(root="./datasets", category="metal_nut", train_batch_size=1, eval_batch_size=1)
    engine = Engine(max_epochs=20, accelerator="gpu", devices=1) # EfficientAD 稍微多训几轮效果更好，这里为了演示先设1
    
    engine.fit(datamodule=datamodule, model=model)
    results = engine.test(datamodule=datamodule, model=model)
    print(f"✅ {model_name} 测试完成！")
    return results

def main():
    # 1. 跑 PatchCore (重型坦克，精度高，速度慢)
    print("--- 实验组 1 ---")
    train_and_test("PatchCore", Patchcore(backbone="wide_resnet50_2"))

    # 2. 跑 EfficientAD (轻型跑车，速度极快，适合部署)
    print("--- 实验组 2 ---")
    train_and_test("EfficientAD", EfficientAd())

if __name__ == "__main__":
    main() 