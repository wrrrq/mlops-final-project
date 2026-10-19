# HeartGuard 部署流水线说明文档

本文档详细说明了 HeartGuard 项目如何通过 GitHub Actions 实现自动化部署与镜像构建。

# 环境变量与安全（GitHub Secrets）
为了保证生产安全，我们不将任何数据库密码或密钥以明文形式写在代码中。我们在 GitHub 仓库的 `Settings -> Secrets and variables -> Actions` 中配置了以下环境变量：
- `STAGING_ENV`: 包含 staging 环境所需的配置（如端口号、调试模式等）。
- `PROD_ENV`: 包含生产环境所需的配置（如连接池大小、生产 API 密钥等）。

在流水线运行到对应的部署阶段时，GitHub Actions 会动态读取这些 Secrets，并将它们写入构建环境中的 `.env` 文件。

# CD（持续交付）触发流程
 1. Staging 环境构建
- 触发条件：当代码成功合并到 `staging` 分支时触发。
- 流水线动作：
  1. 检出最新代码。
  2. 使用 `${{ secrets.STAGING_ENV }}` 生成 staging 专属的 `.env` 文件。
  3. 执行 `docker build -t heartguard:staging .` 构建预发布镜像。
- 目的：供团队或内测人员进行最终验证。

# 2. Production 环境构建
- 触发条件：当代码从 `staging` 分支通过 PR 合并到 `main` 分支时触发。
- 流水线动作：
  1. 检出最新代码。
  2. 使用 `${{ secrets.PROD_ENV }}` 生成生产专属的 `.env` 文件。
  3. 执行 `docker build -t heartguard:prod .` 构建最终生产镜像。
- 目的：生成最终的交付产物，随时可以推送到云服务器或 K8s 集群。

## 容错与质量保障
- 流水线配置了严格的依赖关系。如果 CI 阶段的测试（Pytest）或代码规范检查（Ruff）未通过，CD 阶段将自动终止，防止缺陷代码被构建成镜像。
- 镜像统一基于 `python:3.12-slim` 构建，并排除了 `.git`、`.venv` 等冗余文件，确保镜像轻量且安全。

