# Helper Tools Index
This document indexes available tools for the agent.

## MCP Tools
```json
{
  "timestamp": "2026-02-02T14:10:45.943099",
  "count": 2,
  "servers": [
    {
      "url": "https://mcp.alibaba-inc.com/code/mcp",
      "type": "http",
      "name": "aone-open-platform-code",
      "_source": "/root/.vscode-server-insiders/data/User/mcp.json",
      "tools": [
        {
          "name": "list_groups",
          "description": "查询用户有权限的分组列表，支持搜索和分页功能",
          "inputSchema": {
            "type": "object",
            "properties": {
              "search": {
                "type": "string",
                "description": "搜索词"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "页码，默认为1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "每一页大小，默认20"
              }
            },
            "required": []
          },
          "annotations": {}
        },
        {
          "name": "merge_branch",
          "description": "合并分支到目标分支",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "sourceRef": {
                "type": "string",
                "description": "待合并引用名称"
              },
              "targetBranch": {
                "type": "string",
                "description": "目标分支名称"
              },
              "mergeType": {
                "type": "string",
                "description": "合并类型，支持的类型有：NO_FF、FAST_FORWARD_ONLY、FAST_FORWARD、SQUASH、REBASE"
              },
              "mergeMessage": {
                "type": "string",
                "description": "合并信息，使用\"SQUASH\"合并类型时必传"
              },
              "authorName": {
                "type": "string",
                "description": "作者名称"
              },
              "authorEmail": {
                "type": "string",
                "description": "作者邮箱"
              }
            },
            "required": [
              "repo",
              "sourceRef",
              "targetBranch",
              "mergeType"
            ]
          },
          "annotations": {
            "destructiveHint": true
          }
        },
        {
          "name": "get_repo_security_level",
          "description": "批量获取仓库代码安全等级。安全等级分为：C1（公开代码）可对外开源，无敏感信息或知识产权风险；C2（内部代码）对外闭源，不涉及核心敏感业务逻辑；C3（核心代码）对外闭源，包含核心敏感业务、数据、知识产权或基础设施相关，不可使用外部AI模型进行代码操作",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repoPaths": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "仓库路径列表，比如[\"foo/bar\", \"foo/baz\"]表示多个仓库路径"
              }
            },
            "required": [
              "repoPaths"
            ]
          },
          "annotations": {}
        },
        {
          "name": "get_repo_by_path",
          "description": "根据仓库路径获取仓库基本信息，比如仓库ID，比如仓库：git@gitlab.alibaba-inc.com:foo/bar.git 的仓库路径是foo/bar",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              }
            },
            "required": [
              "repo"
            ]
          },
          "annotations": {}
        },
        {
          "name": "list_my_branches",
          "description": "查询我的分支列表",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "search": {
                "type": "string",
                "description": "搜索词"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "页码，默认为1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "每一页大小，默认20"
              }
            },
            "required": [
              "repo"
            ]
          },
          "annotations": {}
        },
        {
          "name": "list_changed_files",
          "description": "查询代码仓库分支变更文件列表",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "必传参数，仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "from": {
                "type": "string",
                "description": "Base引用名称，不限于主干分支名称，或者 merge base commit id"
              },
              "to": {
                "type": "string",
                "description": "变更引用名称，不限于变更分支名称，或者指定 commit id"
              },
              "findRenames": {
                "type": "boolean",
                "description": "是否查找重命名"
              }
            },
            "required": [
              "repo",
              "to"
            ]
          },
          "annotations": {}
        },
        {
          "name": "create_branch",
          "description": "新建分支",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "branchName": {
                "type": "string",
                "description": "分支名称"
              },
              "ref": {
                "type": "string",
                "description": "分支基线"
              }
            },
            "required": [
              "repo",
              "branchName",
              "ref"
            ]
          },
          "annotations": {}
        },
        {
          "name": "get_changed_file_diff",
          "description": "查询代码仓库变更文件diff",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "必传参数，仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "from": {
                "type": "string",
                "description": "Base引用名称，不限于主干分支名称，或者 merge base commit id"
              },
              "to": {
                "type": "string",
                "description": "变更引用名称，不限于变更分支名称，或者指定 commit id"
              },
              "oldFilePath": {
                "type": "string",
                "description": "旧文件路径"
              },
              "newFilePath": {
                "type": "string",
                "description": "新文件路径"
              }
            },
            "required": [
              "repo",
              "to",
              "oldFilePath",
              "newFilePath"
            ]
          },
          "annotations": {}
        },
        {
          "name": "list_repo_files",
          "description": "查询代码仓库文件列表",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "必传参数，仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "ref": {
                "type": "string",
                "description": "分支名称或者Commit Id"
              },
              "dirPath": {
                "type": "string",
                "description": "目录路径"
              }
            },
            "required": [
              "repo",
              "ref",
              "dirPath"
            ]
          },
          "annotations": {}
        },
        {
          "name": "get_file_blame",
          "description": "查询代码仓库文件的blame信息，显示每行代码的提交历史和作者信息，用于追踪文件中每一行的变更历史",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "必传参数，仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "ref": {
                "type": "string",
                "description": "分支名称或者Commit Id"
              },
              "filePath": {
                "type": "string",
                "description": "文件路径"
              },
              "startLine": {
                "type": "integer",
                "format": "int32",
                "description": "起始行号，不传表示所有文件行"
              },
              "endLine": {
                "type": "integer",
                "format": "int32",
                "description": "结束行号，不传表示所有文件行"
              }
            },
            "required": [
              "repo",
              "ref",
              "filePath"
            ]
          },
          "annotations": {}
        },
        {
          "name": "get_file_block",
          "description": "获取代码仓库文件指定行区间内的文件内容",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "必传参数，仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "ref": {
                "type": "string",
                "description": "分支名称或者Commit Id"
              },
              "filePath": {
                "type": "string",
                "description": "文件路径"
              },
              "startLine": {
                "type": "integer",
                "format": "int64",
                "description": "起始行号，从1开始，不传表示从第1行开始"
              },
              "endLine": {
                "type": "integer",
                "format": "int64",
                "description": "结束行号，从1开始，不传表示到文件末尾"
              }
            },
            "required": [
              "repo",
              "ref",
              "filePath"
            ]
          },
          "annotations": {}
        },
        {
          "name": "create_repository",
          "description": "创建代码仓库",
          "inputSchema": {
            "type": "object",
            "properties": {
              "group": {
                "type": "string",
                "description": "仓库分组名称"
              },
              "name": {
                "type": "string",
                "description": "仓库名称"
              },
              "description": {
                "type": "string",
                "description": "仓库描述"
              }
            },
            "required": [
              "group",
              "name"
            ]
          },
          "annotations": {}
        },
        {
          "name": "list_commits",
          "description": "获取分支或者分支+文件的提交历史，支持时间范围和分页查询",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "必传参数，仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "refName": {
                "type": "string",
                "description": "分支名称或者Commit Id，不传默认为主分支"
              },
              "path": {
                "type": "string",
                "description": "文件路径，可选，用于获取特定文件的提交历史"
              },
              "since": {
                "type": "string",
                "format": "date-time",
                "description": "开始时间，可选，格式：2025-06-03T14:25:30.000+08:00"
              },
              "until": {
                "type": "string",
                "format": "date-time",
                "description": "结束时间，可选，格式：2025-06-03T14:25:30.000+08:00"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "页码，默认为0"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "每页大小，默认为20"
              }
            },
            "required": [
              "repo"
            ]
          },
          "annotations": {}
        },
        {
          "name": "edit_repo_files",
          "description": "批量编辑文件，支持代码仓库文件的创建、更新、删除和移动位置",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "commitFilesInputDTO": {
                "type": "object",
                "properties": {
                  "actions": {
                    "description": "(required) - Commit actions",
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "action": {
                          "type": "string",
                          "description": "(required) - Commit action (create | update | move | delete), eg. if you want to create a file, use \"create\""
                        },
                        "fileContent": {
                          "type": "string",
                          "description": "(optional) - content, raw file content or base64 encoded string of content. If the encoding is not 'text', then the content must be encoded using Base64."
                        },
                        "fileContentEncoding": {
                          "type": "string",
                          "description": "(optional) - 'text' or 'base64'. text is default."
                        },
                        "filePath": {
                          "type": "string",
                          "description": "(optional) - Full path to new file, use relative paths instead of absolute paths."
                        },
                        "previousPath": {
                          "type": "string",
                          "description": "(optional) - Full path to old file, use relative paths instead of absolute paths."
                        }
                      },
                      "required": [
                        "action"
                      ]
                    }
                  },
                  "authorEmail": {
                    "type": "string",
                    "description": "(optional) - Author email"
                  },
                  "authorName": {
                    "type": "string",
                    "description": "(optional) - Author name"
                  },
                  "branchName": {
                    "type": "string",
                    "description": "(required) - The name of branch"
                  },
                  "commitMessage": {
                    "type": "string",
                    "description": "(required) - Commit message"
                  }
                },
                "required": [
                  "actions",
                  "branchName",
                  "commitMessage"
                ],
                "description": "具体修改内容，使用json格式"
              }
            },
            "required": [
              "repo",
              "commitFilesInputDTO"
            ]
          },
          "annotations": {
            "destructiveHint": true
          }
        },
        {
          "name": "delete_branch",
          "description": "删除分支，此操作属于危险操作，执行前请先让用户确认，用户同意后再执行",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "branchName": {
                "type": "string",
                "description": "分支名称"
              }
            },
            "required": [
              "repo",
              "branchName"
            ]
          },
          "annotations": {
            "destructiveHint": true
          }
        },
        {
          "name": "get_me",
          "description": "获取当前登录用户基本信息，比如用户名，花名，邮箱，工号等",
          "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
          },
          "annotations": {}
        },
        {
          "name": "get_single_file",
          "description": "查询代码仓库单个文件指定版本的内容",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "必传参数，仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "ref": {
                "type": "string",
                "description": "分支名称或者Commit Id"
              },
              "filePath": {
                "type": "string",
                "description": "文件路径"
              },
              "sizeLimit": {
                "type": "integer",
                "format": "int64",
                "description": "文件大小限制"
              }
            },
            "required": [
              "repo",
              "ref",
              "filePath"
            ]
          },
          "annotations": {}
        },
        {
          "name": "create_tag",
          "description": "创建代码仓库标签",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "tagName": {
                "type": "string",
                "description": "标签名称"
              },
              "ref": {
                "type": "string",
                "description": "标签关联的分支或者commit"
              },
              "message": {
                "type": "string",
                "description": "标签描述"
              },
              "releaseDescription": {
                "type": "string",
                "description": "标签发布描述"
              }
            },
            "required": [
              "repo",
              "tagName",
              "ref",
              "message"
            ]
          },
          "annotations": {}
        },
        {
          "name": "get_issue",
          "description": "获取 Issue 详情和评论列表",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "issueId": {
                "type": "integer",
                "format": "int64",
                "description": "Issue ID，示例：12345、67890、100001"
              }
            },
            "required": [
              "repo",
              "issueId"
            ]
          },
          "annotations": {}
        },
        {
          "name": "list_issues",
          "description": "查询 Issue 列表，支持简单搜索和分页",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "types": {
                "type": "string",
                "description": "Issue 类型过滤条件，支持多个类型同时筛选。多个类型用英文逗号分隔，支持的类型：REQ（需求）、BUG（缺陷）。示例：\"REQ,BUG\" 表示查询需求和缺陷类型的Issue"
              },
              "statuses": {
                "type": "string",
                "description": "Issue 状态过滤条件，支持多个状态同时筛选。多个状态用英文逗号分隔，支持的状态：new/待处理、assigned/进行中、fixed/已完成、wontfix/已取消。示例：\"new,assigned\" 表示查询待处理和进行中状态的Issue"
              },
              "assigneeNickName": {
                "type": "string",
                "description": "指派人花名，示例：\"张三\""
              },
              "creatorNickName": {
                "type": "string",
                "description": "创建人花名，示例：\"王五\""
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "页码，从1开始，默认为1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "每页大小，默认为20，最大100"
              },
              "mineCreated": {
                "type": "boolean",
                "description": "是否仅查看我创建的"
              },
              "mineAssigned": {
                "type": "boolean",
                "description": "是否仅查看分配给我的"
              }
            },
            "required": [
              "repo"
            ]
          },
          "annotations": {}
        },
        {
          "name": "create_issue",
          "description": "创建新的 Issue",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "title": {
                "type": "string",
                "description": "Issue 标题，示例：\"修复登录页面显示问题\"、\"新增用户管理功能\""
              },
              "issueType": {
                "type": "string",
                "description": "Issue 类型，支持的类型：REQ（需求）、BUG（缺陷）。示例：\"REQ\"、\"BUG\""
              },
              "description": {
                "type": "string",
                "description": "Issue 描述内容，可选参数"
              },
              "assigneeNickName": {
                "type": "string",
                "description": "指派人花名，示例：\"张三\"，可选参数"
              }
            },
            "required": [
              "repo",
              "title",
              "issueType"
            ]
          },
          "annotations": {}
        },
        {
          "name": "update_issue_status",
          "description": "更新 Issue 状态。必填参数：repo, issueId, status；status 可选值（不区分大小写，支持中英文同义词）：new/待处理、assigned/进行中、done/已完成、cancel/已取消",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "issueId": {
                "type": "integer",
                "format": "int64",
                "description": "Issue ID，示例：12345、67890、100001"
              },
              "status": {
                "type": "string",
                "description": "目标状态，示例：\"new\"、\"assigned\"、\"done\"、\"cancel\""
              }
            },
            "required": [
              "repo",
              "issueId",
              "status"
            ]
          },
          "annotations": {}
        },
        {
          "name": "create_issue_comment",
          "description": "为 Issue 添加评论",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "issueId": {
                "type": "integer",
                "format": "int64",
                "description": "Issue ID，示例：12345、67890、100001"
              },
              "content": {
                "type": "string",
                "description": "评论内容，示例：\"这个问题已经修复了\"、\"需要进一步确认\""
              }
            },
            "required": [
              "repo",
              "issueId",
              "content"
            ]
          },
          "annotations": {}
        },
        {
          "name": "list_repo_merge_requests_created_by_me",
          "description": "查询我创建的代码仓库代码评审MR列表，可以根据仓库ID，搜索词，代码评审状态等查询代码评审列表",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "search": {
                "type": "string",
                "description": "搜索词"
              },
              "state": {
                "type": "string",
                "description": "代码评审状态过滤条件。可选值：opened（评审中）、accepted（已通过）、merged（已合并）。默认为opened"
              },
              "sourceBranch": {
                "type": "string",
                "description": "查询关联指定变更分支的代码评审列表"
              },
              "targetBranch": {
                "type": "string",
                "description": "查询关联指定目标分支的代码评审列表"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "页码，默认为1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "页大小，默认为20"
              }
            },
            "required": [
              "repo"
            ]
          },
          "annotations": {}
        },
        {
          "name": "list_merge_requests_reviewed_by_me",
          "description": "全局查询我评审的代码评审MR列表，可以根据搜索词，代码评审状态等查询代码评审列表",
          "inputSchema": {
            "type": "object",
            "properties": {
              "search": {
                "type": "string",
                "description": "搜索词"
              },
              "state": {
                "type": "string",
                "description": "代码评审状态过滤条件。可选值：opened（评审中）、accepted（已通过）、merged（已合并）。默认为opened"
              },
              "targetBranch": {
                "type": "string",
                "description": "查询关联指定目标分支的代码评审列表"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "页码，默认为1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "页大小，默认为20"
              }
            },
            "required": []
          },
          "annotations": {}
        },
        {
          "name": "list_repo_merge_requests_reviewed_by_me",
          "description": "查询我评审的代码仓库代码评审MR列表，可以根据仓库ID，搜索词，代码评审状态等查询代码评审列表",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "search": {
                "type": "string",
                "description": "搜索词"
              },
              "state": {
                "type": "string",
                "description": "代码评审状态过滤条件。可选值：opened（评审中）、accepted（已通过）、merged（已合并）。默认为opened"
              },
              "sourceBranch": {
                "type": "string",
                "description": "查询关联指定变更分支的代码评审列表"
              },
              "targetBranch": {
                "type": "string",
                "description": "查询关联指定目标分支的代码评审列表"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "页码，默认为1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "页大小，默认为20"
              }
            },
            "required": [
              "repo"
            ]
          },
          "annotations": {}
        },
        {
          "name": "list_merge_requests_created_by_me",
          "description": "全局查询我创建的代码评审MR列表，可以根据搜索词，代码评审状态等查询代码评审列表",
          "inputSchema": {
            "type": "object",
            "properties": {
              "search": {
                "type": "string",
                "description": "搜索词"
              },
              "state": {
                "type": "string",
                "description": "代码评审状态过滤条件。可选值：opened（评审中）、accepted（已通过）、merged（已合并）。默认为opened"
              },
              "targetBranch": {
                "type": "string",
                "description": "查询关联指定目标分支的代码评审列表"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "页码，默认为1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "页大小，默认为20"
              }
            },
            "required": []
          },
          "annotations": {}
        },
        {
          "name": "comment_merge_request_code_suggestion",
          "description": "在代码评审（MR）变更的文件上发表代码建议评论",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "代码评审（MR）ID"
              },
              "comment": {
                "type": "string",
                "description": "评论内容"
              },
              "suggestion": {
                "type": "string",
                "description": "建议替换成的新代码内容"
              },
              "path": {
                "type": "string",
                "description": "变更文件路径"
              },
              "startLine": {
                "type": "integer",
                "format": "int64",
                "description": "变更文件开始行号"
              },
              "endLine": {
                "type": "integer",
                "format": "int64",
                "description": "变更文件结束行号，如果是单行建议则与开始行号相同"
              }
            },
            "required": [
              "repo",
              "mergeRequestId",
              "comment",
              "suggestion",
              "path",
              "startLine"
            ]
          },
          "annotations": {}
        },
        {
          "name": "list_merge_request_changed_files",
          "description": "查询代码评审（MR）上变更的文件列表",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "代码评审（MR）ID"
              }
            },
            "required": [
              "repo",
              "mergeRequestId"
            ]
          },
          "annotations": {}
        },
        {
          "name": "get_merge_request_changed_file_diff",
          "description": "查询代码仓库变更文件diff",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "代码评审（MR）ID"
              },
              "oldPath": {
                "type": "string",
                "description": "文件旧路径"
              },
              "newPath": {
                "type": "string",
                "description": "文件新路径"
              }
            },
            "required": [
              "repo",
              "mergeRequestId",
              "oldPath",
              "newPath"
            ]
          },
          "annotations": {}
        },
        {
          "name": "update_merge_request_comment_status",
          "description": "更新代码评审（MR）评论状态",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "代码评审（MR）ID"
              },
              "noteId": {
                "type": "integer",
                "format": "int64",
                "description": "评论ID"
              },
              "closed": {
                "type": "integer",
                "format": "int32",
                "description": "评论状态，0-未解决，1-已解决。默认为0（未解决）"
              }
            },
            "required": [
              "repo",
              "mergeRequestId",
              "noteId"
            ]
          },
          "annotations": {}
        },
        {
          "name": "create_merge_request",
          "description": "根据用户提供的仓库ID，关联分支，标题和描述创建代码评审",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "sourceBranch": {
                "type": "string",
                "description": "关联变更分支"
              },
              "targetBranch": {
                "type": "string",
                "description": "关联目标分支"
              },
              "title": {
                "type": "string",
                "description": "代码评审标题"
              },
              "description": {
                "type": "string",
                "description": "代码评审描述"
              },
              "assignees": {
                "type": "string",
                "description": "评审人花名，多个以逗号(,)分隔"
              },
              "assigneeStaffIds": {
                "type": "string",
                "description": "评审人工号列表，多个以逗号(,)分隔"
              }
            },
            "required": [
              "repo",
              "sourceBranch",
              "targetBranch",
              "title"
            ]
          },
          "annotations": {}
        },
        {
          "name": "list_repo_merge_requests",
          "description": "查询代码仓库代码评审MR列表，可以根据仓库ID，搜索词，代码评审状态等查询代码评审列表",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "search": {
                "type": "string",
                "description": "搜索词"
              },
              "state": {
                "type": "string",
                "description": "代码评审状态过滤条件。可选值：opened（评审中）、accepted（已通过）、merged（已合并）。默认为opened"
              },
              "sourceBranch": {
                "type": "string",
                "description": "查询关联指定变更分支的代码评审列表"
              },
              "targetBranch": {
                "type": "string",
                "description": "查询关联指定目标分支的代码评审列表"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "页码，默认为1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "页大小，默认为20"
              }
            },
            "required": [
              "repo"
            ]
          },
          "annotations": {}
        },
        {
          "name": "get_merge_request_detail",
          "description": "查询代码评审（MR）详情",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "代码评审（MR）ID"
              }
            },
            "required": [
              "repo",
              "mergeRequestId"
            ]
          },
          "annotations": {}
        },
        {
          "name": "comment_merge_request_changed_file",
          "description": "在代码评审（MR）变更的文件上发表行评论",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "代码评审（MR）ID"
              },
              "note": {
                "type": "string",
                "description": "评论内容"
              },
              "path": {
                "type": "string",
                "description": "变更文件路径"
              },
              "line": {
                "type": "integer",
                "format": "int64",
                "description": "变更文件行号"
              }
            },
            "required": [
              "repo",
              "mergeRequestId",
              "note",
              "path",
              "line"
            ]
          },
          "annotations": {}
        },
        {
          "name": "list_merge_request_comments",
          "description": "获取代码评审（MR）评论列表",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "代码评审（MR）ID"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "页码，默认为1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "页大小，默认为20"
              }
            },
            "required": [
              "repo",
              "mergeRequestId"
            ]
          },
          "annotations": {}
        },
        {
          "name": "delete_merge_request_comment",
          "description": "删除代码评审（MR）评论",
          "inputSchema": {
            "type": "object",
            "properties": {
              "noteId": {
                "type": "integer",
                "format": "int64",
                "description": "评论ID"
              }
            },
            "required": [
              "noteId"
            ]
          },
          "annotations": {
            "destructiveHint": true
          }
        },
        {
          "name": "remind_merge_request_assignees",
          "description": "提醒代码评审评审人评审代码评审",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "代码评审（MR）ID"
              }
            },
            "required": [
              "repo",
              "mergeRequestId"
            ]
          },
          "annotations": {}
        },
        {
          "name": "list_merge_request_commits",
          "description": "查询代码评审（MR）的提交列表",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "代码评审（MR）ID"
              }
            },
            "required": [
              "repo",
              "mergeRequestId"
            ]
          },
          "annotations": {}
        },
        {
          "name": "accept_merge_request",
          "description": "通过代码评审（MR）",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "代码评审（MR）ID"
              }
            },
            "required": [
              "repo",
              "mergeRequestId"
            ]
          },
          "annotations": {}
        },
        {
          "name": "merge_merge_request",
          "description": "合并代码评审（MR）",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "代码评审（MR）ID"
              },
              "mergeType": {
                "type": "string",
                "description": "合并类型，可选ff，ff-only，no-fast-forward，squash，rebase，rebase-with-message，rebase-and-no-fast-forward"
              },
              "mergeMessage": {
                "type": "string",
                "description": "合并提交信息"
              },
              "removeSourceBranch": {
                "type": "boolean",
                "description": "是否移除源分支"
              }
            },
            "required": [
              "repo",
              "mergeRequestId"
            ]
          },
          "annotations": {}
        },
        {
          "name": "update_merge_request",
          "description": "更新代码评审（MR）标题和描述",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "代码评审（MR）ID"
              },
              "title": {
                "type": "string",
                "description": "代码评审标题，字符串长度需小于128"
              },
              "description": {
                "type": "string",
                "description": "代码评审描述，字符串长度需小于100000"
              }
            },
            "required": [
              "repo",
              "mergeRequestId"
            ]
          },
          "annotations": {}
        },
        {
          "name": "list_merge_request_ci_tasks",
          "description": "获取代码评审关联CI任务详情列表",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "代码评审（MR）ID"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "页码，默认为1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "页大小，默认为20"
              }
            },
            "required": [
              "repo",
              "mergeRequestId"
            ]
          },
          "annotations": {}
        },
        {
          "name": "comment_merge_request",
          "description": "在代码评审（MR）上发表全局评论",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "代码评审（MR）ID"
              },
              "note": {
                "type": "string",
                "description": "评论内容"
              }
            },
            "required": [
              "repo",
              "mergeRequestId",
              "note"
            ]
          },
          "annotations": {}
        },
        {
          "name": "repo_vector_search",
          "description": "在代码仓库中根据语义搜索主干分支代码",
          "inputSchema": {
            "type": "object",
            "properties": {
              "question": {
                "type": "string",
                "description": "搜索问题"
              },
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径"
              },
              "limit": {
                "type": "integer",
                "format": "int32",
                "description": "返回结果数量限制，默认为10"
              }
            },
            "required": [
              "question",
              "repo"
            ]
          },
          "annotations": {}
        },
        {
          "name": "search_classes",
          "description": "搜索参与的仓库或指定仓库内的类",
          "inputSchema": {
            "type": "object",
            "properties": {
              "search": {
                "type": "string",
                "description": "搜索关键词"
              },
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径，如不提供则搜索所有参与的仓库"
              },
              "fileName": {
                "type": "string",
                "description": "文件名，搜索指定文件内的类"
              },
              "page": {
                "type": "integer",
                "format": "int32",
                "description": "页码，默认为1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int32",
                "description": "每页大小，默认为5"
              }
            },
            "required": [
              "search"
            ]
          },
          "annotations": {}
        },
        {
          "name": "search_code",
          "description": "搜索参与的仓库或指定仓库内的代码片段和代码文件元数据",
          "inputSchema": {
            "type": "object",
            "properties": {
              "search": {
                "type": "string",
                "description": "搜索关键词"
              },
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径，如不提供则搜索所有参与的仓库"
              },
              "lang": {
                "type": "string",
                "description": "编程语言过滤，如：Java，JavaScript，C，C++，TypeScript，Go，Python"
              },
              "page": {
                "type": "integer",
                "format": "int32",
                "description": "页码，默认为1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int32",
                "description": "每页大小，默认为5"
              }
            },
            "required": [
              "search"
            ]
          },
          "annotations": {}
        },
        {
          "name": "search_methods",
          "description": "搜索参与的仓库或指定仓库内的方法",
          "inputSchema": {
            "type": "object",
            "properties": {
              "search": {
                "type": "string",
                "description": "搜索关键词"
              },
              "repo": {
                "type": "string",
                "description": "仓库路径，比如\"foo/bar\"是仓库\"git@gitlab.alibaba-inc.com:foo/bar.git\"的仓库路径，如不提供则搜索所有参与的仓库"
              },
              "fileName": {
                "type": "string",
                "description": "文件名，搜索指定文件内的方法"
              },
              "page": {
                "type": "integer",
                "format": "int32",
                "description": "页码，默认为1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int32",
                "description": "每页大小，默认为5"
              }
            },
            "required": [
              "search"
            ]
          },
          "annotations": {}
        }
      ],
      "tools_count": 48
    },
    {
      "url": "https://mcp.alibaba-inc.com/aone-km/mcp",
      "type": "http",
      "name": "aone-open-platform-knowledge-base",
      "_source": "/root/.vscode-server-insiders/data/User/mcp.json",
      "tools": [
        {
          "name": "searchCodeWiki",
          "description": "在 CodeWiki 中进行语义搜索，支持跨多个代码仓库搜索。返回按相关性排序的搜索结果。",
          "inputSchema": {
            "type": "object",
            "properties": {
              "codeRepoNames": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "代码仓库名称列表，格式 group/project，最多 20 个"
              },
              "query": {
                "type": "string",
                "description": "搜索查询语句"
              },
              "top": {
                "type": "integer",
                "format": "int32",
                "description": "返回结果数量，默认 10，最大 50"
              },
              "includeContent": {
                "type": "boolean",
                "description": "是否返回完整页面内容，默认 false"
              },
              "scoreThreshold": {
                "type": "number",
                "format": "double",
                "description": "相关性分数阈值 0-1，低于该值的结果将被过滤"
              }
            },
            "required": [
              "codeRepoNames",
              "query"
            ]
          },
          "annotations": {}
        },
        {
          "name": "getCodeWikiPageContent",
          "description": "获取 CodeWiki 指定页面的完整内容。返回页面标题、Markdown 内容和元数据信息。",
          "inputSchema": {
            "type": "object",
            "properties": {
              "codeRepoName": {
                "type": "string",
                "description": "代码仓库名称，格式 group/project"
              },
              "pageId": {
                "type": "string",
                "description": "页面 ID（来自 getCodeWikiStructure 的 pageId / searchCodeWiki 的 pageId；不要传 uuid）"
              }
            },
            "required": [
              "codeRepoName",
              "pageId"
            ]
          },
          "annotations": {}
        },
        {
          "name": "getCodeWikiStructure",
          "description": "获取代码仓库的 CodeWiki 目录结构。默认仅返回当前层级，必要时可递归返回目录树。",
          "inputSchema": {
            "type": "object",
            "properties": {
              "codeRepoName": {
                "type": "string",
                "description": "代码仓库名称，格式 group/project"
              },
              "parentUuid": {
                "type": "string",
                "description": "父节点 UUID，不传则从根目录开始"
              },
              "recursive": {
                "type": "boolean",
                "description": "是否递归获取子节点，默认 false"
              },
              "maxDepth": {
                "type": "integer",
                "format": "int32",
                "description": "最大递归深度，默认 10，最大 10（仅 recursive=true 时生效）"
              },
              "format": {
                "type": "string",
                "description": "返回格式：tree(默认) / json"
              }
            },
            "required": [
              "codeRepoName"
            ]
          },
          "annotations": {}
        },
        {
          "name": "createDingDocWorkspaceDoc",
          "description": "在钉钉知识库中新建文件夹或文档，支持在创建文档的同时写入 markdown 内容",
          "inputSchema": {
            "type": "object",
            "properties": {
              "workspaceId": {
                "type": "string",
                "description": "知识库ID，即钉钉知识库的空间ID（可从钉钉知识库首页链接中获取，如 https://alidocs.dingtalk.com/i/spaces/abcd/overview 中的 abcd"
              },
              "docType": {
                "type": "string",
                "description": "文档类型，只能填写以下两个值之一：DOC（文字文档）或 FOLDER（文件夹），默认为 DOC"
              },
              "name": {
                "type": "string",
                "description": "文档或目录的名称，不能为空"
              },
              "parentNodeId": {
                "type": "string",
                "description": "父节点ID（目录节点的唯一标识符，可先通过 fetchKnowledgeDirectoryByUrl 工具获取到目录列表，然后获取到目录节点的 uuid），如果不指定则默认创建在根目录下"
              },
              "content": {
                "type": "string",
                "description": "文档内容（markdown 格式），仅当 docType 为 DOC 时有效，如果不指定则创建空文档"
              }
            },
            "required": [
              "workspaceId",
              "name"
            ]
          },
          "annotations": {}
        },
        {
          "name": "updateDingDocContent",
          "description": "向钉钉文档覆写内容（会替换文档的全部内容, 只提供 markdown 格式内容写入）",
          "inputSchema": {
            "type": "object",
            "properties": {
              "docKey": {
                "type": "string",
                "description": "文档的唯一标识符（以 https://alidocs.dingtalk.com/i/nodes/abcd1234 为例， abcd1234 即为文档的唯一标识符）"
              },
              "content": {
                "type": "string",
                "description": "要写入的文档内容（markdown 格式）"
              }
            },
            "required": [
              "docKey",
              "content"
            ]
          },
          "annotations": {}
        },
        {
          "name": "askDevOpsKnowledge",
          "description": "通过自然语言提问关于阿里巴巴集团内中间件、研发运维平台相关问题，可以回答使用方法、功能介绍、接入方式、SDK代码片段、问题排查思路等",
          "inputSchema": {
            "type": "object",
            "properties": {
              "question": {
                "type": "string",
                "description": "自然语言提问，例如关于某个中间件如何使用、功能介绍、接入方式等等"
              }
            },
            "required": [
              "question"
            ]
          },
          "annotations": {}
        },
        {
          "name": "searchDevOpsKnowledge",
          "description": "通过自然语言提问关于阿里巴巴集团内中间件、研发运维平台相关问题，可以查询到使用方法、功能介绍、接入方式、SDK代码片段、问题排查思路等",
          "inputSchema": {
            "type": "object",
            "properties": {
              "question": {
                "type": "string",
                "description": "自然语言提问，例如关于某个中间件如何使用、功能介绍、接入方式等等"
              }
            },
            "required": [
              "question"
            ]
          },
          "annotations": {}
        },
        {
          "name": "chatWithKnowledgeBase",
          "description": "基于知识库的智能问答，通过 ReAct 模式进行多轮推理和文档检索，返回带有文档引用的完整回答。适用于需要深度理解和多步推理的复杂问题。",
          "inputSchema": {
            "type": "object",
            "properties": {
              "question": {
                "type": "string",
                "description": "用户的问题，例如：如何接入 HSF 服务？"
              },
              "pageRepoId": {
                "type": "string",
                "description": "知识库 ID，多个用逗号分隔，例如 \"1,2,3\"。如果不指定则使用用户有权限的所有知识库"
              },
              "pageGroupId": {
                "type": "string",
                "description": "知识组 ID，多个用逗号分隔，例如 \"1,2,3\""
              },
              "chatSessionId": {
                "type": "string",
                "description": "会话 ID，用于多轮对话。首次对话可不传，系统会自动创建新会话"
              },
              "topK": {
                "type": "integer",
                "format": "int32",
                "description": "单次文档召回工具的检索数量，默认 40"
              },
              "skipFinalAnswer": {
                "type": "boolean",
                "description": "是否跳过最终回答生成，直接返回文档内容列表。设置为 true 时，将跳过流式输出总结部分，直接返回检索到的文档内容，让用户自行总结。默认 false"
              }
            },
            "required": [
              "question"
            ]
          },
          "annotations": {}
        },
        {
          "name": "searchDocChunk",
          "description": "通过自然语言召回符合问题答案的文档片段列表",
          "inputSchema": {
            "type": "object",
            "properties": {
              "query": {
                "type": "string",
                "description": "用户提出的问题，如 Aone 是什么"
              },
              "repoIds": {
                "type": "array",
                "items": {
                  "type": "integer",
                  "format": "int32"
                },
                "description": "需要查询的知识库 ID 列表，支持单个或多个知识库 ID，例如 [82] 或 [1, 2]"
              },
              "topK": {
                "type": "integer",
                "format": "int32",
                "description": "在检索结果中返回的最相似的 k 个项目或文档， 如 20"
              },
              "instruction": {
                "type": "string",
                "description": "给予AI模型的具体指令或任务描述，告诉模型应该执行什么操作或如何回应，如扮演一个知识库内容问答专家"
              },
              "rerankInstruction": {
                "type": "string",
                "description": "用于指导 Rerank 模型对召回结果进行重新排序的自然语言指令，例如指定文档内容的相关性标准"
              },
              "scoreThreshold": {
                "type": "number",
                "format": "double",
                "description": "Rerank 模型生成的分数阈值，低于该值的召回结果将被过滤，例如设置为 0.0 表示不过滤任何结果"
              },
              "groupIds": {
                "type": "array",
                "items": {
                  "type": "integer",
                  "format": "int32"
                },
                "description": "需要查询的知识组 ID 列表，支持单个或多个知识组 ID，例如 [82] 或 [1, 2]"
              },
              "mode": {
                "type": "string",
                "description": "检索模式：preciseRetrieval - 精确检索，retrievalUserKnowledge - 权重检索（优先检索 repoIds，再检索用户有权限访问的全部知识库，包括公开知识；如果 repoIds 为空，则检索用户有权限访问的全部知识库，包括公开知识）"
              },
              "summary": {
                "type": "boolean",
                "description": "是否生成文档搜索结果的总结"
              },
              "recallLimit": {
                "type": "integer",
                "format": "int32",
                "description": "指定粗排阶段召回的文本片段数量，可以为空"
              },
              "tags": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "指定文档的标签，可以为空"
              }
            },
            "required": [
              "query",
              "topK"
            ]
          },
          "annotations": {}
        },
        {
          "name": "fetchExternalContentByUrl",
          "description": "通过钉钉或者语雀文档链接获取文档内容，如果获取不到内容，请检查知识库是否完成授权，如果知识库未完成授权，请访问链接进行授权检测",
          "inputSchema": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "description": "文档链接，支持语雀域名（aliyuque.antfin.com、yuque.antfin-inc.com、yuque.antfin.com、yuque.alibaba-inc.com）和钉钉域名（alidocs.dingtalk.com）"
              }
            },
            "required": [
              "url"
            ]
          },
          "annotations": {}
        },
        {
          "name": "fetchKnowledgeDirectoryByUrl",
          "description": "通过钉钉或者语雀知识库链接获取知识库的目录列表，如果获取不到内容，请检查知识库是否完成授权，如果知识库未完成授权，请访问链接进行授权检测",
          "inputSchema": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "description": "知识库链接，支持语雀域名（aliyuque.antfin.com、yuque.antfin-inc.com、yuque.antfin.com、yuque.alibaba-inc.com）和钉钉域名（alidocs.dingtalk.com），钉钉知识库链接示例：https://alidocs.dingtalk.com/i/spaces/xxx/overview，语雀知识库链接示例：https://aliyuque.antfin.com/team/repo"
              },
              "parentUuid": {
                "type": "string",
                "description": "父节点UUID（钉钉知识库专用），用于指定从哪个节点开始获取目录。如果不指定则从根目录开始。注意：此参数仅对钉钉知识库生效，语雀知识库会忽略此参数"
              },
              "recursive": {
                "type": "boolean",
                "description": "是否递归获取子目录（钉钉知识库专用）。true：递归获取所有子目录；false：只获取一层子目录。默认为 true。注意：此参数仅对钉钉知识库生效，语雀知识库会忽略此参数"
              }
            },
            "required": [
              "url"
            ]
          },
          "annotations": {}
        },
        {
          "name": "uploadDocToKbRepo",
          "description": "上传 Markdown 文档到平台知识库，支持指定目录路径或父节点",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repoId": {
                "type": "integer",
                "format": "int64",
                "description": "知识库ID，即平台知识库的 repoId"
              },
              "content": {
                "type": "string",
                "description": "文档内容（markdown 格式）"
              },
              "fileName": {
                "type": "string",
                "description": "文档名称，如：我的文档.md"
              },
              "dirNamePath": {
                "type": "string",
                "description": "目录路径，如：/技术文档/前端，如果不指定则创建在根目录"
              },
              "parentUuid": {
                "type": "string",
                "description": "父节点UUID，用于直接挂载到指定目录节点下，与 dirNamePath 二选一"
              }
            },
            "required": [
              "repoId",
              "content",
              "fileName"
            ]
          },
          "annotations": {}
        }
      ],
      "tools_count": 12
    }
  ],
  "note": "This list represents configured MCP servers. 'tools' field populated for HTTP servers if reachable."
}
```

## System Binaries
Standard executables in PATH (checked via 'command -v' or 'which').

## Shell Environment
Active environment variables and shell functions.

## Project Scripts
Automation scripts located in the project 'scripts/' directory.
