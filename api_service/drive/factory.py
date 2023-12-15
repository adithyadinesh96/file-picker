from typing import Type

from drive.google_drive import GoogleDriveManager
from drive.manager import DriveManager

_DRIVE_MAP = {
    'GOOGLE_DRIVE': GoogleDriveManager
}


def get_drive(drive_name: str) -> Type[DriveManager]:
    if drive_name not in _DRIVE_MAP:
        raise ValueError(f'Unknown drive type {drive_name}')
    return _DRIVE_MAP[drive_name]
