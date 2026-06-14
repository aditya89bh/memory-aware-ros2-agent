"""Release artifact validation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path


@dataclass(frozen=True)
class ReleaseArtifactReport:
    """Validation result for release artifacts."""

    wheel_count: int
    sdist_count: int
    hashes: dict[str, str]

    @property
    def is_valid(self) -> bool:
        """Return whether exactly one wheel and one source distribution exist."""

        return self.wheel_count == 1 and self.sdist_count == 1 and bool(self.hashes)


def validate_release_artifacts(dist_dir: Path) -> ReleaseArtifactReport:
    """Validate release artifacts and calculate SHA256 hashes."""

    wheels = tuple(dist_dir.glob("*.whl"))
    sdists = tuple(dist_dir.glob("*.tar.gz"))
    artifacts = sorted((*wheels, *sdists))
    return ReleaseArtifactReport(
        wheel_count=len(wheels),
        sdist_count=len(sdists),
        hashes={artifact.name: _sha256_file(artifact) for artifact in artifacts},
    )


def _sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()
