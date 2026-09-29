"""Build a pinned source companion. Python 3.11+; no network or extraction.

Inputs are downloaded upstream archives, not the development working tree.
Only the reviewed public project tree and the exact archives below are copied.
"""
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import zipfile

# archive: (SHA-256, public source URL)
INPUTS = {
    'wine-52796bf.tar.gz': ('1e4af10a578c8a7d1075f9cdbf68d02adc5302fd956b42e452d6eb44503f0531', 'https://codeload.github.com/AeroNico/proton-wine/tar.gz/52796bf615c265c23b22ae9dacc3da9e38c8487f'),
    'directaudio-2101085.tar.gz': ('f16bee1ba4864cad3ebcc704d02b31cefeecbd21fbd7e713bb3fa08f354c3408', 'https://codeload.github.com/The412Banner/directaudio/tar.gz/2101085596ffe4911f7686012a97585eacbde9d0'),
    'banners-wayland-0121416.tar.gz': ('6fa5d717bd93423867b696cff3ceb78ac1c9521c5b03daa092a1772c43700196', 'https://codeload.github.com/The412Banner/Banners-Turnip/tar.gz/0121416358dce37615bb3ff97e67980ce7baf353'),
    'dxvk-0cf0578.tar.gz': ('64b1c768dbff87cf7bbea6803502826491293be7a533d3079b8da69e1e7f0aa0', 'https://codeload.github.com/doitsujin/dxvk/tar.gz/0cf05780abd7250c2cd713b7749cf32180157cf5'),
    'directx-9df86f2.tar.gz': ('9c1b8bbfd2d6c758fac4d93c2808a46bc1eee429fe656b4f21b29e02615aa8aa', 'https://codeload.github.com/Joshua-Ashton/mingw-directx-headers/tar.gz/9df86f2341616ef1888ae59919feaa6d4fad693d'),
    'spirv-8b246ff.tar.gz': ('cfeed5f9a97d12a9761a26e7f5bd10fedb1a8ce92033075151ae3bc7206fc229', 'https://codeload.github.com/KhronosGroup/SPIRV-Headers/tar.gz/8b246ff75c6615ba4532fe4fde20f1be090c3764'),
    'vulkan-46dc0f6.tar.gz': ('322c947754bae5e3cdca3b21aba20f420569f14e4784b20cdbc7565e2b593734', 'https://codeload.github.com/KhronosGroup/Vulkan-Headers/tar.gz/46dc0f6e514f5730784bb2cac2a7c731636839e8'),
    'mesa-fe067b17d9.tar.gz': ('6eb6aebf2701f863185a28fe4ffa0cb5cfb3c78a266caa530352149a29d3b382', 'https://codeload.github.com/chaotic-cx/mesa-mirror/tar.gz/fe067b17d908d8f02e88ef3c4433ec5fbb66b2a9'),
    'mesa-wayland-base.tar.gz': ('aa7a338064a10ce4db4a729a15204b748f0ae5e8fa80aa2341840127f3f38f93', 'https://codeload.github.com/chaotic-cx/mesa-mirror/tar.gz/7cda7850edd103ace21aac37d416d2fdf7a282e1'),
    'mesa-wayland-a7xx.tar.gz': ('39103b7fe47ffd930ec0abcdc9b6847b8f3c5187b395ab6dc52d006d0245f976', 'https://codeload.github.com/chaotic-cx/mesa-mirror/tar.gz/7631b5254f1a0a4371f5594e630ce2f2b8394e73'),
    'mesa-wayland-a8xx.tar.gz': ('9cf1b8959d35bbaa6a35ea0e6bba09bce5970c399ccec090b51bbdb0cfe24582', 'https://codeload.github.com/chaotic-cx/mesa-mirror/tar.gz/12b7b819edb4ddd3580e7e5ffe384610ae726c90'),
    'mesa-wayland-smxz.tar.gz': ('dac01a757d1535ee2e243fa70ba92b5232f73091235dcb06dbf3c4773cfd833d', 'https://codeload.github.com/chaotic-cx/mesa-mirror/tar.gz/c501e1d16e11c256610cd5922b1afa5660f2f5ea'),
    'mesa-wayland-white.tar.gz': ('a3d1b88f7225a7eb9daff0b725965143b37447443cb480db3295b4ec7af551cd', 'https://codeload.github.com/whitebelyash/mesa-unified/tar.gz/9c475fc367a7283a7eee58501fb48149780f2c1e'),
    'mesa-wayland-upstream.tar.gz': ('2bf5207a17a7ba270839edcdfa63f8a77bd5446c90ee2988db3f6f2100dff3c7', 'https://codeload.github.com/chaotic-cx/mesa-mirror/tar.gz/bbc7792f717f27b17b4c12e6a4503d703a362aac'),
    'libdrm-2.4.134.tar.xz': ('ac5e74d157830eb8bee44c6a6bf3ad49774ef0dd2a72bdad74a8f20308b52a95', 'https://dri.freedesktop.org/libdrm/libdrm-2.4.134.tar.xz'),
    'xkbcommon-1.13.1.tar.gz': ('aeb951964c2f7ecc08174cb5517962d157595e9e3f38fc4a130b91dc2f9fec18', 'https://codeload.github.com/xkbcommon/libxkbcommon/tar.gz/refs/tags/xkbcommon-1.13.1'),
}


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def filtered_wine(path):
    """Exclude only the 16 vendored ELF libraries, not their headers or data."""
    result = io.BytesIO()
    omitted = []
    with tarfile.open(path) as original:
        with gzip.GzipFile(fileobj=result, mode='wb', mtime=0, filename='') as compressed:
            with tarfile.open(fileobj=compressed, mode='w|', format=tarfile.PAX_FORMAT) as output:
                for member in original:
                    if member.isfile():
                        with original.extractfile(member) as stream:
                            magic = stream.read(8)
                            stream.seek(0)
                            if magic.startswith((b'\x7fELF', b'MZ', b'!<arch>\n')):
                                if not (magic.startswith(b'\x7fELF') and '/android/wayland-deps/usr/lib/' in member.name):
                                    raise ValueError('Unexpected binary in Wine source: ' + member.name)
                                omitted.append({'path': member.name, 'sha256': hashlib.file_digest(stream, 'sha256').hexdigest()})
                                continue
                            output.addfile(member, stream)
                    else:
                        output.addfile(member)
    if len(omitted) != 16:
        raise ValueError('Unexpected vendored library count')
    return result.getvalue(), omitted


def main(inputs, output):
    root = Path(__file__).resolve().parents[1]
    subprocess.run([sys.executable, '-B', str(root / 'tools/check-publication.py')], check=True)
    for name, (digest, _) in INPUTS.items():
        if sha(inputs / name) != digest:
            raise ValueError('Wrong source archive: ' + name)
        with tarfile.open(inputs / name) as archive:
            archive.getmembers()  # Reject HTML responses or truncated archives.
    manifest = {'format': 1, 'sources': [], 'wine_omitted_prebuilt_libraries': []}
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_STORED, allowZip64=True) as bundle:
        for name, (digest, url) in INPUTS.items():
            included = name
            included_digest = digest
            if name == 'wine-52796bf.tar.gz':
                data, omitted = filtered_wine(inputs / name)
                included = 'wine-52796bf-source.tar.gz'
                included_digest = hashlib.sha256(data).hexdigest()
                manifest['wine_omitted_prebuilt_libraries'] = omitted
                bundle.writestr('upstream/' + included, data)
            else:
                bundle.write(inputs / name, 'upstream/' + included)
            manifest['sources'].append({'file': included, 'sha256': included_digest, 'original_sha256': digest, 'url': url})
        for path in sorted(root.rglob('*')):
            if '.git' not in path.relative_to(root).parts and path.is_file():
                bundle.write(path, 'thor-forever/' + path.relative_to(root).as_posix())
        bundle.writestr('SOURCE-MANIFEST.json', json.dumps(manifest, indent=2) + '\n')
        bundle.writestr('README.txt', 'Thor Forever source companion\n\nStart with thor-forever/docs/SOURCE-DISTRIBUTION.md and BUILDING.md.\nEach upstream archive retains its own licenses. No game files are included.\nWine source excludes 16 vendored compiled libraries; omissions are listed in\nSOURCE-MANIFEST.json. Their Mesa sources/patch recipes are included separately;\nWayland notices are included in thor-forever/notices/WAYLAND.txt.\n')
    with zipfile.ZipFile(output) as bundle:
        if bundle.testzip() is not None:
            raise ValueError('Source ZIP integrity failure')
    print(sha(output), output.name)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: package-sources.py ARCHIVE-DIRECTORY NEW-OUTPUT.zip')
    main(Path(sys.argv[1]), Path(sys.argv[2]))
