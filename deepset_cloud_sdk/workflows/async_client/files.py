"""This module contains async functions for uploading files and folders to the Deepset Cloud."""
from pathlib import Path
from typing import List, Optional

from deepset_cloud_sdk.api.config import (
    API_KEY,
    API_URL,
    DEFAULT_WORKSPACE_NAME,
    CommonConfig,
)
from deepset_cloud_sdk.service.files_service import DeepsetCloudFile, FilesService


async def upload_file_paths(
    file_paths: List[Path],
    api_key: Optional[str] = None,
    api_url: Optional[str] = None,
    workspace_name: str = DEFAULT_WORKSPACE_NAME,
    blocking: bool = True,
    timeout_s: int = 300,
) -> None:
    """Upload files to the Deepset Cloud.

    :param file_paths: List of file paths to upload.
    :param api_key: API key to use for authentication.
    :param api_url: API URL to use for authentication.
    :param workspace_name: Name of the workspace to upload the files to.
    :param blocking: Whether to wait for the upload to finish.
    :param timeout_s: Timeout in seconds for the upload.
    """
    config = CommonConfig(api_key=api_key or API_KEY, api_url=api_url or API_URL)
    async with FilesService.factory(config) as file_service:
        await file_service.upload_file_paths(
            workspace_name=workspace_name, file_paths=file_paths, blocking=blocking, timeout_s=timeout_s
        )


async def upload_folder(
    folder_path: Path,
    api_key: Optional[str] = None,
    api_url: Optional[str] = None,
    workspace_name: str = DEFAULT_WORKSPACE_NAME,
    blocking: bool = True,
    timeout_s: int = 300,
) -> None:
    """Upload a folder to the Deepset Cloud.

    :param folder_path: Path to the folder to upload.
    :param api_key: API key to use for authentication.
    :param api_url: API URL to use for authentication.
    :param workspace_name: Name of the workspace to upload the files to.
    :param blocking: Whether to wait for the upload to finish.
    :param timeout_s: Timeout in seconds for the upload.
    """
    config = CommonConfig(api_key=api_key or API_KEY, api_url=api_url or API_URL)
    async with FilesService.factory(config) as file_service:
        await file_service.upload_folder(
            workspace_name=workspace_name, folder_path=folder_path, blocking=blocking, timeout_s=timeout_s
        )


async def upload_texts(
    dc_files: List[DeepsetCloudFile],
    api_key: Optional[str] = None,
    api_url: Optional[str] = None,
    workspace_name: str = DEFAULT_WORKSPACE_NAME,
    blocking: bool = True,
    timeout_s: int = 300,
) -> None:
    """Upload texts to the Deepset Cloud.

    :param dc_files: List of DeepsetCloudFile to upload.
    :param api_key: API key to use for authentication.
    :param api_url: API URL to use for authentication.
    :param workspace_name: Name of the workspace to upload the files to.
    :param blocking: Whether to wait for the upload to finish.
    :param timeout_s: Timeout in seconds for the upload.
    """
    config = CommonConfig(api_key=api_key or API_KEY, api_url=api_url or API_URL)
    async with FilesService.factory(config) as file_service:
        await file_service.upload_texts(
            workspace_name=workspace_name, dc_files=dc_files, blocking=blocking, timeout_s=timeout_s
        )