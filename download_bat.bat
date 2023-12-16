@echo off
setlocal enabledelayedexpansion

REM Copyright (c) Meta Platforms, Inc. and affiliates.
REM This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

set PRESIGNED_URL=""
set MODEL_SIZE=""
set TARGET_FOLDER="."

set /p PRESIGNED_URL=Enter the URL from email: 
echo.
set /p MODEL_SIZE=Enter the list of models to download without spaces (7B,13B,70B,7B-chat,13B-chat,70B-chat), or press Enter for all: 
if "%MODEL_SIZE%" == "" set MODEL_SIZE=7B,13B,70B,7B-chat,13B-chat,70B-chat

echo Downloading LICENSE and Acceptable Usage Policy
curl -L %PRESIGNED_URL:*/=LICENSE% -o "%TARGET_FOLDER%\LICENSE"
curl -L %PRESIGNED_URL:*/=USE_POLICY.md% -o "%TARGET_FOLDER%\USE_POLICY.md"

echo Downloading tokenizer
curl -L %PRESIGNED_URL:*/=tokenizer.model% -o "%TARGET_FOLDER%\tokenizer.model"
curl -L %PRESIGNED_URL:*/=tokenizer_checklist.chk% -o "%TARGET_FOLDER%\tokenizer_checklist.chk"
set CPU_ARCH=$(uname -m)
if "%CPU_ARCH%" == "arm64" (
  cd %TARGET_FOLDER%
  md5sum -c tokenizer_checklist.chk
) else (
  cd %TARGET_FOLDER%
  md5sum -c tokenizer_checklist.chk
)

for %%m in (%MODEL_SIZE:,= %) do (
  if "%%m" == "7B" (
    set SHARD=0
    set MODEL_PATH=llama-2-7b
  ) else if "%%m" == "7B-chat" (
    set SHARD=0
    set MODEL_PATH=llama-2-7b-chat
  ) else if "%%m" == "13B" (
    set SHARD=1
    set MODEL_PATH=llama-2-13b
  ) else if "%%m" == "13B-chat" (
    set SHARD=1
    set MODEL_PATH=llama-2-13b-chat
  ) else if "%%m" == "70B" (
    set SHARD=7
    set MODEL_PATH=llama-2-70b
  ) else if "%%m" == "70B-chat" (
    set SHARD=7
    set MODEL_PATH=llama-2-70b-chat
  )

  echo Downloading !MODEL_PATH!
  mkdir "%TARGET_FOLDER%\!MODEL_PATH!"

  for /l %%s in (0,1,!SHARD!) do (
    curl -L %PRESIGNED_URL:*/=!MODEL_PATH!\consolidated.%%s.pth% -o "%TARGET_FOLDER%\!MODEL_PATH!\consolidated.%%s.pth"
  )

  curl -L %PRESIGNED_URL:*/=!MODEL_PATH!\params.json% -o "%TARGET_FOLDER%\!MODEL_PATH!\params.json"
  curl -L %PRESIGNED_URL:*/=!MODEL_PATH!\checklist.chk% -o "%TARGET_FOLDER%\!MODEL_PATH!\checklist.chk"
  echo Checking checksums
  if "%CPU_ARCH%" == "arm64" (
    cd "%TARGET_FOLDER%\!MODEL_PATH%"
    md5 checklist.chk
  ) else (
    cd "%TARGET_FOLDER%\!MODEL_PATH%"
    md5sum -c checklist.chk
  )
)
