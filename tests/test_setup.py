import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from workstation_setup.cli import PROFILES, parser
from workstation_setup.catalog import DESKTOP
from workstation_setup.context import Context
from workstation_setup.modules import (
    dell,
    firmware,
    hyperx,
    multimedia,
    nvidia,
    virtualization,
)
from workstation_setup.runner import Runner
from workstation_setup.system import Facts, _edid_model


def facts(**overrides):
    values = {
        "distro": "fedora",
        "version": "44",
        "codename": "",
        "pretty_name": "Fedora Linux 44",
        "computer_vendor": "Dell Inc.",
        "computer_model": "Precision 3591",
        "architecture": "x86_64",
        "wsl": False,
        "memory_gib": 32.0,
        "nvidia": False,
        "nvidia_devices": (),
        "hyperx": False,
        "hyperx_usb_ids": (),
        "monitor_models": (),
        "dell_precision_3591": True,
        "dell_s3423dwc": False,
        "desktop": True,
        "secure_boot": "disabled",
    }
    values.update(overrides)
    return Facts(**values)


class RecordingRunner(Runner):
    def __init__(self):
        super().__init__(dry_run=True)
        self.commands = []

    def run(self, args, **kwargs):
        self.commands.append([str(item) for item in args])
        return super().run(args, **kwargs)


class SetupTests(unittest.TestCase):
    def context(self, system):
        return Context(ROOT, Path("/home/test"), system, RecordingRunner())

    def test_profiles_reference_known_modules(self):
        known = {
            "base", "firmware", "devops", "desktop", "multimedia", "vscode",
            "dell", "virtualization", "nvidia",
            "hyperx", "hashicorp", "integrations",
        }
        for modules in PROFILES.values():
            self.assertLessEqual(set(modules), known)

    def test_boolean_integration_flags(self):
        args = parser().parse_args(["--profile", "devops", "--no-openshift-cli"])
        self.assertFalse(args.openshift_cli)

    def test_desktop_uses_spectacle(self):
        for packages in DESKTOP.values():
            self.assertIn("spectacle", packages)
            self.assertNotIn("flameshot", packages)

    def test_nvidia_is_skipped_in_wsl(self):
        ctx = self.context(facts(wsl=True, nvidia=True))
        nvidia.install(ctx)
        self.assertEqual(ctx.runner.commands, [])

    def test_nvidia_secure_boot_prepares_akmods_key(self):
        ctx = self.context(facts(nvidia=True, secure_boot="enabled"))
        with patch("workstation_setup.modules.nvidia.Path.exists", return_value=False):
            nvidia.install(ctx)
        self.assertIn(["kmodgenca", "-a"], ctx.runner.commands)
        self.assertIn(["modinfo", "-F", "version", "nvidia"], ctx.runner.commands)

    def test_multimedia_fedora_configures_codecs(self):
        ctx = self.context(facts())
        multimedia.install(ctx)
        flattened = [" ".join(command) for command in ctx.runner.commands]
        self.assertTrue(any("rpmfusion-free-release-44" in command for command in flattened))
        self.assertIn(
            ["dnf", "swap", "-y", "ffmpeg-free", "ffmpeg", "--allowerasing"],
            ctx.runner.commands,
        )
        self.assertTrue(any("intel-media-driver" in command for command in flattened))

    def test_firmware_only_checks_for_updates(self):
        ctx = self.context(facts())
        firmware.install(ctx)
        self.assertIn(["fwupdmgr", "get-updates"], ctx.runner.commands)
        self.assertNotIn(["fwupdmgr", "update"], ctx.runner.commands)

    def test_virtualization_requires_memory(self):
        ctx = self.context(facts(memory_gib=8.0))
        virtualization.install(ctx)
        self.assertEqual(ctx.runner.commands, [])

    def test_us_international_layout_translation(self):
        ctx = self.context(facts(hyperx=True, hyperx_usb_ids=("0951:16dc",)))
        hyperx.install(ctx, keyboard_layout="us-intl")
        self.assertIn(
            ["localectl", "set-x11-keymap", "us", "", "intl"],
            ctx.runner.commands,
        )

    def test_edid_model_descriptor(self):
        data = bytearray(128)
        data[54:59] = b"\x00\x00\x00\xfc\x00"
        data[59:72] = b"S3423DWC\n    "
        self.assertEqual(_edid_model(bytes(data)), "S3423DWC")

    def test_dell_profile_installs_monitor_helper(self):
        ctx = self.context(facts(dell_s3423dwc=True))
        dell.install(ctx)
        flattened = [" ".join(command) for command in ctx.runner.commands]
        self.assertTrue(any("ddcutil" in command for command in flattened))
        self.assertTrue(any("assets/bin/dell-monitor" in command for command in flattened))


if __name__ == "__main__":
    unittest.main()
