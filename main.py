import os
import json
import subprocess
import sys
import time

from typing import Literal, Union

config_type = dict[
    Union[Literal["project_lang", "enable_addlicense"]],
    Union[list[Union[Literal["python", "rust"], str]], bool],
]


def main():
    config_filepath = os.path.join(
        (os.path.dirname(__file__)), "ptl_config.json"
    )
    with open(config_filepath, "r", encoding="utf-8") as f:
        config: config_type = json.load(f)
    #
    start_time = time.time()
    print("開始！")
    #
    for lang in config["project_lang"]:  # pyright: ignore[reportGeneralTypeIssues]
        if lang == "python":
            print("-" * 10, "python (pip-licenses)", "-" * 10)
            command = [
                "uv",
                "run",
                "pip-licenses",
                "--format=html",
                "--output-file",
                "ThirdPartyLicense-Python.html",
                "--from=mixed",
                "--with-urls",
            ]

        elif lang == "rust":
            print("-" * 10, "rust (cargo-about)", "-" * 10)
            command = [
                "cargo-about",
                "generate",
                "--output-file",
                "ThirdPartyLicense-Rust.html",
                "about.hbs",
                "--threshold",
                "1.0",
            ]
        else:
            print(f"錯誤！不支援的語言：{lang}")
            continue
        subprocess.run(
            command,
            check=True,
            stdout=sys.stdout,
            stdin=sys.stdin,
            stderr=sys.stderr,
            timeout=120,
        )
    if config["enable_addlicense"] is True:
        print("license check (addlicense)")
        ignores = [
            "-ignore",
            "**/.git/**",
            "-ignore",
            "**/.venv/**",
            "-ignore",
            "dist/**",
            "-ignore",
            "pkg/**",
            "-ignore",
            "target/**",
            "-ignore",
            "build/**",
            "-ignore",
            "**/__pycache__/**",
            "-ignore",
            "**/*.lock",
            "-ignore",
            "**/*.png",
            "-ignore",
            "**/*.kra",
            "-ignore",
            "**/*.ttf",
            "-ignore",
            "assets/",
            "-ignore",
            "**/*.json",
            "-ignore",
            "ThirdPartyLicense-Rust.html",
            "-ignore",
            "ThirdPartyLicense-Python.html",
            "-ignore",
            "src/licenses_rust.rs",
            "-ignore",
            "src/licenses_python.rs",
            "-ignore",
            "**/*.icon",
            "-ignore",
            "**/*.sh",
            "-ignore",
            "positive_license_tool/**",  # positive_license_tool
            "-ignore",
            "**/.python-version",  # uv python's version
        ]
        command = [
            "addlicense",
            "-check",
            "-f",
            "addlicense.template",
            ".",
        ]
        command.extend(ignores.copy())
        print(" ".join(command))
        print("-" * 10)
        process = subprocess.run(
            command,
            # check=True,
            stdout=sys.stdout,
            stdin=sys.stdin,
            stderr=sys.stderr,
            timeout=90,
        )
        if process.returncode != 0:
            print("包含無license 標記的檔案！")
            format_command = [
                "addlicense",
                "-f",
                "addlicense.template",
                ".",
            ]
            format_command.extend(ignores.copy())
            print(f"命令：\n{format_command}")
    #
    print("完成！")
    end_time = time.time()
    print(f"花了：{str(end_time - start_time)}")


if __name__ == "__main__":
    main()
