# HeartGuard - 心血管疾病风险预测系统

简单来说，这是一个能用的医疗预测网页。医生在网页上输入病人的年龄、血压、胆固醇这些数据，我们的后端就会调用训练好的 AI 模型，算出来得心血管疾病的风险高不高。

# 团队分工
本项目由三人小组协作完成，模拟 DevOps 与 MLOps 流程：
- 同学 杨梦雨（App 开发与测试）：负责 FastAPI 后端接口、HTML 前端页面开发，以及核心 API 测试编写。
- 同学 王瑞麒（MLOps 与数据工程）：负责使用 DVC 管理数据版本，训练机器学习模型，并使用 MLflow 进行实验追踪。
- 同学 刘佳琪（DevOps 与 CI/CD）：负责 Git 分支规范管理、编写 Dockerfile 容器化应用、搭建 GitHub Actions 自动化流水线及文档编写。

# 技术栈
- 应用层：FastAPI, Scikit-learn, HTML
- DevOps：Git, Docker, GitHub Actions
- MLOps：DVC (Azure Blob), MLflow

# CI/CD 流水线架构与触发规则
我们用 Git 管理了 4 个层级：
`feature`（自己干活的草稿本） -> `dev`（大家一起合并的开发版） -> `staging`（预发布环境） -> `main`（最终交作业的完美版）。
以下流程图展示了代码从提交到构建的自动化旅程：

```mermaid
graph LR
    Feature[Feature 分支] -->|提交 PR| Dev(Dev 分支)
    Dev -->|PR 通过 CI 检查| Staging(Staging 分支)
    Staging -->|合并自动构建| StagingImage(Staging Docker 镜像)
    Staging -->|PR 合并| Main(Main 分支)
    Main -->|合并自动构建| ProdImage(Production Docker 镜像)


//流水线具体触发规则说明
CI 阶段（持续集成）：
触发条件：任何向 dev、staging、main 分支发起的 Pull Request (PR)。
执行动作：自动运行 Ruff 静态代码检查、Pytest 单元测试、Docker build 镜像构建测试。如果任何一步失败，PR 将被标记为红色，禁止合并。

CD 阶段（持续交付）：
触发条件：代码被正式合并（Push）到 staging 或 main 分支。
执行动作：
合并到 staging：注入 STAGING_ENV 环境变量，自动构建 heartguard:staging 镜像。
合并到 main：注入 PROD_ENV 环境变量，自动构建 heartguard:prod 生产镜像。
