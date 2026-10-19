# HeartGuard 部署流水线说明文档

这篇文档主要记录一下我们这个项目是怎么做环境隔离和安全部署的。

# 环境变量与安全（GitHub Secrets）
在 GitHub 仓库设置里，我们建了两个环境：`staging` 和 `production`。不管在哪个环境，密码的变量名我们都统一叫 `ENV_FILE`。但是在 `staging` 环境里，这个密码是测试用的假数据；而在 `production` 环境里，它才是真实的生产配置。这样哪怕两边配置完全不同，我们的代码也一行都不用改！

# 部署流水线是怎么跑起来的？

我们在 `.github/workflows/ci.yml` 里写好了触发规则：

1. Staging 预发布部署
   - 当代码合入 `staging` 分支时，流水线里的 `cd-staging` 任务就会被激活。
   - 它会自动去 GitHub 拿 `staging` 环境的 `ENV_FILE` 密码，在服务器上生成一个 `.env` 文件。
   - 然后执行 `docker build -t heartguard:staging .`，把代码打成一个测试版镜像。

2. Production 生产部署
   - 当我们测试没问题，把代码合入 `main` 分支时，`cd-production` 任务启动。
   - 同样的配方，它去拿 `production` 环境的密码生成 `.env`。
   - 然后打包出 `heartguard:prod` 镜像。这就是最终要交付的成品了。
