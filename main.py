# SPDX-License-Identifier: AGPL-3.0-only
# 著作權所有 (C) 2026 TW0hank0
#
# 本檔案屬於 positive_toolbox 專案的一部分。
# 專案儲存庫：https://github.com/TW0hank0/positive_toolbox
#
# 本程式為自由軟體：您可以根據自由軟體基金會發佈的 GNU Affero 通用公共授權條款
# 第 3 版（僅此版本）重新發佈及/或修改本程式。
#
# 本程式的發佈是希望它能發揮功用，但不提供任何擔保；
# 甚至沒有隱含的適銷性或特定目的適用性擔保。詳見 GNU Affero 通用公共授權條款。
#
# 您應該已經收到一份 GNU Affero 通用公共授權條款副本。
# 如果沒有，請參見 <https://www.gnu.org/licenses/>。

import os
import json
import subprocess
import sys
import time

from typing import Literal, Union

config_type = dict[
    Union[
        Literal[
            "project_lang",
            "enable_addlicense",
            "enable_python_licensecheck",
        ]
    ],
    Union[list[Union[Literal["python", "rust"], str]], bool],
]


def main():
    #
    check_dir = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.path.dirname(os.path.dirname(__file__))
    )
    #
    config_filepath = os.path.join(
        os.path.dirname(__file__)
        if len(sys.argv) > 1
        else os.path.dirname(os.path.dirname(__file__)),
        "ptl_config.json",
    )
    with open(config_filepath, "r", encoding="utf-8") as f:
        config: config_type = json.load(f)
    #
    start_time = time.time()
    print("Start!")
    #
    for lang in config["project_lang"]:  # pyright: ignore[reportGeneralTypeIssues]
        if lang == "python":
            if config["enable_python_licensecheck"] is True:
                print("-" * 10, "python (licensecheck)", "-" * 10)
                command = ["uv", "run", "licensecheck"]
            else:
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
        print("-" * 10, "license check (addlicense)", "-" * 10)
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
            "**/rustup-init.sh",  # Rustup (Linux)
            "-ignore",
            "**/rustup-init.exe",  # Rustup (Windows)
            "-ignore",
            "positive_license_tool/**",  # positive_license_tool
            "-ignore",
            ".python-version",  # uv python's version
        ]
        command = [
            "addlicense",
            "-check",
            "-f",
            "addlicense.template",
        ]
        command.extend(ignores.copy())
        command.append(check_dir)
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
            print("包含無license 標記的檔案或其他錯誤！")
            format_command = [
                "addlicense",
                "-f",
                "addlicense.template",
            ]
            format_command.extend(ignores.copy())
            format_command.append(check_dir)
            print(f"命令：\n{' '.join(format_command)}")
    #
    print("Finish!")
    end_time = time.time()
    print(f"{str(end_time - start_time)} Secs")


if __name__ == "__main__":
    main()
