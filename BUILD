load("@bazel_lint//bazel:buildifier.bzl", "buildifier")
load("@bazel_lint//python:pylint.bzl", "pylint")
load("@bazel_lint//python:yapf.bzl", "yapf")

buildifier(
    name = "format_bazel",
    srcs = ["WORKSPACE"],
    glob = [
        "**/*BUILD",
        "**/*.bzl",
    ],
    glob_exclude = [
        "bazel-*/**",
    ],
)

yapf(
    name = "format_python",
    glob = [
        "**/*.py",
    ],
    glob_exclude = [
        "bazel-*/**",
    ],
    style_file = ".style.yapf",
)

pylint(
    name = "lint_python",
    glob = [
        "**/*.py",
    ],
    glob_exclude = [
        "bazel-*/**",
    ],
    rcfile = "pylintrc",
)

py_library(
    name = "shell_util",
    srcs = ["shell_util.py"],
    visibility = ["//visibility:public"],
)

py_library(
    name = "bazel_util",
    srcs = ["bazel_util.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":shell_util",
    ],
)

py_library(
    name = "git_util",
    srcs = ["git_util.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":shell_util",
    ],
)

py_library(
    name = "dev_util",
    srcs = ["dev_util.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":git_util",
    ],
)

py_binary(
    name = "gen_compile_commands",
    srcs = ["gen_compile_commands.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":bazel_util",
    ],
)

py_binary(
    name = "gen_pyright_config",
    srcs = ["gen_pyright_config.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":bazel_util",
        ":git_util",
    ],
)

py_binary(
    name = "run_all",
    srcs = ["run_all.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":gen_compile_commands",
        ":gen_pyright_config",
    ],
)
