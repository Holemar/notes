
# kubectl 日志查看

## 下载、安装
- 下载说明： https://kubernetes.io/docs/tasks/tools/install-kubectl/#kubectl-install-1
- 下载地址：  
	+ linux:   curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.20.1/bin/linux/amd64/kubectl
	+ macOs:   curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.20.1/bin/darwin/amd64/kubectl
	+ Windows: curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.20.1/bin/windows/amd64/kubectl.exe

	* 上面地址中的“v1.20.1”是版本号，下载时需要替换成最新的版本号，查询版本号地址：
	* https://storage.googleapis.com/kubernetes-release/release/stable.txt

### 让软件可执行
	`chmod +x ./kubectl`

### 移到PATH
	`sudo mv ./kubectl /usr/local/bin/kubectl`

### 测试是否可用
	`kubectl version --client`


## 语法
`kubectl [command] [TYPE] [NAME] [flags]`

+ 其中 command、TYPE、NAME 和 flags 分别是：  
	- command：指定要对一个或多个资源执行的操作，例如 create、get、describe、delete。
	- TYPE：指定资源类型。资源类型不区分大小写， 可以指定单数、复数或缩写形式。
	- NAME：指定资源的名称。名称区分大小写。 如果省略名称，则显示所有资源的详细信息 kubectl get pods。
	- flags: 指定可选的参数。例如，可以使用 -s 或 -server 参数指定 Kubernetes API 服务器的地址和端口。

+ 在对多个资源执行操作时，你可以按类型和名称指定每个资源，或指定一个或多个文件：
- 要按类型和名称指定资源：
	要对所有类型相同的资源进行分组，请执行以下操作：`TYPE1 name1 name2 name<#>`。
	例子：kubectl get pod example-pod1 example-pod2

- 分别指定多个资源类型：`TYPE1/name1 TYPE1/name2 TYPE2/name3 TYPE<#>/name<#>`。
	例子：kubectl get pod/example-pod1 replicationcontroller/example-rc1

- 用一个或多个文件指定资源：`-f file1 -f file2 -f file<#>`

- 使用 YAML 而不是 JSON 因为 YAML 更容易使用，特别是用于配置文件时。
	例子：kubectl get -f ./pod.yaml


## 操作
- 下表包含所有 kubectl 操作的简短描述和普通语法：

操作 | 语法 | 描述
-- | -- | --
alpha	|	`kubectl alpha SUBCOMMAND [flags]`	|	列出与 alpha 特性对应的可用命令，这些特性在 Kubernetes 集群中默认情况下是不启用的。
annotate	|	`kubectl annotate (-f FILENAME | TYPE NAME | TYPE/NAME) KEY_1=VAL_1 ... KEY_N=VAL_N [--overwrite] [--all] [--resource-version=version] [flags]`	|	添加或更新一个或多个资源的注解。
api-resources	|	`kubectl api-resources [flags]`	|	列出可用的 API 资源。
api-versions	|	`kubectl api-versions [flags]`	|	列出可用的 API 版本。
apply	|	`kubectl apply -f FILENAME [flags]`	|	从文件或 stdin 对资源应用配置更改。
attach	|	`kubectl attach POD -c CONTAINER [-i] [-t] [flags]`	|	附加到正在运行的容器，查看输出流或与容器（stdin）交互。
auth	|	`kubectl auth [flags] [options]`	|	检查授权。
autoscale	|	`kubectl autoscale (-f FILENAME | TYPE NAME | TYPE/NAME) [--min=MINPODS] --max=MAXPODS [--cpu-percent=CPU] [flags]`	|	自动伸缩由副本控制器管理的一组 pod。
certificate	|	`kubectl certificate SUBCOMMAND [options]`	|	修改证书资源。
cluster-info	|	`kubectl cluster-info [flags]`	|	显示有关集群中主服务器和服务的端口信息。
completion	|	`kubectl completion SHELL [options]`	|	为指定的 shell （bash 或 zsh）输出 shell 补齐代码。
config	|	`kubectl config SUBCOMMAND [flags]`	|	修改 kubeconfig 文件。有关详细信息，请参阅各个子命令。
convert	|	`kubectl convert -f FILENAME [options]`	|	在不同的 API 版本之间转换配置文件。配置文件可以是 YAML 或 JSON 格式。
cordon	|	`kubectl cordon NODE [options]`	|	将节点标记为不可调度。
cp	|	`kubectl cp <file-spec-src> <file-spec-dest> [options]`	|	在容器之间复制文件和目录。
create	|	`kubectl create -f FILENAME [flags]`	|	从文件或 stdin 创建一个或多个资源。
delete	|	`kubectl delete (-f FILENAME | TYPE [NAME | /NAME | -l label | --all]) [flags]`	|	从文件、标准输入或指定标签选择器、名称、资源选择器或资源中删除资源。
describe	|	`kubectl describe (-f FILENAME | TYPE [NAME_PREFIX | /NAME | -l label]) [flags]`	|	显示一个或多个资源的详细状态。
diff	|	`kubectl diff -f FILENAME [flags]`	|	将 live 配置和文件或标准输入做对比 (BETA)
drain	|	`kubectl drain NODE [options]`	|	腾空节点以准备维护。
edit	|	`kubectl edit (-f FILENAME | TYPE NAME | TYPE/NAME) [flags]`	|	使用默认编辑器编辑和更新服务器上一个或多个资源的定义。
exec	|	`kubectl exec POD [-c CONTAINER] [-i] [-t] [flags] [-- COMMAND [args...]]`	|	对 pod 中的容器执行命令。
explain	|	`kubectl explain [--recursive=false] [flags]`	|	获取多种资源的文档。例如 pod, node, service 等。
expose	|	`kubectl expose (-f FILENAME | TYPE NAME | TYPE/NAME) [--port=port] [--protocol=TCP|UDP] [--target-port=number-or-name] [--name=name] [--external-ip=external-ip-of-service] [--type=type] [flags]`	|	将副本控制器、服务或 pod 作为新的 Kubernetes 服务暴露。
get	|	`kubectl get (-f FILENAME | TYPE [NAME | /NAME | -l label]) [--watch] [--sort-by=FIELD] [[-o | --output]=OUTPUT_FORMAT] [flags]`	|	列出一个或多个资源。
kustomize	|	`kubectl kustomize <dir> [flags] [options]`	|	列出从 kustomization.yaml 文件中的指令生成的一组 API 资源。参数必须是包含文件的目录的路径，或者是 git 存储库 URL，其路径后缀相对于存储库根目录指定了相同的路径。
label	|	`kubectl label (-f FILENAME | TYPE NAME | TYPE/NAME) KEY_1=VAL_1 ... KEY_N=VAL_N [--overwrite] [--all] [--resource-version=version] [flags]`	|	添加或更新一个或多个资源的标签。
logs	|	`kubectl logs POD [-c CONTAINER] [--follow] [flags]`	|	在 pod 中打印容器的日志。
options	|	`kubectl options`	|	全局命令行选项列表，适用于所有命令。
patch	|	`kubectl patch (-f FILENAME | TYPE NAME | TYPE/NAME) --patch PATCH [flags]`	|	使用策略合并 patch 程序更新资源的一个或多个字段。
plugin	|	`kubectl plugin [flags] [options]`	|	提供用于与插件交互的实用程序。
port-forward	|	`kubectl port-forward POD [LOCAL_PORT:]REMOTE_PORT [...[LOCAL_PORT_N:]REMOTE_PORT_N] [flags]`	|	将一个或多个本地端口转发到一个 pod。
proxy	|	`kubectl proxy [--port=PORT] [--www=static-dir] [--www-prefix=prefix] [--api-prefix=prefix] [flags]`	|	运行 Kubernetes API 服务器的代理。
replace	|	`kubectl replace -f FILENAME`	|	从文件或标准输入中替换资源。
rollout	|	`kubectl rollout SUBCOMMAND [options]`	|	管理资源的部署。有效的资源类型包括：Deployments, DaemonSets 和 StatefulSets。
run	|	`kubectl run NAME --image=image [--env="key=value"] [--port=port] [--dry-run=server | client | none] [--overrides=inline-json] [flags]`	|	在集群上运行指定的镜像。
scale	|	`kubectl scale (-f FILENAME | TYPE NAME | TYPE/NAME) --replicas=COUNT [--resource-version=version] [--current-replicas=count] [flags]`	|	更新指定副本控制器的大小。
set	|	`kubectl set SUBCOMMAND [options]`	|	配置应用程序资源。
taint	|	`kubectl taint NODE NAME KEY_1=VAL_1:TAINT_EFFECT_1 ... KEY_N=VAL_N:TAINT_EFFECT_N [options]`	|	更新一个或多个节点上的污点。
top	|	`kubectl top [flags] [options]`	|	显示资源（CPU/内存/存储）的使用情况。
uncordon	|	`kubectl uncordon NODE [options]`	|	将节点标记为可调度。
version	|	`kubectl version [--client] [flags]`	|	显示运行在客户端和服务器上的 Kubernetes 版本。
wait	|	`kubectl wait ([-f FILENAME] | resource.group/resource.name | resource.group [(-l label | --all)]) [--for=delete|--for condition=available] [options]`	|	实验性：等待一种或多种资源的特定条件。


