import datetime
from pathlib import Path
from typing import Any, AsyncGenerator, List
from unittest.mock import AsyncMock, patch
from uuid import UUID

from deepset_cloud_sdk._api.config import DEFAULT_WORKSPACE_NAME
from deepset_cloud_sdk._api.files import File
from deepset_cloud_sdk._api.upload_sessions import (
    UploadSessionDetail,
    UploadSessionIngestionStatus,
    UploadSessionStatus,
    UploadSessionStatusEnum,
    UploadSessionWriteModeEnum,
    WriteMode,
)
from deepset_cloud_sdk._service.files_service import DeepsetCloudFile
from deepset_cloud_sdk.models import UserInfo
from deepset_cloud_sdk.workflows.sync_client.files import (
    get_upload_session,
    list_files,
    list_upload_sessions,
    upload,
    upload_file_paths,
    upload_texts,
)


@patch("deepset_cloud_sdk.workflows.sync_client.files.async_upload_file_paths")
def test_upload_file_paths(async_file_upload_mock: AsyncMock) -> None:
    upload_file_paths(
        file_paths=[Path("./tests/data/example.txt")],
        write_mode=WriteMode.FAIL,
    )
    async_file_upload_mock.assert_called_once_with(
        file_paths=[Path("./tests/data/example.txt")],
        api_key=None,
        api_url=None,
        workspace_name=DEFAULT_WORKSPACE_NAME,
        write_mode=WriteMode.FAIL,
        blocking=True,
        timeout_s=300,
        show_progress=True,
    )


@patch("deepset_cloud_sdk.workflows.sync_client.files.async_upload")
def test_upload_folder(async_upload_mock: AsyncMock) -> None:
    upload(
        paths=[Path("./tests/data/upload_folder")],
    )
    async_upload_mock.assert_called_once_with(
        paths=[Path("./tests/data/upload_folder")],
        api_key=None,
        api_url=None,
        workspace_name=DEFAULT_WORKSPACE_NAME,
        write_mode=WriteMode.KEEP,
        blocking=True,
        timeout_s=300,
        show_progress=True,
        recursive=False,
    )


@patch("deepset_cloud_sdk.workflows.sync_client.files.async_upload_texts")
def test_upload_texts(async_upload_texts_mock: AsyncMock) -> None:
    files = [
        DeepsetCloudFile(
            name="test_file.txt",
            text="test content",
            meta={"test": "test"},
        )
    ]
    upload_texts(files=files)
    async_upload_texts_mock.assert_called_once_with(
        files=files,
        api_key=None,
        api_url=None,
        workspace_name=DEFAULT_WORKSPACE_NAME,
        write_mode=WriteMode.KEEP,
        blocking=True,
        timeout_s=300,
        show_progress=True,
    )


def test_list_files() -> None:
    async def mocked_async_list_files(*args: Any, **kwargs: Any) -> AsyncGenerator[List[File], None]:
        yield [
            File(
                file_id=UUID("cd16435f-f6eb-423f-bf6f-994dc8a36a10"),
                url="/api/v1/workspaces/search tests/files/cd16435f-f6eb-423f-bf6f-994dc8a36a10",
                name="silly_things_1.txt",
                size=611,
                meta={},
                created_at=datetime.datetime.fromisoformat("2022-06-21T16:40:00.634653+00:00"),
            )
        ]

    with patch("deepset_cloud_sdk.workflows.sync_client.files.async_list_files", new=mocked_async_list_files):
        returned_files = list(
            list_files(
                workspace_name="my_workspace",
                name="test_file.txt",
                content="test content",
                odata_filter="test",
                batch_size=100,
                timeout_s=100,
            )
        )
        assert len(returned_files) == 1
        assert returned_files[0] == [
            File(
                file_id=UUID("cd16435f-f6eb-423f-bf6f-994dc8a36a10"),
                url="/api/v1/workspaces/search tests/files/cd16435f-f6eb-423f-bf6f-994dc8a36a10",
                name="silly_things_1.txt",
                size=611,
                meta={},
                created_at=datetime.datetime.fromisoformat("2022-06-21T16:40:00.634653+00:00"),
            )
        ]


def test_list_upload_sessions() -> None:
    async def mocked_async_upload_sessions(
        *args: Any, **kwargs: Any
    ) -> AsyncGenerator[List[UploadSessionDetail], None]:
        yield [
            UploadSessionDetail(
                session_id=UUID("cd16435f-f6eb-423f-bf6f-994dc8a36a10"),
                created_by=UserInfo(
                    user_id=UUID("cd16435f-f6eb-423f-bf6f-994dc8a36a10"),
                    given_name="Fake",
                    family_name="User",
                ),
                expires_at=datetime.datetime.fromisoformat("2022-06-21T16:40:00.634653+00:00"),
                created_at=datetime.datetime.fromisoformat("2022-06-21T16:10:00.634653+00:00"),
                write_mode=UploadSessionWriteModeEnum.KEEP,
                status=UploadSessionStatusEnum.CLOSED,
            )
        ]

    with patch(
        "deepset_cloud_sdk.workflows.sync_client.files.async_list_upload_sessions", new=mocked_async_upload_sessions
    ):
        returned_files = list(
            list_upload_sessions(
                workspace_name="my_workspace",
                is_expired=True,
                batch_size=100,
                timeout_s=100,
            )
        )
        assert len(returned_files) == 1
        assert returned_files[0] == [
            UploadSessionDetail(
                session_id=UUID("cd16435f-f6eb-423f-bf6f-994dc8a36a10"),
                created_by=UserInfo(
                    user_id=UUID("cd16435f-f6eb-423f-bf6f-994dc8a36a10"),
                    given_name="Fake",
                    family_name="User",
                ),
                expires_at=datetime.datetime.fromisoformat("2022-06-21T16:40:00.634653+00:00"),
                created_at=datetime.datetime.fromisoformat("2022-06-21T16:10:00.634653+00:00"),
                write_mode=UploadSessionWriteModeEnum.KEEP,
                status=UploadSessionStatusEnum.CLOSED,
            )
        ]


def test_get_upload_session() -> None:
    existing_upload_session = UploadSessionStatus(
        session_id=UUID("cd16435f-f6eb-423f-bf6f-994dc8a36a10"),
        expires_at=datetime.datetime.fromisoformat("2022-06-21T16:40:00.634653+00:00"),
        documentation_url="https://docs.deepset.ai",
        ingestion_status=UploadSessionIngestionStatus(
            failed_files=0,
            finished_files=1,
        ),
    )

    async def mocked_async_get_upload_session(*args: Any, **kwargs: Any) -> UploadSessionStatus:
        return existing_upload_session

    with patch(
        "deepset_cloud_sdk.workflows.sync_client.files.async_get_upload_session", new=mocked_async_get_upload_session
    ):
        returned_upload_session = get_upload_session(
            workspace_name="my_workspace",
            session_id=UUID("cd16435f-f6eb-423f-bf6f-994dc8a36a10"),
        )
        returned_upload_session == existing_upload_session
