"""Every bundled environment must be a valid, installed Nav2 / slam_toolbox map."""

import pathlib
import re

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAP_YAMLS = sorted((ROOT / 'envs').glob('*/map.yaml'))

# map.yaml files whose `image:` is an absolute, deployment-specific path instead
# of the bundled image next to the YAML (nav2_map_server resolves relative
# paths against the YAML's directory, so `image: map.pgm` works everywhere).
KNOWN_ABSOLUTE_IMAGE = {
    'house': 'points at /robot/ros2_ws/install/share/... (one specific install layout)',
    'laboriii': 'points at /robot/data/map.pgm, not the bundled map',
}


def env(path):
    return path.parent.name


def load(path):
    return yaml.safe_load(path.read_text())


def read_pgm_header(path):
    """Return (width, height, maxval, header_len) of a binary (P5) PGM."""
    data = path.read_bytes()
    tokens, pos = [], 0
    while len(tokens) < 4:
        m = re.compile(rb'\s*(#[^\n]*\n\s*)*(\S+)').match(data, pos)
        assert m, f'{path}: truncated PGM header'
        tokens.append(m.group(2))
        pos = m.end()
    magic, w, h, maxval = tokens
    assert magic == b'P5', f'{path}: expected binary PGM (P5), got {magic!r}'
    return int(w), int(h), int(maxval), pos + 1, len(data)


def test_maps_found():
    assert MAP_YAMLS, 'no envs/*/map.yaml found'


@pytest.mark.parametrize('path', MAP_YAMLS, ids=env)
def test_map_yaml_is_valid_for_map_server(path):
    m = load(path)
    for key in ('image', 'resolution', 'origin', 'negate', 'occupied_thresh', 'free_thresh'):
        assert key in m, f'{env(path)}: missing {key}'
    assert m['resolution'] > 0
    assert len(m['origin']) == 3 and all(isinstance(v, (int, float)) for v in m['origin'])
    assert m['negate'] in (0, 1)
    assert 0 <= m['free_thresh'] < m['occupied_thresh'] <= 1
    assert m.get('mode', 'trinary') in ('trinary', 'scale', 'raw')
    assert pathlib.PurePosixPath(m['image']).suffix in ('.pgm', '.png')


@pytest.mark.parametrize('path', MAP_YAMLS, ids=env)
def test_bundled_image_is_a_plausible_map(path):
    pgm = path.parent / 'map.pgm'
    w, h, maxval, header_len, size = read_pgm_header(pgm)
    assert 10 <= w <= 20000 and 10 <= h <= 20000, (w, h)
    assert maxval in (255, 65535)
    assert size - header_len == w * h * (1 if maxval < 256 else 2), 'pixel data size mismatch'
    res = load(path)['resolution']
    # A building-scale map: between 1 m and 1 km on each side.
    assert 1 <= w * res <= 1000 and 1 <= h * res <= 1000


def _image_case(path):
    reason = KNOWN_ABSOLUTE_IMAGE.get(env(path))
    marks = [pytest.mark.xfail(strict=True, reason=reason)] if reason else []
    return pytest.param(path, id=env(path), marks=marks)


@pytest.mark.parametrize('path', [_image_case(p) for p in MAP_YAMLS])
def test_image_path_points_at_bundled_image(path):
    image = pathlib.Path(load(path)['image'])
    assert not image.is_absolute(), f'absolute image path {image}'
    assert (path.parent / image).is_file()


@pytest.mark.parametrize('path', MAP_YAMLS, ids=env)
def test_slam_toolbox_serialization_is_complete(path):
    """slam_toolbox needs both halves of a serialized map."""
    graph, data = path.parent / 'map.posegraph', path.parent / 'map.data'
    assert graph.is_file() == data.is_file(), 'posegraph and data must come in pairs'
    if graph.is_file():
        assert graph.stat().st_size > 0 and data.stat().st_size > 0


def test_every_map_file_is_installed():
    cmake = re.sub(r'#.*', '', (ROOT / 'CMakeLists.txt').read_text())
    installed = set()
    for files, dest in re.findall(
            r'install\s*\(\s*FILES(.*?)DESTINATION\s+share/\$\{PROJECT_NAME\}/?(\S*)\s*\)',
            cmake, re.S):
        for src in files.split():
            assert (ROOT / src).is_file(), f'CMake installs missing file {src}'
            installed.add(src)
    shipped = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'envs').rglob('*') if p.is_file()}
    assert shipped <= installed, f'not installed: {sorted(shipped - installed)}'
