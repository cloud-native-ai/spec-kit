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
          "description": "Query the list of groups the user has permission to access, with search and pagination support",
          "inputSchema": {
            "type": "object",
            "properties": {
              "search": {
                "type": "string",
                "description": "Search term"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "Page number, default is 1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "Page size, default is 20"
              }
            },
            "required": []
          },
          "annotations": {}
        },
        {
          "name": "merge_branch",
          "description": "Merge branch into target branch",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "sourceRef": {
                "type": "string",
                "description": "Source ref name to merge"
              },
              "targetBranch": {
                "type": "string",
                "description": "Target branch name"
              },
              "mergeType": {
                "type": "string",
                "description": "Merge type, supported types: NO_FF, FAST_FORWARD_ONLY, FAST_FORWARD, SQUASH, REBASE"
              },
              "mergeMessage": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"SQUASH\"[CN]"
              },
              "authorName": {
                "type": "string",
                "description": "Author name"
              },
              "authorEmail": {
                "type": "string",
                "description": "Author email"
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
          "description": "Batch retrieve repository code security levels. Security levels: C1 (Public Code) can be open-sourced externally, no sensitive info or IP risk; C2 (Internal Code) closed-source externally, does not involve core sensitive business logic; C3 (Core Code) closed-source externally, contains core sensitive business, data, IP or infrastructure, must not use external AI models for code operations",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repoPaths": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "Internal tool description (originally in Chinese)"foo/bar\", \"foo/baz\"][CN]"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "search": {
                "type": "string",
                "description": "Search term"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "Page number, default is 1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "Page size, default is 20"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "from": {
                "type": "string",
                "description": "See tool description for details"
              },
              "to": {
                "type": "string",
                "description": "See tool description for details"
              },
              "findRenames": {
                "type": "boolean",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "branchName": {
                "type": "string",
                "description": "See tool description for details"
              },
              "ref": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "from": {
                "type": "string",
                "description": "See tool description for details"
              },
              "to": {
                "type": "string",
                "description": "See tool description for details"
              },
              "oldFilePath": {
                "type": "string",
                "description": "See tool description for details"
              },
              "newFilePath": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "ref": {
                "type": "string",
                "description": "See tool description for details"
              },
              "dirPath": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "ref": {
                "type": "string",
                "description": "See tool description for details"
              },
              "filePath": {
                "type": "string",
                "description": "File path"
              },
              "startLine": {
                "type": "integer",
                "format": "int32",
                "description": "See tool description for details"
              },
              "endLine": {
                "type": "integer",
                "format": "int32",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "ref": {
                "type": "string",
                "description": "See tool description for details"
              },
              "filePath": {
                "type": "string",
                "description": "File path"
              },
              "startLine": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "endLine": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "group": {
                "type": "string",
                "description": "See tool description for details"
              },
              "name": {
                "type": "string",
                "description": "See tool description for details"
              },
              "description": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "refName": {
                "type": "string",
                "description": "See tool description for details"
              },
              "path": {
                "type": "string",
                "description": "See tool description for details"
              },
              "since": {
                "type": "string",
                "format": "date-time",
                "description": "See tool description for details"
              },
              "until": {
                "type": "string",
                "format": "date-time",
                "description": "See tool description for details"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
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
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "branchName": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
          },
          "annotations": {}
        },
        {
          "name": "get_single_file",
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "ref": {
                "type": "string",
                "description": "See tool description for details"
              },
              "filePath": {
                "type": "string",
                "description": "File path"
              },
              "sizeLimit": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "tagName": {
                "type": "string",
                "description": "See tool description for details"
              },
              "ref": {
                "type": "string",
                "description": "See tool description for details"
              },
              "message": {
                "type": "string",
                "description": "See tool description for details"
              },
              "releaseDescription": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "issueId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "types": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"REQ,BUG\" [CN]Issue"
              },
              "statuses": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"new,assigned\" [CN]Issue"
              },
              "assigneeNickName": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"[CN]\""
              },
              "creatorNickName": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"[CN]\""
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "mineCreated": {
                "type": "boolean",
                "description": "See tool description for details"
              },
              "mineAssigned": {
                "type": "boolean",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "title": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"[CN]\"[CN]\"[CN]\""
              },
              "issueType": {
                "type": "string",
                "description": "See tool description for details"REQ\"[CN]\"BUG\""
              },
              "description": {
                "type": "string",
                "description": "See tool description for details"
              },
              "assigneeNickName": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"[CN]\"[CN]"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "issueId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "status": {
                "type": "string",
                "description": "See tool description for details"new\"[CN]\"assigned\"[CN]\"done\"[CN]\"cancel\""
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "issueId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "content": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"[CN]\"[CN]\"[CN]\""
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "search": {
                "type": "string",
                "description": "Search term"
              },
              "state": {
                "type": "string",
                "description": "See tool description for details"
              },
              "sourceBranch": {
                "type": "string",
                "description": "See tool description for details"
              },
              "targetBranch": {
                "type": "string",
                "description": "See tool description for details"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "Page number, default is 1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "search": {
                "type": "string",
                "description": "Search term"
              },
              "state": {
                "type": "string",
                "description": "See tool description for details"
              },
              "targetBranch": {
                "type": "string",
                "description": "See tool description for details"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "Page number, default is 1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              }
            },
            "required": []
          },
          "annotations": {}
        },
        {
          "name": "list_repo_merge_requests_reviewed_by_me",
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "search": {
                "type": "string",
                "description": "Search term"
              },
              "state": {
                "type": "string",
                "description": "See tool description for details"
              },
              "sourceBranch": {
                "type": "string",
                "description": "See tool description for details"
              },
              "targetBranch": {
                "type": "string",
                "description": "See tool description for details"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "Page number, default is 1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "search": {
                "type": "string",
                "description": "Search term"
              },
              "state": {
                "type": "string",
                "description": "See tool description for details"
              },
              "targetBranch": {
                "type": "string",
                "description": "See tool description for details"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "Page number, default is 1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              }
            },
            "required": []
          },
          "annotations": {}
        },
        {
          "name": "comment_merge_request_code_suggestion",
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "comment": {
                "type": "string",
                "description": "See tool description for details"
              },
              "suggestion": {
                "type": "string",
                "description": "See tool description for details"
              },
              "path": {
                "type": "string",
                "description": "See tool description for details"
              },
              "startLine": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "endLine": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "oldPath": {
                "type": "string",
                "description": "See tool description for details"
              },
              "newPath": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "noteId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "closed": {
                "type": "integer",
                "format": "int32",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "sourceBranch": {
                "type": "string",
                "description": "See tool description for details"
              },
              "targetBranch": {
                "type": "string",
                "description": "See tool description for details"
              },
              "title": {
                "type": "string",
                "description": "See tool description for details"
              },
              "description": {
                "type": "string",
                "description": "See tool description for details"
              },
              "assignees": {
                "type": "string",
                "description": "See tool description for details"
              },
              "assigneeStaffIds": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "search": {
                "type": "string",
                "description": "Search term"
              },
              "state": {
                "type": "string",
                "description": "See tool description for details"
              },
              "sourceBranch": {
                "type": "string",
                "description": "See tool description for details"
              },
              "targetBranch": {
                "type": "string",
                "description": "See tool description for details"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "Page number, default is 1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "note": {
                "type": "string",
                "description": "See tool description for details"
              },
              "path": {
                "type": "string",
                "description": "See tool description for details"
              },
              "line": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "Page number, default is 1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "noteId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "mergeType": {
                "type": "string",
                "description": "See tool description for details"
              },
              "mergeMessage": {
                "type": "string",
                "description": "See tool description for details"
              },
              "removeSourceBranch": {
                "type": "boolean",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "title": {
                "type": "string",
                "description": "See tool description for details"
              },
              "description": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "page": {
                "type": "integer",
                "format": "int64",
                "description": "Page number, default is 1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "mergeRequestId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "note": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "question": {
                "type": "string",
                "description": "See tool description for details"
              },
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "limit": {
                "type": "integer",
                "format": "int32",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "search": {
                "type": "string",
                "description": "See tool description for details"
              },
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "fileName": {
                "type": "string",
                "description": "See tool description for details"
              },
              "page": {
                "type": "integer",
                "format": "int32",
                "description": "Page number, default is 1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int32",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "search": {
                "type": "string",
                "description": "See tool description for details"
              },
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "lang": {
                "type": "string",
                "description": "See tool description for details"
              },
              "page": {
                "type": "integer",
                "format": "int32",
                "description": "Page number, default is 1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int32",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "search": {
                "type": "string",
                "description": "See tool description for details"
              },
              "repo": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"foo/bar\"[CN]\"git@gitlab.alibaba-inc.com:foo/bar.git\"[CN]"
              },
              "fileName": {
                "type": "string",
                "description": "See tool description for details"
              },
              "page": {
                "type": "integer",
                "format": "int32",
                "description": "Page number, default is 1"
              },
              "pageSize": {
                "type": "integer",
                "format": "int32",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "codeRepoNames": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "See tool description for details"
              },
              "query": {
                "type": "string",
                "description": "See tool description for details"
              },
              "top": {
                "type": "integer",
                "format": "int32",
                "description": "See tool description for details"
              },
              "includeContent": {
                "type": "boolean",
                "description": "See tool description for details"
              },
              "scoreThreshold": {
                "type": "number",
                "format": "double",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "codeRepoName": {
                "type": "string",
                "description": "See tool description for details"
              },
              "pageId": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "codeRepoName": {
                "type": "string",
                "description": "See tool description for details"
              },
              "parentUuid": {
                "type": "string",
                "description": "See tool description for details"
              },
              "recursive": {
                "type": "boolean",
                "description": "See tool description for details"
              },
              "maxDepth": {
                "type": "integer",
                "format": "int32",
                "description": "See tool description for details"
              },
              "format": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "workspaceId": {
                "type": "string",
                "description": "See tool description for details"
              },
              "docType": {
                "type": "string",
                "description": "See tool description for details"
              },
              "name": {
                "type": "string",
                "description": "See tool description for details"
              },
              "parentNodeId": {
                "type": "string",
                "description": "See tool description for details"
              },
              "content": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "docKey": {
                "type": "string",
                "description": "See tool description for details"
              },
              "content": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "question": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "question": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "question": {
                "type": "string",
                "description": "See tool description for details"
              },
              "pageRepoId": {
                "type": "string",
                "description": "Internal tool description (originally in Chinese)"1,2,3\"[CN]"
              },
              "pageGroupId": {
                "type": "string",
                "description": "See tool description for details"1,2,3\""
              },
              "chatSessionId": {
                "type": "string",
                "description": "See tool description for details"
              },
              "topK": {
                "type": "integer",
                "format": "int32",
                "description": "See tool description for details"
              },
              "skipFinalAnswer": {
                "type": "boolean",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "query": {
                "type": "string",
                "description": "See tool description for details"
              },
              "repoIds": {
                "type": "array",
                "items": {
                  "type": "integer",
                  "format": "int32"
                },
                "description": "See tool description for details"
              },
              "topK": {
                "type": "integer",
                "format": "int32",
                "description": "See tool description for details"
              },
              "instruction": {
                "type": "string",
                "description": "See tool description for details"
              },
              "rerankInstruction": {
                "type": "string",
                "description": "See tool description for details"
              },
              "scoreThreshold": {
                "type": "number",
                "format": "double",
                "description": "See tool description for details"
              },
              "groupIds": {
                "type": "array",
                "items": {
                  "type": "integer",
                  "format": "int32"
                },
                "description": "See tool description for details"
              },
              "mode": {
                "type": "string",
                "description": "See tool description for details"
              },
              "summary": {
                "type": "boolean",
                "description": "See tool description for details"
              },
              "recallLimit": {
                "type": "integer",
                "format": "int32",
                "description": "See tool description for details"
              },
              "tags": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "description": "See tool description for details"
              },
              "parentUuid": {
                "type": "string",
                "description": "See tool description for details"
              },
              "recursive": {
                "type": "boolean",
                "description": "See tool description for details"
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
          "description": "See tool description for details",
          "inputSchema": {
            "type": "object",
            "properties": {
              "repoId": {
                "type": "integer",
                "format": "int64",
                "description": "See tool description for details"
              },
              "content": {
                "type": "string",
                "description": "See tool description for details"
              },
              "fileName": {
                "type": "string",
                "description": "See tool description for details"
              },
              "dirNamePath": {
                "type": "string",
                "description": "See tool description for details"
              },
              "parentUuid": {
                "type": "string",
                "description": "See tool description for details"
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
