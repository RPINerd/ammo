#!/usr/bin/env python3
from pathlib import Path
from common import (
    fomod_selections_choose_files,
    mod_extracts_files,
    mod_installs_files,
)


def test_base_object_swapper():
    """
    Test that configuring base object swapper behaves correctly.
    This ensures the conversion of the 'source' folder from the
    XML into a full path is accurate.
    """
    files = [
        Path("Data/SKSE/Plugins/po3_BaseObjectSwapper.dll"),
        Path("Data/SKSE/Plugins/po3_BaseObjectSwapper.pdb"),
    ]

    fomod_selections_choose_files(
        "mock_base_object_swapper",
        files,
    )


def test_embers_xd():
    """
    In the past, there were some issues with Embers XD plugin becoming visible
    upon activate, but not persisting through a refresh.

    Test that only plugins located immediately under the Data folder are
    added to self.plugins for fomods.

    mock_embers_xd is a preconfigured fomod with a Data folder, so we can
    test this by merely activating, refreshing, and checking plugins.
    """
    files = [
        Path("Data/Embers XD - Fire Magick Add-On.esp"),
    ]

    mod_installs_files("mock_embers_xd", files)


def test_realistic_ragdolls():
    """
    Test advancing through the installer with default options.
    This verifies auto-selection for "selectExactlyOne"
    """
    files = [
        Path("Data/realistic_ragdolls_Realistic.esp"),
        Path("Data/meshes/actors/bear/character assets/skeleton.nif"),
        Path("Data/meshes/actors/canine/character assets dog/skeleton.nif"),
        Path("Data/meshes/actors/canine/character assets wolf/skeleton.nif"),
        Path("Data/meshes/actors/cow/character assets/skeleton.nif"),
        Path("Data/meshes/actors/deer/character assets/skeleton.nif"),
        Path("Data/meshes/actors/draugr/character assets/skeleton.nif"),
        Path("Data/meshes/actors/falmer/character assets/skeleton.nif"),
        Path("Data/meshes/actors/frostbitespider/character assets/skeleton.nif"),
        Path("Data/meshes/actors/giant/character assets/skeleton.nif"),
        Path("Data/meshes/actors/goat/character assets/skeleton.nif"),
        Path("Data/meshes/actors/hagraven/character assets/skeleton.nif"),
        Path("Data/meshes/actors/mudcrab/character assets/skeleton.nif"),
        Path("Data/meshes/actors/sabrecat/character assets/skeleton.nif"),
        Path("Data/meshes/actors/troll/character assets/skeleton.nif"),
        Path("Data/meshes/actors/werewolfbeast/character assets/skeleton.nif"),
        Path("Data/meshes/actors/wolf/character assets/skeleton.nif"),
        Path(
            "Data/meshes/actors/character/character assets female/skeleton_female.nif"
        ),
        Path(
            "Data/meshes/actors/character/character assets female/skeletonbeast_female.nif"
        ),
        Path("Data/meshes/actors/character/character assets/skeleton.nif"),
        Path("Data/meshes/actors/character/character assets/skeletonbeast.nif"),
    ]

    fomod_selections_choose_files(
        "mock_realistic_ragdolls",
        files,
    )


def test_realistic_ragdolls_no_ragdolls():
    """
    This verifies that selections in "selectExactlyOne" change flags only when they are supposed to.
    """
    files = [
        Path("Data/realistic_ragdolls_Realistic.esp"),
    ]

    fomod_selections_choose_files(
        "mock_realistic_ragdolls",
        files,
        selections=[
            {
                "page": 0,  # Force
                "option": 0,  # Realistic
            },
            {
                "page": 1,  # Ragdolls
                "option": 2,  # None (as opposed to all, or creatures only).
            },
        ],
    )


def test_extract_fake_fomod():
    """
    Tests that installing a mod that has a fomod dir but no
    ModuleConfig.txt extracts files to the expected locations.
    This behavior is needed by SkyUI.
    """
    files = [
        Path("fomod/no_module_conf.txt"),
        Path("some_plugin.esp"),
    ]
    mod_extracts_files("mock_skyui", files)


def test_activate_fake_fomod():
    """
    Tests that activating a mod that has a fomod dir but no
    ModuleConfig.txt installs symlinks to the expected locations.
    Notably, anything inside the fomod dir is undesired.
    """
    files = [
        Path("Data/some_plugin.esp"),
    ]
    mod_installs_files("mock_skyui", files)


def test_fomod_relighting_skyrim():
    """
    Relighting Skyrim uses the 'requiredInstallFiles' directive as well as
    conditional file installs that are matched according to flags configured
    by the users selections.

    This tests that requiredInstallFiles are included, and that conditionalFileInstalls
    are handled properly.
    """
    files = [
        # requiredInstallFiles
        Path("Data/meshes/Relight/LightOccluder.nif"),
        # Default options: USSEP yes, both indoors and outdoors
        Path("Data/RelightingSkyrim_SSE.esp"),
    ]

    fomod_selections_choose_files(
        "mock_relighting_skyrim",
        files,
    )


def test_fomod_relighting_skryim_exteriors_only():
    """
    Exteriors only does not rely on the USSEP flag, it is the same plugin
    regardless of whether the user selected the USSEP option.

    Test that the correct plugin is installed regardless of whether the user
    said they had USSEP. This verifies that flags correctly map to
    conditionalFileInstalls.
    """
    files = [
        # requiredInstallFiles
        Path("Data/meshes/Relight/LightOccluder.nif"),
        # exterior-only plugin
        Path("Data/RelightingSkyrim_SSE_Exteriors.esp"),
    ]

    # With ussep
    fomod_selections_choose_files(
        "mock_relighting_skyrim",
        files,
        selections=[
            {
                "page": 0,  # with or without ussep requirement
                "option": 0,  # with ussep
            },
            {
                "page": 1,  # choose a version to install
                "option": 1,  # exteriors only version.
            },
        ],
    )

    # Without ussep
    fomod_selections_choose_files(
        "mock_relighting_skyrim",
        files,
        selections=[
            {
                "page": 0,  # with or without ussep requirement
                "option": 1,  # without ussep
            },
            {
                "page": 1,  # choose a version to install
                "option": 1,  # exteriors only version.
            },
        ],
    )


def test_fomod_relighting_skyrim_interiors_only():
    """
    Interiors gets a different plugin depending on USSEP.

    This verifies that flags correctly map to conditionalFileInstalls.
    """
    files = [
        # requiredInstallFiles
        Path("Data/meshes/Relight/LightOccluder.nif"),
        # conditionalFileInstalls
        Path("Data/RelightingSkyrim_SSE_Interiors.esp"),
    ]

    # With ussep
    fomod_selections_choose_files(
        "mock_relighting_skyrim",
        files,
        selections=[
            {
                "page": 0,  # with/out ussep
                "option": 0,  # with
            },
            {
                "page": 1,  # version
                "option": 2,  # interiors only version
            },
        ],
    )

    files[-1] = Path("Data/RelightingSkyrim_SSE_Interiors_nonUSSEP.esp")
    # Without ussep
    fomod_selections_choose_files(
        "mock_relighting_skyrim",
        files,
        selections=[
            {
                "page": 0,  # with/out ussep
                "option": 1,  # without
            },
            {
                "page": 1,  # version
                "option": 2,  # interiors only version
            },
        ],
    )
